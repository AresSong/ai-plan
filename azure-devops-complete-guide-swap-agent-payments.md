# Connected guide: Features, Stories, acceptance criteria, and test cases

Updated: 2026-10-23. Working example: Feature 16968945, Swap Agent Payment Enhancement, from the supplied screenshot. This guide replaces the earlier illustrative examples with this example. No Azure DevOps work items have been changed.

## Read this first

A Feature defines a valuable capability. Stories deliver specific outcomes within it. Acceptance criteria (ACs) state the conditions for accepting either. Test cases demonstrate whether those conditions hold; test steps specify actions and checks during execution. Tasks describe implementation work.

Do not turn this into a rule that Feature ACs are end-to-end and Story ACs are each processing step. End-to-end describes test scope. Feature versus Story describes requirement and delivery scope. A Story can span receipt, classification, netting, suppression, and accounting when that forms a small enough business outcome.

Microsoft documents Features containing smaller backlog items, Stories mapped to Features, and Tasks supporting Stories. It also documents Test Cases linked to requirements, with Action and Expected Result fields for individual steps. AC identifiers and the decomposition below are recommended team conventions, not extra mandatory Azure DevOps hierarchy levels. [Microsoft: Features](https://learn.microsoft.com/en-us/azure/devops/boards/backlogs/define-features-epics?view=azure-devops); [Microsoft: Agile workflow](https://learn.microsoft.com/en-us/azure/devops/boards/work-items/guidance/agile-process-workflow?view=azure-devops); [Microsoft: Test Cases](https://learn.microsoft.com/en-us/azure/devops/test/create-test-cases?view=azure-devops). Accessed 2026-10-22.

## Two starting points, one connected structure

This guide covers both reorganizing the current detailed requirements and developing future requirements from Feature outcomes. The workflows below are recommended BA/QA practices. Both lead to the same structure: current Feature ACs F-AC1–5, contributing Stories with detailed behavior ACs, shared rules, and mapped tests.

| Starting point | Current example: reorganize existing detail | Future work: develop requirements progressively |
|---|---|---|
| Available input | The screenshot's 12 detailed ACs, mixing routes, rules, and exceptions. | A business need, proposed capability, and whatever rules or constraints are already known. |
| First BA activity | Identify the complete outcomes behind the existing rules. | Define capability scope and outcome-level Feature ACs; capture known detail alongside them. |
| Story refinement | Allocate existing detail to meaningful Stories and fill gaps. | Discover and refine detailed conditions with QA and developers as Stories become ready. |
| Traceability | Preserve original items as legacy source references; use F-AC1–5 for active acceptance tracking. | Link Stories directly to current Feature ACs from the start; no legacy numbering is necessary. |
| QA involvement | Check that no original rule disappears, then design focused and complete-route coverage. | Challenge ambiguity and propose examples early, then refine executable cases alongside Stories. |

These are starting points, not rigid phases. Examples can change the Feature boundary; Story refinement can reveal a missing Feature outcome. Update the linked artifacts together. Do not wait until Story development is complete to involve QA.

## Path A — Current example: pivot from the 12 detailed ACs

The original detail is useful input. Reorganization makes its delivery scope and acceptance relationships explicit; it does not discard the original rules.

| Action | Application to the screenshot | Result |
|---|---|---|
| 1. Identify outcome routes. | Separate selected-counterparty processing, Coupon processing, MTM processing, fallback, and no-partner handling. | Five named acceptance outcomes rather than one sequence of 12 steps. |
| 2. Write combined Feature ACs. | Combine items 1–5 and 11 into F-AC1; 6–7 and 11 into F-AC2; 8–9 and 11 into F-AC3; map 10 to F-AC4 and 12 to F-AC5. | The current proposed Feature ACs defined later in this guide. |
| 3. Propose meaningful Stories. | Use candidate Stories S1–S5 for the five outcomes, subject to sizing and dependencies. | Delivery slices that reference F-AC1–5. |
| 4. Allocate detailed behavior. | Put selected-counterparty classification, timing, grouping, netting, suppression, and accounting into S1-AC1–6. Reference shared rules from the other routes. | Detailed Story ACs without maintaining copies of the same rule. |
| 5. Resolve gaps with QA and developers. | Clarify WAITING versus READY, schedule meaning, grouping restrictions, and no-partner accounting behavior. | Deterministic expected results where resolved; explicit open questions elsewhere. |
| 6. Map verification. | Use focused decision/grouping/state cases and selected full-route cases. | Evidence for both detailed Story behavior and complete Feature outcomes. |

Worked chain:

```text
Legacy screenshot items 1–5 and 11
  → F-AC1: complete selected-counterparty processing outcome
    → S1: process eligible selected-counterparty cashflows
      → S1-AC1–6: detailed acceptance conditions
        → focused cases and a representative full-route case
```

The legacy numbers show provenance only. The active relationship is F-AC1 → S1-ACs → test evidence. The detailed tables later in this guide show that relationship and preserve all 12 source items.

## Path B — Future work: start from Feature outcomes and capture known detail

For a new capability, BA normally starts with purpose, scope, major outcomes, and Feature ACs. This does not restrict BA to high-level wording. Capture an exact grouping rule, timing constraint, interface requirement, or exception as soon as it is known. Some detail remains a Feature-wide constraint; some becomes a shared rule or a specific Story AC.

### Example initial Feature brief

Using the same Swap Agent capability as a hypothetical new request:

| Feature content | Example initial entry |
|---|---|
| Purpose | Automate the specified cashflow routes and their downstream treatment. |
| Outcome ACs | F-AC1 selected-counterparty processing; F-AC2 Coupon processing; F-AC3 MTM processing; F-AC4 fallback; F-AC5 unmatched-flow handling, as defined below. |
| Known detail | Record the four-part netting key immediately; retain the candidate eligibility expression and VD 01:00 GMT timing requirement with their confirmation status. |
| Shared rules | Maintain eligibility, precedence, grouping, schedule, and status/output rules once, with stable references. |
| Open questions | What selects WAITING versus READY? What happens to accounting for unmatched flows? Does the same key/schedule apply to SAL routes? |
| Acceptance boundary | Specify whether the required downstream outcome is accounting sent, acknowledged, or posted. Do not silently extend it. |

The table illustrates how to record known information; it does not resolve the screenshot's business-rule questions. If the five outcomes are not yet known in an actual new request, discover them through refinement rather than filling a template with invented requirements.

### Refine the Feature into Stories and evidence

| Activity | BA contribution | QA/developer contribution | Result |
|---|---|---|---|
| Explore the Feature. | Describe business scope, outcomes, known rules, and unknowns. | Challenge examples, dependencies, system boundaries, and observability. | Initial Feature brief and outcome ACs. |
| Prepare a Story for implementation. | Define its specific outcome, detailed behavior ACs, exclusions, and rule references. | Check feasibility, size, decision combinations, failure cases, and testability. | A Story with clear acceptance conditions and visible dependencies. |
| Prepare executable verification. | Clarify expected business results and representative data. | Define cases, concrete inputs, steps/assertions, environments, and evidence access. | Tests mapped to Story ACs and Feature outcomes. |
| Verify and accept. | Assess the agreed outcomes with the product/business decision-maker. | Produce focused, integration, and journey evidence at the stated boundaries. | Story acceptance and Feature acceptance assessed at their respective scopes. |

For example, BA may know the grouping key before S1 exists. Record it once in the grouping specification. During S1 refinement, write S1-AC3 describing the grouping behavior and reference that specification. QA then selects same-key and different-key examples. There is no need to postpone the rule, copy it into multiple places, or convert each test action into an AC.

### Future Story template

```text
Parent Feature: [work item link]
Contributes to Feature AC: F-AC1
Story outcome: Process eligible selected-counterparty cashflows.
Acceptance boundary: [agreed beginning/end of this Story's responsibility]
Known/shared rules: [specific rule IDs and links]

Detailed Story ACs:
  S1-AC1: Classification behavior.
  S1-AC2: Approved processing schedule.
  S1-AC3: Grouping and compatibility behavior.
  S1-AC4: Netting output behavior.
  S1-AC5: Resultant suppression behavior.
  S1-AC6: Accounting generation/send behavior.

Verification: [focused cases plus relevant route evidence]
Open questions/dependencies: [resolve acceptance-critical ambiguity before implementation]
```

These are detailed behavior ACs, not necessarily step-level ACs. A Story may cover several processing stages, and its final scope must be small enough to deliver and verify. Known details are welcome at Feature discovery; the team's obligation is to give each rule a clear home and refine acceptance-critical gaps before implementing the affected behavior.

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

The following combined criteria are the current proposed Feature ACs and the primary references for Stories and test coverage. They summarize the outcome and retain critical constraints. The screenshot's original items 1–12 are source references only, not the current Feature AC identifiers. Their historical mapping is retained below so no source requirement is lost. The structure is adopted for this guide; unresolved business wording remains a draft.

| Current ID | Draft Feature AC | Legacy screenshot items (source only) |
|---|---|---|
| F-AC1 | Eligible matching selected-counterparty cashflows, including supported source/payment combinations, complete processing on the agreed schedule and within the approved grouping boundary. Original flows become Netted; a Swap Agent Netting resultant is generated; that resultant becomes SWIFT_SUPPRESSED; and its accounting entry is generated and sent to EBBS. | 1–5, 11 |
| F-AC2 | Eligible Coupon flows outside the selected counterparty list complete the SAL Coupon route: eligible flows are classified, matching flows net, originals become Netted, a SAL Coupon Netting resultant is generated, and the resultant undergoes suppression and accounting generation/send. | 6–7, 11 |
| F-AC3 | Eligible MTM/amortization-exchange flows outside the selected list complete the corresponding route with a SAL MTM Netting resultant and the specified downstream suppression/accounting behavior. | 8–9, 11 |
| F-AC4 | Other applicable payment types outside the selected list follow the explicitly approved WAITING/Pending Exception versus READY decision rule. This criterion is not acceptance-ready until that decision rule is supplied. | 10 |
| F-AC5 | For each of the three named netting routes, an eligible flow without a matching partner is not netted and the original flow becomes SWIFT_SUPPRESSED. Accounting behavior for this path remains to be confirmed. | 12 |

For F-AC1, a Given–When–Then version is:

> Given matching cashflows meeting the approved selected-counterparty eligibility rule, when RATAN evaluates them and the scheduled processing runs, then the original flows become Netted, the correctly grouped Swap Agent Netting resultant becomes SWIFT_SUPPRESSED, and the required accounting entry is generated and sent to EBBS, under the approved schedule and netting-key rules.

This retains start, outcome, and constraints. Keeping only “cashflows received → accounting sent” would omit evidence of the correct grouping, route, object statuses, and resultant payment type.

## Proposed Stories mapped to the combined Feature ACs

| Story | Draft outcome statement | Contributes to current Feature AC |
|---|---|---|
| S1: Selected-counterparty route | As a settlement operations user, I want eligible selected-counterparty cashflows automatically processed through the Swap Agent route so that the specified netting and accounting outcome is produced. | F-AC1 |
| S2: SAL Coupon route | As a settlement operations user, I want eligible Coupon flows outside the selected list processed through the SAL Coupon route. | F-AC2 |
| S3: SAL MTM route | As a settlement operations user, I want eligible MTM/amortization-exchange flows outside the selected list processed through the SAL MTM route. | F-AC3 |
| S4: Other payment types | As a settlement operations user, I want remaining applicable payment types placed into a deterministic approved state. | F-AC4; decision rule currently incomplete |
| S5: Unmatched flows | As a settlement operations user, I want eligible flows with no matching partner handled explicitly instead of remaining in pending netting indefinitely. | F-AC5; accounting behavior unresolved |

Item 11 is one shared requirement referenced by S1–S3, not three independently maintained copies and not automatically a separate Story. One Story can own the first implementation with dependencies for the other routes. A separate shared-behavior Story is also reasonable if its scope warrants independent delivery. Record ownership explicitly. S5's applicability to accounting must be resolved before extending item 11 to that path.

### Detailed draft ACs for S1

**Contributes to Feature AC:** F-AC1 — reference Feature 16968945 and its stable AC ID in the Story's Description or a separate traceability section. This is relationship information, not an additional Story AC. In the proposed S1 scope, the Story covers the selected-counterparty route; it does not cover the SAL routes, fallback behavior, or unmatched-flow handling.

| ID | Draft acceptance criterion | Contributes to | Legacy source only |
|---|---|---|---|
| S1-AC1 | Given a cashflow satisfying the approved eligibility expression and selected counterparty list, when RATAN evaluates its netting route, then its sub-status type becomes Pending Auto Netting and it is tagged to Swap Agent Netting. | F-AC1: eligibility and classification | 1 |
| S1-AC2 | Given eligible pending/tagged flows, when the scheduled processing runs, then the applicable flows are processed at the approved VD 01:00 GMT schedule. Confirm what VD means, timing tolerance, late arrivals, and missed runs before finalizing. | F-AC1: timing | 2 |
| S1-AC3 | Given eligible flows, when a netting group is formed, then grouping uses Booking entity + counterparty + currency + value date. Matching flows from supported sources/payment types may be grouped together; flows with different key components remain separate. Supported combinations and the separate-group interpretation require explicit approval. | F-AC1: grouping and compatibility | 3, 5 |
| S1-AC4 | Given a valid matching group, when netting completes, then original flows become Netted and the generated resultant has payment type Swap Agent Netting. Expected amount/sign/rounding rules must be supplied for full verification. | F-AC1: netting output | 4 |
| S1-AC5 | Given that resultant, when the SWIFT suppression rule is evaluated, then the resultant becomes SWIFT_SUPPRESSED. | F-AC1: resultant suppression | 11 |
| S1-AC6 | Given the Swap Agent Netting resultant covered by F-AC1, when downstream accounting processing completes, then the required accounting entry is generated and sent to EBBS. Confirm trigger ordering and evidence of send; the screenshot does not require EBBS receipt or posting. | F-AC1: accounting generation and send | 11 |

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

## Referencing Feature ACs from Stories

Story ACs elaborate the behaviors contributing to Feature acceptance; they need not be a mechanical decomposition of the Feature wording. Feature acceptance can also require evidence that multiple Stories operate together.

Use a separate “Contributes to Feature AC” section above the Story ACs. Reference the Feature work item and AC ID, state the Story's contribution, and then list the Story's own testable conditions. Do not paste the full Feature AC into each Story or count the reference itself as an AC.

Recommended template:

```text
Story: [specific user or operational outcome]
Parent Feature: [work item link]
Contributes to Feature AC: [stable AC ID]
Contribution: [the part of the outcome this Story delivers]
Acceptance boundary: [where this Story's responsibility ends]

Story ACs:
  [Story-AC1] [specific acceptance condition]
  [Story-AC2] [specific acceptance condition]

Shared rules: [stable rule IDs and links, where applicable]
Verification: [linked test cases or coverage matrix]
```

For S1, use “Contributes to F-AC1” followed by S1-AC1–6 above. If a Story contributes to several Feature ACs, use a small mapping rather than repeating those Feature criteria. For example, S5 contributes to F-AC5 across the three routes; that does not make it responsible for every condition in F-AC1–3.

| Situation | How to document it |
|---|---|
| One Feature AC summarizes several Story behaviors. | Reference it once above the Story ACs; specify this Story's detailed behavior below. |
| One Story contributes to multiple Feature ACs. | Map individual Story AC IDs to Feature AC IDs when a Story-level reference is insufficient. |
| Several Stories use an identical business rule. | Maintain the exact rule once, link it by stable ID, and specify which behavior each Story must demonstrate. |
| A Feature AC extends beyond the Story's scope. | State the partial contribution and acceptance boundary explicitly. Do not inherit the entire Feature acceptance obligation. |

For example, if S1 is later split into classification and downstream processing Stories, the classification Story can be accepted when its own agreed conditions pass. F-AC1 remains unaccepted until its complete outcome has sufficient evidence. Story closure does not automatically establish Feature acceptance. Conversely, one successful Feature journey does not prove every detailed Story rule.

When a Feature AC or shared rule changes, BA and QA review the mapped Story ACs and test cases for impact. References reduce repeated text; they do not remove the need to assess changed behavior. Keep IDs stable and update the authoritative wording and affected evidence.

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

### Acceptance scope versus test type

ACs define the conditions for accepting work. Test types describe verification scope or purpose. Feature ACs are not synonymous with system integration testing (SIT), and Story ACs are not limited to component tests. The following is a practical convention; teams may use SIT to include full journey tests.

| Test scope/purpose | Swap Agent example | Possible acceptance coverage |
|---|---|---|
| Component or service test | Exercise eligibility and grouping decisions with controlled inputs. | Detailed Story ACs and supporting evidence for Feature constraints. |
| System integration test | Verify the RATAN-to-EBBS accounting interface and processing across that connection. | Story or Feature ACs involving the interface. |
| End-to-end test | Exercise ingestion through classification, netting, suppression, and accounting send. | Complete-route Feature AC and several Story ACs. |
| Business acceptance/UAT | Operations validates representative routes and business results. | Feature and Story ACs within the agreed business acceptance scope. |

Successful message delivery alone does not establish correct grouping, net amount, or accounting content. Label each case with both its test scope and the ACs it verifies. This is recommended test planning practice, not an Azure DevOps enforcement rule.

### Useful overlap versus duplicate tests

Some coverage overlap is intentional: a focused grouping test establishes detailed rule behavior, while a full-route test establishes that correctly classified flows actually reach grouping and then downstream processing. They address different risks even when both check group membership.

| Situation | Recommended treatment |
|---|---|
| Focused grouping cases and a representative full-route case both inspect grouping. | Keep the overlap: detailed behavior and real connections need evidence. |
| The same data, setup, actions, assertions, and execution boundary are copied into “Feature” and “Story” cases. | Prefer one maintained test case mapped to both acceptance scopes. |
| Every eligibility combination repeats the full downstream route. | Prefer focused combination tests plus selected journey tests, unless assessed risk justifies broader full-route coverage. |
| One case supports several ACs. | Record which assertions support which ACs; do not treat an incidental check as complete coverage of every rule. |

Maintain one coverage matrix rather than two duplicated test inventories. The following test IDs are proposed examples, not existing Azure DevOps cases.

| Test case | Direct Story coverage | Feature contribution | Scope |
|---|---|---|---|
| TC01: Eligibility combinations | S1-AC1 | Supports the eligibility part of F-AC1. | Focused rule/service tests. |
| TC02: Grouping-key and supported-combination cases | S1-AC3 | Supports the grouping/compatibility part of F-AC1. | Focused grouping tests. |
| TC03: Actual scheduler invocation and timing | S1-AC2 | Supports the timing part of F-AC1. | Scheduler integration. |
| TC04: Complete selected-counterparty route | Representative scenarios across S1-AC1–6 | Direct journey evidence for F-AC1; not exhaustive rule coverage. | End-to-end at the agreed boundary. |
| TC05: Accounting interface and content variations | S1-AC6 and corresponding S2/S3 ACs where applicable | Supports accounting conditions in F-AC1–3. | Interface/integration tests. |

TC01 alone cannot establish F-AC1. TC04 passing cannot establish every eligibility combination covered by TC01. TC04 need not be cloned merely because it provides evidence for both Feature and Story acceptance. A failure requires identifying the affected assertions and assessing impacted ACs; it does not imply every mapped AC failed.

## Traceability and Azure DevOps usage

Use parent/child links for Feature → Stories → Tasks. Keep Feature ACs on the Feature and detailed Story ACs on Stories. Link Test Cases to applicable requirement work items using supported requirement/test relationships or requirement-based suites. Do not create ACs or tests as child Tasks merely to force a single tree.

Microsoft documents requirement-based suites automatically linking cases to backlog requirements. Stable AC IDs and a coverage matrix add finer traceability inside those requirements; that finer mapping is a proposed team practice rather than automatic per-AC tracking. [Microsoft: Test Case linking](https://learn.microsoft.com/en-us/azure/devops/test/create-test-cases?view=azure-devops). Accessed 2026-10-22.

### Current acceptance coverage: combined Feature AC → Story AC → tests

Use this view for delivery and acceptance tracking. A combined Feature AC can have several detailed checks and several tests; it is not accepted merely because one mapped check passes. S2–S5 subjects below remain draft outlines until their detailed ACs are agreed.

| Current Feature AC | Contributing Story acceptance | Focused evidence | Complete-outcome evidence |
|---|---|---|---|
| F-AC1: Selected-counterparty route | S1-AC1–6 | TC01 eligibility, TC02 grouping/compatibility, TC03 scheduling, TC05 accounting, plus output/suppression checks | TC04 representative selected-counterparty journey, supported by detailed coverage |
| F-AC2: SAL Coupon route | S2 classification, netting, resultant suppression, and accounting ACs | Coupon decision matrix and focused state/interface checks | SAL Coupon route journey; planned cases not yet assigned IDs |
| F-AC3: SAL MTM route | S3 classification, netting, resultant suppression, and accounting ACs | MTM decision matrix and focused state/interface checks | SAL MTM route journey; planned cases not yet assigned IDs |
| F-AC4: Other payment types | S4 deterministic fallback decision ACs | Decision-table cases once WAITING versus READY is defined | Representative fallback processing; acceptance blocked by missing business rule |
| F-AC5: Unmatched flows | S5 no-partner, no-netting, and original suppression ACs | No-partner cases across all three routes | Representative unmatched-flow processing; unresolved accounting behavior explicitly tracked |

For example, the coverage chain is F-AC1 → S1-AC3 → TC02 for detailed grouping rules, and F-AC1 → TC04 for the complete selected-counterparty journey. Do not use legacy screenshot item 3 as the current Feature AC reference. The shared suppression/accounting behavior contributes to F-AC1, F-AC2, and F-AC3; its original source item 11 does not remain a separate current F-AC11.

### Legacy source mapping: screenshot items 1–12

This table preserves provenance and verifies that the restructuring lost no original requirement. It is not a second active Feature AC list. Day-to-day Story and test references use F-AC1–5 and the relevant Story AC IDs.

| Legacy screenshot item | Detailed home | Current combined Feature AC | QA evidence |
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
