# Connected guide: Features, Stories, acceptance criteria, and test cases

Updated: 2026-10-22. Working example: Feature 16968945, Swap Agent Payment Enhancement, from the supplied screenshot. This guide replaces the earlier illustrative examples with this example. No Azure DevOps work items have been changed.

## Read this first

A Feature defines a valuable capability. Stories deliver specific outcomes within it. Acceptance criteria (ACs) state the conditions for accepting either. Test cases demonstrate whether those conditions hold; test steps specify actions and checks during execution. Tasks describe implementation work.

Do not turn this into a rule that Feature ACs are end-to-end and Story ACs are each processing step. End-to-end describes test scope. Feature versus Story describes requirement and delivery scope. A Story can span receipt, classification, netting, suppression, and accounting when that forms a small enough business outcome.

Microsoft documents Features containing smaller backlog items, Stories mapped to Features, and Tasks supporting Stories. It also documents Test Cases linked to requirements, with Action and Expected Result fields for individual steps. AC identifiers and the decomposition below are recommended team conventions, not extra mandatory Azure DevOps hierarchy levels. [Microsoft: Features](https://learn.microsoft.com/en-us/azure/devops/boards/backlogs/define-features-epics?view=azure-devops); [Microsoft: Agile workflow](https://learn.microsoft.com/en-us/azure/devops/boards/work-items/guidance/agile-process-workflow?view=azure-devops); [Microsoft: Test Cases](https://learn.microsoft.com/en-us/azure/devops/test/create-test-cases?view=azure-devops). Accessed 2026-10-22.

## Source interpretation and boundaries

The screenshot is the source for the product-specific rules. Proposed wording is a review draft, not confirmation that the rules are approved or complete. Original numbers below refer to the screenshot's 12 numbered criteria. Its field names, payment types, states, and Boolean expressions must be checked against editable source before implementation.

Items 1–4 and 11 describe a connected selected-counterparty processing route. Item 5 adds mixed-source/mixed-payment eligibility. Items 6–7 and 8–9 define alternative routes. Item 10 defines fallback behavior. Item 12 defines unmatched-flow behavior. Therefore the numbers are requirement references, not a single chronological test script.

For item 1, a possible reading is CCS AND (strategy SWAP_AGENT OR non-null Swap Agent Id) AND counterparty in the approved list. Confirm the parentheses and field paths. Item 8 also needs explicit parentheses around the payment-type alternatives. No inferred rule precedence is treated as approved.

## The connected model

```text
Feature: Swap Agent Payment Enhancement
  Feature ACs: complete routes, shared outcomes, exclusions and exceptions
  Shared rule tables: eligibility, precedence, key, schedule, status/output mapping
  |
  +-- S1: Process eligible selected-counterparty cashflows
  |     Story ACs: detailed routing, schedule, grouping, outputs, downstream results
  |     Tasks: implementation and verification work
  +-- S2: Process eligible SAL Coupon cashflows
  +-- S3: Process eligible SAL MTM cashflows
  +-- S4: Handle other payment types outside the selected list
  +-- S5: Handle eligible cashflows without a matching partner

Test Cases --verify--> Feature and Story ACs
  Focused tests: rule combinations, grouping, boundaries, state transitions
  Journey tests: actual upstream-to-downstream connections
  Each case contains executable actions and expected results
```

S1–S5 are candidate delivery slices. Estimate them before creating commitments. They are not guaranteed independent or sprint-sized. Shared suppression/accounting behavior can be implemented once and reused, with dependencies made explicit. If S1 is too large, retain the Feature outcome and split delivery at a demonstrable business or interface boundary; never assume a mocked downstream result proves live integration.

## What each artifact should contain

| Artifact | Purpose | Example in this Feature |
|---|---|---|
| Feature | Explain capability, scope, and exclusions. | Automate the specified Swap Agent and SAL cashflow processing routes and their downstream treatment. |
| Feature AC | Establish a complete outcome or a rule spanning the capability. | Eligible matching selected-counterparty flows complete the route through netting, resultant suppression, and accounting sent to EBBS. |
| Story | Deliver a specific usable or operational outcome. | Process eligible selected-counterparty flows through the agreed route. |
| Story AC | Define exact behavior, decisions, and boundaries for that outcome. | Cashflows differing in any required netting-key component are not grouped together. This is a proposed explicit interpretation of item 3, subject to approval. |
| Shared rule table | Maintain exact logic once. | Eligibility expressions, rule precedence, four-part key, statuses, and output payment types. |
| Task | Specify delivery work. | Implement classification; configure scheduling; implement grouping; add tests. |
| Test Case | Verify conditions with concrete data and repeatable actions. | Ingest compatible flows, run processing, inspect original and resultant states, and verify the accounting send. |
| Test step | Specify an action or verification within the case. | Trigger the scheduled job and inspect its processing outcome. |

## Proposed Feature acceptance criteria

The following criteria summarize the outcome and retain critical constraints. They reference the detailed Story ACs and shared rules rather than copying their wording.

| ID | Draft Feature AC | Original coverage |
|---|---|---|
| F-AC1 | Eligible matching selected-counterparty cashflows, including supported source/payment combinations, complete processing on the agreed schedule and within the approved grouping boundary. Original flows become Netted; a Swap Agent Netting resultant is generated; that resultant becomes SWIFT_SUPPRESSED; and its accounting entry is generated and sent to EBBS. | 1–5, 11 |
| F-AC2 | Eligible Coupon flows outside the selected counterparty list complete the SAL Coupon route: eligible flows are classified, matching flows net, originals become Netted, a SAL Coupon Netting resultant is generated, and the resultant undergoes suppression and accounting generation/send. | 6–7, 11 |
| F-AC3 | Eligible MTM/amortization-exchange flows outside the selected list complete the corresponding route with a SAL MTM Netting resultant and the specified downstream suppression/accounting behavior. | 8–9, 11 |
| F-AC4 | Other applicable payment types outside the selected list follow the explicitly approved WAITING/Pending Exception versus READY decision rule. This criterion is not acceptance-ready until that decision rule is supplied. | 10 |
| F-AC5 | For each of the three named netting routes, an eligible flow without a matching partner is not netted and the original flow becomes SWIFT_SUPPRESSED. Accounting behavior for this path remains to be confirmed. | 12 |

For F-AC1, a Given–When–Then version is:

> Given matching cashflows meeting the approved selected-counterparty eligibility rule, when RATAN evaluates them and the scheduled processing runs, then the original flows become Netted, the correctly grouped Swap Agent Netting resultant becomes SWIFT_SUPPRESSED, and the required accounting entry is generated and sent to EBBS, under the approved schedule and netting-key rules.

This retains start, outcome, and constraints. Keeping only “cashflows received → accounting sent” would omit evidence of the correct grouping, route, object statuses, and resultant payment type.

## Proposed Stories and ownership of all 12 original criteria

| Story | Draft outcome statement | Detailed coverage |
|---|---|---|
| S1: Selected-counterparty route | As a settlement operations user, I want eligible selected-counterparty cashflows automatically processed through the Swap Agent route so that the specified netting and accounting outcome is produced. | 1–5; shared downstream rule 11 |
| S2: SAL Coupon route | As a settlement operations user, I want eligible Coupon flows outside the selected list processed through the SAL Coupon route. | 6–7; shared downstream rule 11 |
| S3: SAL MTM route | As a settlement operations user, I want eligible MTM/amortization-exchange flows outside the selected list processed through the SAL MTM route. | 8–9; shared downstream rule 11 |
| S4: Other payment types | As a settlement operations user, I want remaining applicable payment types placed into a deterministic approved state. | 10; currently incomplete |
| S5: Unmatched flows | As a settlement operations user, I want eligible flows with no matching partner handled explicitly instead of remaining in pending netting indefinitely. | 12; accounting behavior unresolved |

Item 11 is one shared requirement referenced by S1–S3, not three independently maintained copies and not automatically a separate Story. One Story can own the first implementation with dependencies for the other routes. A separate shared-behavior Story is also reasonable if its scope warrants independent delivery. Record ownership explicitly. S5's applicability to accounting must be resolved before extending item 11 to that path.

### Detailed draft ACs for S1

| ID | Draft acceptance criterion | Original |
|---|---|---|
| S1-AC1 | Given a cashflow satisfying the approved eligibility expression and selected counterparty list, when RATAN evaluates its netting route, then its sub-status type becomes Pending Auto Netting and it is tagged to Swap Agent Netting. | 1 |
| S1-AC2 | Given eligible pending/tagged flows, when the scheduled processing runs, then the applicable flows are processed at the approved VD 01:00 GMT schedule. Confirm what VD means, timing tolerance, late arrivals, and missed runs before finalizing. | 2 |
| S1-AC3 | Given eligible flows, when a netting group is formed, then grouping uses Booking entity + counterparty + currency + value date. Matching flows from supported sources/payment types may be grouped together; flows with different key components remain separate. Supported combinations and the separate-group interpretation require explicit approval. | 3, 5 |
| S1-AC4 | Given a valid matching group, when netting completes, then original flows become Netted and the generated resultant has payment type Swap Agent Netting. Expected amount/sign/rounding rules must be supplied for full verification. | 4 |
| S1-AC5 | Given that resultant, when the SWIFT suppression rule is evaluated, then the resultant becomes SWIFT_SUPPRESSED. | 11 |
| S1-AC6 | Given the resultant subject to item 11, when downstream accounting processing completes, then the required accounting entry is generated and sent to EBBS. Confirm trigger ordering and evidence of send; the screenshot does not require EBBS receipt or posting. | 11 |

Splitting item 11 into two checks improves failure diagnosis without creating two mandatory Stories. S1-AC3 also could be split if the team prefers separate grouping and source-compatibility rules. AC numbering is an aid, not an architectural constraint.

### Detailed coverage for the remaining Stories

| Story | AC subjects to specify |
|---|---|
| S2 | Exact Coupon eligibility and exclusions; Pending Auto Netting/SAL Coupon tagging; original Netted status and SAL Coupon Netting resultant; resultant suppression; accounting generation/send. Confirm grouping and schedule rather than assuming the S1 rules apply. |
| S3 | Exact MTM/amortization eligibility, parentheses and exclusions; Pending Auto Netting/SAL MTM tagging; original Netted status and SAL MTM Netting resultant; resultant suppression; accounting generation/send. Confirm grouping and schedule. |
| S4 | Exact fallback eligibility; explicit condition leading to WAITING/Pending Exception; explicit condition leading to READY; any required subsequent behavior. Do not write a test that accepts either state arbitrarily. |
| S5 | No matching eligible partner under the applicable route/key; no netting performed; original flow becomes SWIFT_SUPPRESSED; repeat for all three routes; explicitly resolve resultant/accounting behavior. |

Do not add arbitrary ACs merely to hit a numerical target. Each should describe a meaningful acceptance concern with a deterministic expected result.

## Rules to maintain once

| Shared artifact | BA content | QA use |
|---|---|---|
| Eligibility/precedence table | Exact AND/OR expressions; approved list; source/payment applicability; resolution of overlapping rules. | Positive/negative decision-table cases. |
| Grouping table | Key components, null rules, additional compatibility restrictions, route applicability. | Same-key positives and one-component-different negatives. |
| Schedule rule | VD definition, time zone, calendar, tolerance, late arrivals, reruns. | Boundary and scheduled-integration tests. |
| State/output table | Original flow versus resultant versus accounting entry; valid transitions and outputs for each route. | Assertions against the correct object. |
| Net amount/accounting specification | Calculation, sign, rounding, zero-net handling, accounting mapping, and send evidence. | Concrete expected results and downstream checks. |

Keep authoritative rule details in agreed work item content or versioned linked specification. Feature and Story ACs reference stable rule identifiers. A reference must lead to specific, reviewable content, not simply say “as per requirements.”

## Test design that is feasible for BA and QA

Use focused tests for combinations and boundaries, and a smaller risk-based set of journey tests for real connections. The exact count depends on the approved rule matrix, not on the count of ACs. Test automation can operate at an API, service, job, or interface level; this backend capability does not require browser automation for every check.

| Test family | Coverage | Execution approach |
|---|---|---|
| Routing | Product, strategy, agent-ID, counterparty inclusion/exclusion, overlapping routes. | Data-driven service/rule tests; representative integration checks. |
| Grouping | Same key; change each key component individually; mixed supported sources/payment types. | Focused grouping tests and representative netting integration. |
| Timing | Approved processing instant, tolerance, late-arrival and rerun policy. | Controlled-clock tests where possible plus evidence that the actual scheduler invokes the job correctly. |
| State and resultant | Pending/tagged originals, Netted originals, resultant payment type, suppressed resultant. | Service/integration tests with stable object identifiers. |
| Accounting | Correct entry content and send evidence for each resultant route. | Interface tests; downstream integration evidence at the agreed environment boundary. |
| Unmatched flow | Each route without a partner; no netting; suppressed original; clarified accounting. | Focused exception cases plus representative integration. |
| Full route | S1, S2, and S3 from ingestion to suppression/accounting; additional high-risk exceptions. | A manageable set of end-to-end cases. They do not replace detailed rule tests. |

A manually triggered job verifies job behavior, not actual scheduling. A stubbed EBBS verifies an agreed interface contract, not live EBBS integration. Record these boundaries on results. An end-to-end test can start at cashflow ingestion and finish at verified accounting send if that is the accepted Feature boundary; EBBS posting would extend that boundary and needs an explicit requirement.

### Example test: selected-counterparty route

Purpose: verify F-AC1 and S1-AC1–6 on one representative approved data set. Create at least two compatible, eligible flows with a shared key and record unique identifiers. Use approved sources/payment types; expected net amount and accounting content require the missing calculation/mapping specification. A separate mixed-source case verifies item 5 if this data set does not cover it.

| Step | Action | Expected result/evidence |
|---|---|---|
| 1 | Ingest the prepared flows into RATAN and allow classification to run. | Original IDs are traceable; each has Pending Auto Netting sub-status and the Swap Agent Netting tag. |
| 2 | Allow the actual scheduled run at the approved time, or trigger the job for the separate functional case. | Invocation and processing timestamps meet the case's stated purpose. Manual execution alone does not pass the scheduling criterion. |
| 3 | Inspect group membership and the produced result. | Only the intended compatible group participates; original flows are Netted; the resultant payment type is Swap Agent Netting; amount follows the approved specification. |
| 4 | Inspect the resultant after suppression evaluation. | The resultant, not merely the originals, is SWIFT_SUPPRESSED. |
| 5 | Inspect the accounting output and send evidence. | Expected accounting entry is generated and sent to EBBS, correlated to this result. Receipt/posting is required only if separately specified. |

These rows are test steps. S1-AC1–6 remain meaningful acceptance conditions even if one test case checks several of them. Additional tests should isolate failures such as a key mismatch or an ineligible counterparty without repeating the entire journey for every combination.

## Traceability and Azure DevOps usage

Use parent/child links for Feature → Stories → Tasks. Keep Feature ACs on the Feature and detailed Story ACs on Stories. Link Test Cases to applicable requirement work items using supported requirement/test relationships or requirement-based suites. Do not create ACs or tests as child Tasks merely to force a single tree.

Microsoft documents requirement-based suites automatically linking cases to backlog requirements. Stable AC IDs and a coverage matrix add finer traceability inside those requirements; that finer mapping is a proposed team practice rather than automatic per-AC tracking. [Microsoft: Test Case linking](https://learn.microsoft.com/en-us/azure/devops/test/create-test-cases?view=azure-devops). Accessed 2026-10-22.

Example coverage:

| Original | Authoritative detailed home | Feature summary | QA evidence |
|---|---|---|---|
| 1 | S1-AC1 | F-AC1 | Eligibility matrix + full-route case |
| 2 | S1-AC2 | F-AC1 | Scheduler/timing case + job processing case |
| 3 | S1-AC3 | F-AC1 | Key matrix + route integration |
| 4 | S1-AC4 | F-AC1 | Original/resultant state and amount checks |
| 5 | S1-AC3 or a separate source-compatibility AC | F-AC1 | Supported mixed-source/payment cases |
| 6 | S2 routing AC | F-AC2 | Coupon eligibility matrix |
| 7 | S2 result AC | F-AC2 | Coupon netting integration |
| 8 | S3 routing AC | F-AC3 | MTM eligibility matrix |
| 9 | S3 result AC | F-AC3 | MTM netting integration |
| 10 | S4 decision ACs | F-AC4 | Pending clarification before final cases |
| 11 | Shared suppression/accounting rule referenced by S1–S3 | F-AC1–3 | Parameterized route checks + downstream integration |
| 12 | S5 unmatched-flow ACs | F-AC5 | No-partner cases for each route |

## BA and QA collaboration

BA defines the business boundary, approved rules, statuses, calculations, and acceptance conditions. QA challenges ambiguity early, selects test data, determines focused/integration/journey coverage, and identifies evidence access. Both agree the actual test boundary, clock/data/environment constraints, and acceptance evidence before delivery.

Avoid maintaining three separate copies of the same eligibility expression in Feature ACs, Story ACs, and test scripts. Maintain the business expression once and use concrete examples and references in tests. The Feature remains understandable on its own through concise outcome statements and named constraints.

For backend behavior, observable does not mean visible on a UI. A defined status, emitted resultant, or accounting message can be acceptance evidence when exposed at an agreed system boundary. A particular private table or helper method should not become the requirement unless the contract explicitly depends on it. Cucumber recommends expressing scenarios as business-rule examples with context, event, and observable outcome. [Cucumber: Gherkin reference](https://cucumber.io/docs/gherkin/reference/). Accessed 2026-10-22.

## Questions needed to make the screenshot acceptance-ready

| Question | Why it matters |
|---|---|
| What are the exact parentheses and route precedence in items 1, 6, 8, and 10? | Overlapping or misread expressions can route identical data differently. |
| What determines WAITING/Pending Exception versus READY in item 10? | “Or” does not define a deterministic expected state. |
| What does VD mean, and what are the exact schedule/tolerance/calendar rules? Does the timing apply to SAL routes? | A processing-time test cannot be specified reliably without them. |
| Does the four-part key apply to SAL routes too? Are there other grouping restrictions? | Items 3 and 5 do not fully define compatibility for all routes. |
| What are expected net amount, sign, rounding, zero-net, and accounting mapping rules? | Status-only checks cannot establish a correct netting/accounting result. |
| For item 12, is a resultant created or an accounting entry generated/sent? | Item 11 concerns resultants; item 12 concerns an unnetted original flow. Do not assume the same downstream behavior. |
| Does “sent to EBBS” require transport evidence, acknowledgement, or posting? | These are different acceptance boundaries. |
| What behavior is required on late arrivals, retries, or downstream failures, if in scope? | Needed to choose exception coverage; proposed questions, not new requirements. |

The screenshot is sufficient to propose structure, but not to approve these unresolved expected results. Preserve all 12 source criteria and their references while resolving them.
