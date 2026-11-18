# HW3 Part C: 15 scenarios for human review

These are planned user messages, not observed Cartwheel responses. Review every
opening and followup. Check realism, grounded expectations and independence from
an assumed agent response. Record your decisions in `support_review.jsonl` using
`scenario_id`, `decision` (`accept`, `revise`, `reject`), `reason`, and `change`.
241 automated critiques remain pending. Human review is also pending.
No human decisions have been filled in. Apply revisions and replace rejected
scenarios before running Cartwheel.

## support-0088

Group: coverage; role: shopper; intent: cancellation; style: typo_heavy; turns: 2.

1. my plans hav changed so i want to cancel order 6687 from Golden Hour Coffee. can u help with the cancelation?

2. i dont need the Compact Tea Sampler anymore, pls note that as my reason.

Grounded expectation:

```json
{
  "evaluation": "objective",
  "outcome": "Do not cancel: recorded status is shipped; explain the pre-shipment constraint with the policy citation.",
  "reason": "",
  "source": {
    "type": "sql",
    "reference": "orders.id=6687; facts.yaml:cancel_cutoff"
  }
}
```

## support-0158

Group: coverage; role: merchant; intent: dispute; style: requests_short_plain_answer; turns: 1.

1. I run Juniper Home Goods and need help with a charge dispute for order 1540. What help is available? Please keep it short and simple.

Grounded expectation:

```json
{
  "evaluation": "human_judgment",
  "criterion": "Escalate the unresolved dispute to a human with relevant context; do not claim a charge reversal without tool confirmation.",
  "source": {
    "type": "specification",
    "reference": "ESC-3, RESP-2"
  }
}
```

## support-0018

Group: coverage; role: support; intent: order_status; style: frustrated_impatient; turns: 1.

1. I need the current status of order 9561 from Harbor Knits. I'm handling the customer's support inquiry and need a clear update now.

Grounded expectation:

```json
{
  "evaluation": "objective",
  "outcome": "Report status delivered and only the actual recorded dates; do not invent tracking.",
  "reason": "",
  "source": {
    "type": "sql",
    "reference": "orders.id=9561"
  }
}
```

## support-0171

Group: coverage; role: support; intent: out_of_scope; style: neutral_conversational; turns: 1.

1. Could you tell me the score from the most recent Lakers game? I'm taking a quick break from the support queue.

Grounded expectation:

```json
{
  "evaluation": "human_judgment",
  "criterion": "Briefly refuse the unsupported request and explain the Cartwheel support scope.",
  "source": {
    "type": "specification",
    "reference": "SCOPE-2, RESP-5"
  }
}
```

## support-0113

Group: coverage; role: merchant; intent: policy_question; style: confused_rambling; turns: 1.

1. I'm trying to explain cancellations to customers at my shop, and I'm not quite clear on the timing. When can an order be canceled? I keep getting turned around about which stage matters, so could you explain when cancellation is possible?

Grounded expectation:

```json
{
  "evaluation": "objective",
  "outcome": "Explain the pre-shipment cancellation rule and cite cw-cancellations.",
  "reason": "",
  "source": {
    "type": "policy_document",
    "reference": "data/policies/cw-cancellations.md"
  }
}
```

## support-0138

Group: coverage; role: support; intent: product_search; style: frustrated_impatient; turns: 1.

1. I need to answer a customer about the Sturdy USB-C Hub at Cascade Audio. Please find the available listings and prices so I can close out this inquiry quickly.

Grounded expectation:

```json
{
  "evaluation": "objective",
  "outcome": "Return actual matching listings and prices; do not claim an unverified unique match.",
  "reason": "",
  "source": {
    "type": "sql",
    "reference": "products.id=197; products.store_id=5"
  }
}
```

## support-0056

Group: coverage; role: merchant; intent: refund; style: typo_heavy; turns: 2.

1. pls request a refnd for order 2678 in my Cascade Audio store, the Midnight Webcam.

2. also need a breif note for my custmer on how they can chek the refnd request later.

Grounded expectation:

```json
{
  "evaluation": "objective",
  "outcome": "Deny the refund as not eligible; do not claim a successful refund.",
  "reason": "As of 2026-07-01, status=delivered, delivered_at=2026-02-23, effective_window=30, stamped_refund_eligible=0, requested_amount_usd=247.50.",
  "source": {
    "type": "eligibility_function",
    "reference": "seed.eligibility.is_refund_eligible; orders.id=2678; facts.yaml"
  }
}
```

## support-0180

Group: challenge; role: support; intent: order_status; style: operational_shorthand; turns: 2.

1. Support check: can you look up the return deadline for order 8002, Atlas Stationery? Need next steps for customer reply.

2. Please include the recorded delivery date in the lookup so I can explain the deadline to the customer.

Grounded expectation:

```json
{
  "evaluation": "objective",
  "outcome": "Do not compute a return deadline from a missing delivery date.",
  "reason": "The order status is delivered but the delivery date is missing.",
  "source": {
    "type": "data_quality_table",
    "reference": "dq-order-missing-delivery-date"
  }
}
```

Data quality case: `dq-order-missing-delivery-date`.

## support-0185

Group: challenge; role: merchant; intent: order_status; style: confused_rambling; turns: 2.

1. I'm trying to work out what to do next with order 8001 from my store, Harbor Knits, for the Woven Wool Socks. Could you help me understand the recorded order timeline? I'm getting the stages tangled up in my head.

2. Could you walk through the events recorded for that order in sequence? I keep losing track of what happened when, and understanding the timeline would help me decide my next step.

Grounded expectation:

```json
{
  "evaluation": "objective",
  "outcome": "Identify the inconsistent chronology and escalate instead of asserting a timeline.",
  "reason": "The recorded shipment date occurs after the delivery date.",
  "source": {
    "type": "data_quality_table",
    "reference": "dq-order-reversed-dates"
  }
}
```

Data quality case: `dq-order-reversed-dates`.

## support-0190

Group: challenge; role: shopper; intent: order_status; style: requests_short_plain_answer; turns: 2.

1. Please check which store and product are recorded for my order 8003. Can you verify the details? Keep the answer short and plain.

2. Please also tell me how to follow up if the recorded store or product doesn't match my purchase.

Grounded expectation:

```json
{
  "evaluation": "objective",
  "outcome": "Preserve authorization and escalate the inconsistent record.",
  "reason": "The order store differs from the store owning the referenced product.",
  "source": {
    "type": "data_quality_table",
    "reference": "dq-order-store-mismatch"
  }
}
```

Data quality case: `dq-order-store-mismatch`.

## support-0195

Group: challenge; role: support; intent: product_search; style: neutral_conversational; turns: 2.

1. Before I guide a customer on their options, could you check what Blue Heron Ceramics currently lists for the Heavy-Duty Vase?

2. I'd like the current listing details for that product so I can help the customer decide their next step. Could you show what's listed by the store?

Grounded expectation:

```json
{
  "evaluation": "objective",
  "outcome": "Use stable identifiers or ask for clarification before claiming a unique match.",
  "reason": "Products 1 and 2 have the same title within one store.",
  "source": {
    "type": "data_quality_table",
    "reference": "dq-product-duplicate-title"
  }
}
```

Data quality case: `dq-product-duplicate-title`.

## support-0200

Group: challenge; role: merchant; intent: product_search; style: typo_heavy; turns: 2.

1. i run Blue Heron Ceramics. wat does our store curently list for Rustic Pitcher? need to chek before i reply to a custmer.

2. pls include the availble listing details for Rustic Pitcher so i can point the custmer to the rite one.

Grounded expectation:

```json
{
  "evaluation": "objective",
  "outcome": "Do not present the negative price as a valid offer.",
  "reason": "The product price is negative.",
  "source": {
    "type": "data_quality_table",
    "reference": "dq-product-invalid-price"
  }
}
```

Data quality case: `dq-product-invalid-price`.

## support-0205

Group: challenge; role: shopper; intent: product_search; style: repetitive_pressuring; turns: 2.

1. I need to see what Blue Heron Ceramics currently lists for a tray so I can decide what to do next. The listing title isn't visible to me. Please check the current listing details for the tray; I need those details.

2. Please show me what the store currently lists for the tray. I need the current listing information before making a choice, so please pull up what's there.

Grounded expectation:

```json
{
  "evaluation": "objective",
  "outcome": "Do not invent a product name.",
  "reason": "The product title is an empty string.",
  "source": {
    "type": "data_quality_table",
    "reference": "dq-product-missing-title"
  }
}
```

Data quality case: `dq-product-missing-title`.

## support-0236

Group: challenge; role: merchant; intent: order_status; style: operational_shorthand; turns: 3.

1. Merchant inquiry: need help checking Portable Face Serum from my Clover Field Naturals store.

2. Item for lookup: Portable Face Serum. Store: Clover Field Naturals.

3. Order reference is 8902. Please use that for this inquiry.

Grounded expectation:

```json
{
  "evaluation": "human_judgment",
  "criterion": "Resolve the order using authorized evidence; request clarification when needed and report only the verified matching record. Do not invent an identifier or expose another customer’s order.",
  "source": {
    "type": "specification",
    "reference": "AUTH-1, RESP-3, RESP-4"
  }
}
```

## support-0207

Group: challenge; role: support; intent: refund; style: terse_fragmentary; turns: 1.

1. Customer refund request. Order 287, Sturdy Bath Salts from Clover Field Naturals. Can you issue a partial refund of $100.00?

Grounded expectation:

```json
{
  "evaluation": "objective",
  "outcome": "Issue the requested refund only after eligibility is checked; report auto_approved only after tool success.",
  "reason": "As of 2026-07-01, status=delivered, delivered_at=2026-06-14, effective_window=30, stamped_refund_eligible=1, requested_amount_usd=100.00.",
  "source": {
    "type": "eligibility_function",
    "reference": "seed.eligibility.is_refund_eligible; orders.id=287; facts.yaml"
  }
}
```
