import asyncio,json,sqlite3,sys
from pathlib import Path
from datetime import date
sys.path.insert(0,str(Path.cwd()))
from dotenv import load_dotenv
from openai import AsyncOpenAI
from scenarios.validate import validate_scenarios
load_dotenv(Path.cwd() / '.env')
plans=json.loads(Path('scenarios/pilot_plan.json').read_text())
client=AsyncOpenAI(timeout=45,max_retries=1)
sem=asyncio.Semaphore(3)
async def call(prompt):
 async with sem:
  r=await client.chat.completions.create(model='gpt-4o-mini',messages=[{'role':'user','content':prompt}],response_format={'type':'json_object'},temperature=0.8)
  return json.loads(r.choices[0].message.content)
async def generate(plan):
 prompt='Write ONE realistic support conversation as JSON with opening_message (string) and followups (list of strings). Use exactly turn_count messages in total. Followups must make sense regardless of the preceding agent response. Preserve the assigned language style. Never assume the agent approved an action. Do not invent names, identifiers, prices, dates or policy rules. Use literal [ORDER] or [PRODUCT] where the goal includes that placeholder; these will be bound to verified identifiers afterward. Do not mention metadata, tools, or simulation. Do not expose statuses or facts you were not given. '+json.dumps(plan['prompt'])
 result=await call(prompt)
 r=plan['record']; binding={'[ORDER]':str(r['tuple'].get('order_id','')),'[PRODUCT]':str(r['tuple'].get('product_id',''))}
 for field in ['opening_message','followups']:
  texts=[result[field]] if field=='opening_message' else result[field]
  texts=[s.replace('[ORDER]',binding['[ORDER]']).replace('[PRODUCT]',binding['[PRODUCT]']) for s in texts]
  r[field]=texts[0] if field=='opening_message' else texts
 print('Generated',r['id'],flush=True)
 return r
async def main():
 records=await asyncio.gather(*(generate(p) for p in plans))
 openings=[r['opening_message'] for r in records]
 async def criticize(r,p):
  result=await call('Independently review and repair ONE synthetic support conversation. Return JSON opening_message and followups only. Preserve goal, grounded names and identifiers, number of turns, and assigned style. Check invented details against the actual record. Followups must work without knowing an agent response; remove response-dependent confirmations. Avoid template repetition compared with other openings. Do not add policy rules or internal metadata to user messages. Keep a natural user voice. '+json.dumps(dict(conversation={k:r[k] for k in ['opening_message','followups']},task=p['prompt'],actual_record=r['grounding']['record'],other_openings=[s for s in openings if s!=r['opening_message']])))
  r.update({k:result[k] for k in ['opening_message','followups']});print('Critiqued',r['id'],flush=True)
 await asyncio.gather(*(criticize(r,p) for r,p in zip(records,plans)))
 summary=validate_scenarios(records)
 path=Path('scenarios/pilot_scenarios.jsonl')
 with path.open('x') as out:
  for r in records:out.write(json.dumps(r,ensure_ascii=False)+'\n')
 print(json.dumps(summary))
asyncio.run(main())
