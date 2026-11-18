"""Assemble the saved HW3 Part C conversations; never run Cartwheel."""
import sys,json,re,hashlib,random,argparse
from pathlib import Path
from collections import Counter
sys.path.insert(0,str(Path.cwd()))
from scenarios.validate import validate_scenarios
from agent.db import connection
from agent.auth import AuthContext,can_view_order
parser=argparse.ArgumentParser(description='Assemble HW3 scenarios from saved generation and critique responses.')
parser.add_argument('--allow-pending-critique',action='store_true',help='Write drafts with explicit pending critique status.')
args=parser.parse_args()
base=Path('scenarios');audit=base/'generation_audit'
manifest=audit/'validation_summary.json'
previous=json.loads(manifest.read_text()) if manifest.exists() else {}
for name,digest in previous.get('assembled_sha256',{}).items():
 path=base/name
 if path.exists() and hashlib.sha256(path.read_bytes()).hexdigest()!=digest:
  raise SystemExit(f'{path} changed after assembly; preserve and reconcile those edits before rebuilding.')
pending=sorted(p.stem for p in (audit/'generation').glob('support-*.json') if not (audit/'critic'/p.name).exists())
if pending and not args.allow_pending_critique:
 raise SystemExit(f'{len(pending)} critiques pending; finish them first or explicitly use --allow-pending-critique.')
plans=json.loads((base/'support_plan.json').read_text())
rows=[];changed=[]
for plan in plans:
 rec=plan['record'];sid=rec['id']
 draft=json.loads((audit/'generation'/f'{sid}.json').read_text())
 critic_path=audit/'critic'/f'{sid}.json'
 reviewed=critic_path.exists()
 critic=json.loads(critic_path.read_text()) if reviewed else draft
 if reviewed:
  assert isinstance(critic['issues'],list),sid
  assert isinstance(critic['changed'],bool),sid
 actual_changed=any(draft[k]!=critic[k] for k in ['opening_message','followups'])
 # The stored text is authoritative for the change count, independently of its flag.
 if actual_changed:changed.append(sid)
 bindings={'[ORDER]':str(rec['tuple'].get('order_id','')),'[PRODUCT]':str(rec['tuple'].get('product_id',''))}
 def bind(s):
  for old,new in bindings.items():
   if old in s:assert new,(sid,old)
   s=s.replace(old,new)
  assert not re.search(r'\[(ORDER|PRODUCT)\]',s),sid
  return s
 messages=[critic['opening_message'],*critic['followups']]
 if rec['tuple'].get('order_id'):
  assert any('[ORDER]' in message for message in messages),(sid,'missing planned order reference')
 if rec['tuple']['intent']=='refund' and rec['grounding']['requested_refund_usd']!=rec['grounding']['record']['total_cents']/100:
  amount=f"{rec['grounding']['requested_refund_usd']:.2f}"
  assert any(amount in message for message in messages),(sid,'requested partial refund amount lost')
 if int(sid.split('-')[1]) in range(91,96) or rec['tuple']['turn_count']==3:
  assert '[ORDER]' not in messages[0] and '[ORDER]' in messages[-1],(sid,'clarification plan not preserved')
 rec['opening_message']=bind(critic['opening_message'])
 rec['followups']=[bind(s) for s in critic['followups']]
 rec['provenance']={'plan':'scenarios/support_plan.json','generation_input':f'scenarios/generation_audit/generation_inputs/{sid}.json','generation_output':f'scenarios/generation_audit/generation/{sid}.json','critic_input':f'scenarios/generation_audit/critic_inputs/{sid}.json','critic_output':f'scenarios/generation_audit/critic/{sid}.json' if reviewed else None,'critic_status':'completed' if reviewed else 'pending'}
 rows.append(rec)
summary=validate_scenarios(rows,final=True)
pilot=[json.loads(l) for l in (base/'pilot_scenarios.jsonl').read_text().splitlines() if l.strip()]
assert not {r['id'] for r in rows}&{r['id'] for r in pilot}
counts=Counter(r['tuple'].get('order_id') for r in rows)
assert all(counts[r['tuple']['order_id']]==1 for r in rows if r['tuple']['intent'] in ['refund','cancellation'])
with connection() as c:
 for r in rows:
  t=r['tuple'];user=c.execute('select * from users where id=?',(t['user_id'],)).fetchone()
  assert user['role']==t['role']
  if t.get('order_id'):
   o=c.execute('select * from orders where id=?',(t['order_id'],)).fetchone()
   assert dict(o)==r['grounding']['record'],r['id']
   allowed=can_view_order(AuthContext(user['id'],user['role'],user['store_id']),o['user_id'],o['store_id'])
   assert allowed==(r['grounding']['authorization_expected']=='allowed'),r['id']
   if not allowed:assert r['data_quality_case_id'] is None
  if t.get('product_id'):
   p=c.execute('select * from products where id=?',(t['product_id'],)).fetchone()
   assert dict(p)==r['grounding']['record']
# Publish only validated records; pending critiques remain explicit in provenance.
path=base/'support_scenarios.jsonl'
# Existing assembled outputs may be refreshed only when their saved hashes still match.
path.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
rng=random.Random(20260703)
monitor=[]
for intent in sorted({r['tuple']['intent'] for r in rows}):
 pool=[r for r in rows if r['scenario_group']=='coverage' and r['tuple']['intent']==intent]
 monitor+=rng.sample(pool,5)
quotas={'order_status':3,'refund':3,'cancellation':2,'policy_question':2,'product_search':3,'out_of_scope':2}
for intent,n in quotas.items():monitor+=rng.sample([r for r in rows if r['scenario_group']=='challenge' and r['tuple']['intent']==intent],n)
assert len(monitor)==50 and len({r['id'] for r in monitor})==50
assert {r['tuple']['role'] for r in monitor}=={'shopper','merchant','support'}
# Preserve edited outputs through the manifest hash check above.
(base/'monitoring_scenarios.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in monitor))
# Seven intent representatives + six defect cases + a long clarification + threshold boundary.
sample=[]
for intent in sorted({r['tuple']['intent'] for r in rows}):
 pool=[r for r in rows if r['scenario_group']=='coverage' and r['tuple']['intent']==intent]
 sample.append(pool[len(pool)//2])
for case in sorted({r['data_quality_case_id'] for r in rows if r['data_quality_case_id']}):
 sample.append(next(r for r in rows if r['data_quality_case_id']==case and r['tuple']['turn_count']==2))
sample.append(next(r for r in rows if r['tuple']['turn_count']==3))
sample.append(next(r for r in rows if r['scenario_group']=='challenge' and r['tuple']['intent']=='refund' and r['grounding']['requested_refund_usd']==100))
assert len(sample)==15 and len({r['id'] for r in sample})==15
assert {r['tuple']['role'] for r in sample}=={'shopper','merchant','support'}
lines=['# HW3 Part C: 15 scenarios for human review','','These are planned user messages, not observed Cartwheel responses. Review every','opening and followup. Check realism, grounded expectations and independence from','an assumed agent response. Record your decisions in `support_review.jsonl` using','`scenario_id`, `decision` (`accept`, `revise`, `reject`), `reason`, and `change`.',f'{len(pending)} automated critiques remain pending. Human review is also pending.', 'No human decisions have been filled in. Apply revisions and replace rejected','scenarios before running Cartwheel.','']
for r in sample:
 t=r['tuple'];lines += [f"## {r['id']}",'',f"Group: {r['scenario_group']}; role: {t['role']}; intent: {t['intent']}; style: {t['user_style']}; turns: {t['turn_count']}.",'']
 for i,s in enumerate([r['opening_message'],*r['followups']],1):lines += [f'{i}. {s}','']
 lines += ['Grounded expectation:','', '```json',json.dumps(r['expected'],indent=2,ensure_ascii=False),'```','']
 if r['data_quality_case_id']:lines += [f"Data quality case: `{r['data_quality_case_id']}`.",'']
(base/'support_sample.md').write_text('\n'.join(lines))
(base/'support_review_template.jsonl').write_text(''.join(json.dumps({'scenario_id':r['id'],'decision':None,'reason':'','change':None})+'\n' for r in sample))
report={'validation':summary,'generation_outputs':250,'critic_outputs':250-len(pending),'pending_critic_ids':pending,'conversations_changed_by_critic':len(changed),'changed_scenario_ids':changed,'human_review_status':'pending','sample_ids':[r['id'] for r in sample],'monitoring':{'count':50,'groups':dict(Counter(r['scenario_group'] for r in monitor)),'roles':dict(Counter(r['tuple']['role'] for r in monitor))},'checks':'offline schema, composition, unique conversations and IDs, disjoint pilot IDs, identities, authorization, ground truth snapshots, unique write targets, policy references in plan checks','cartwheel_runs':0,'pilot_exception':'Student explicitly authorized generation without five confirmed pilot failures. Pilot assessments preserved.'}
report['assembled_sha256']={name:hashlib.sha256((base/name).read_bytes()).hexdigest() for name in ['support_scenarios.jsonl','monitoring_scenarios.jsonl','support_sample.md','support_review_template.jsonl']}
(audit/'validation_summary.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'validation':summary,'generation_outputs':250,'critic_outputs':250-len(pending),'pending_critiques':len(pending),'human_review_status':'pending'},indent=2))
