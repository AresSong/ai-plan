# Unified Domain Knowledge — Five-Week Delivery Plan

**Duration:** five calendar weeks  
**Team:** Song Han and Lu Shuai, each officially allocated 0.5 person-day per working day; Lu Shuai
is unavailable in weeks 2 and 3  
**Delivery shape:** three weeks of component development, one week of environment/VS Code integration,
one week of demo preparation and demonstration  
**Primary slice:** Netting domain + three Java 17 repositories + selected Confluence pages + selected
Azure DevOps (ADO) items  
**Development interface:** Visual Studio Code (VS Code) with GitHub Copilot  
**Test position:** component contract and smoke checks are required; generating a draft test case
from the Domain Knowledge Graph is a must-have; integrating existing test cases is optional

## Project storytelling narrative

Software changes create risk when teams review expected behavior, existing code and changed code
separately. This knowledge sits across ADO, Confluence, architecture designs, repositories, tests and
people. The separation can hide behavior gaps until testing or production.

The project connects these elements in an evidence-backed Domain Knowledge Graph:

```text
                       Expected behavior
                      /                 \
        implemented by                   implemented/preserved by
                    /                       \
          Existing code  <---- impacted by ----  Changed code
```

Missing, stale or conflicting relationships become review candidates. People validate the evidence
and approve the knowledge. Approved knowledge generates tests that QA can deploy and run. The PoC
proves this flow for the Netting domain; the project can later extend it to more sources and runtime
evidence.

## 1. Success criteria

By the end of week 5, the Netting gold slice must demonstrate that:

1. existing code is linked to the expected behavior it implements;
2. changed code is linked to the expected behavior it is intended to implement or preserve;
3. changed code is linked to the existing code and behavior it may impact;
4. missing, contradictory, ambiguous or unsupported relationships create reviewable gap candidates;
5. human decisions and evidence history are retained;
6. approved knowledge generates a QA-accepted test that runs from the deployed test pack; and
7. the complete flow runs from VS Code with GitHub Copilot and exports a reproducible approval pack.

## 2. Whole PoC plan at a glance

| Week | Phase and planned capacity | Components | Developer ownership | SME validation | Tangible showcase milestone | Exit gate / dependency |
|---|---|---|---|---|---|---|
| **1** | Independent sources and shared standard — **4.25 person-days** | Standard Knowledge Source Interface; Code Knowledge Graph; Confluence Knowledge Graph; ADO Knowledge Graph | TBD | Architect: code/ADO structure. BA: Confluence/ADO meaning. QA: positive, negative, ambiguous and changed-source cases | Run three independent source views and trace one item from each graph to exact source evidence | All knowledge sources run from fixtures; prioritize one live source only if access/tooling is already ready; leave handoff is complete |
| **2** | Unified knowledge layer — **2 person-days** | Domain Knowledge Graph; Knowledge Linker | TBD | Architect + BA validate canonical identities, predicates, provenance and ambiguity handling | Navigate an evidence-backed path from an ADO item to a Confluence behavior and Java entity | At least five expected links persist across restart; negatives do not link; ambiguity is not forced; depends on the frozen week-1 interface and fixtures |
| **3** | Governance and test generation — **2 person-days** | Knowledge Governance; Review Workbench; Test Case Generator | TBD | Architect/BA review linked meaning; QA validates the review flow and generated test case | Review a linked candidate, record a human decision, update the DKG and produce a QA-reviewable draft test | Human review and one-format test generation are mandatory; semantic enrichment and existing-test integration are deferred; depends on usable graph and linker results |
| **4** | Environment and VS Code integration — **4.25 person-days** | Development Environment Integration; VS Code + GitHub Copilot Integration; Test Pack Deployment; Approval-Pack Export | TBD | Architect + BA + QA validate the integrated flow; QA Lead supports test-pack deployment and execution | From VS Code with GitHub Copilot, ingest the gold slice, inspect linked evidence, decide an item, deploy/run the test pack and export the pack | Clean setup and test-pack execution work in the target environment; live/fixture state is explicit; depends on weeks 1–3 results |
| **5** | Demo and stop/go — **4.5 person-days** | Demo Workflow; Approval Pack; Fallback Package | TBD | BA validates story; QA signs demo checklist; architect records production gaps; sponsor owns stop/go | Deliver the live 15–20 minute end-to-end demo and reproducible approval pack | Two clean rehearsals including fallback mode; every conclusion resolves to evidence; no critical demo defects; depends on week-4 clean run |
| **Total** | **17 planned person-days + 3-day buffer** | Source Graphs → Domain Knowledge Graph → Knowledge Linker → Human Review → Test Generation → Test Pack Deployment → VS Code Integration → Demo | TBD | Approximately 9–10 SME-days + 1 QA Lead day + 1 DevOps day + 5 sponsor hours | One showcase every week, ending in a traceable Netting PoC | Existing-test integration, semantic linking, additional live sources and UI polish are optional and cannot rely on unofficial extra time |

## 3. Required resources

### Human resources

| Resource | Suggested commitment | Primary contribution |
|---|---:|---|
| Song Han | 12.5 gross person-days | Project owner; component ownership TBD |
| Lu Shuai | 7.5 gross person-days | Project owner; component ownership TBD; unavailable in weeks 2 and 3 |
| Architect SME | 2.5–3 days total | Contract, code/ADO graph, unified graph and architecture validation |
| BA SME | 3 days total | Confluence/ADO semantics, expected links and demo narrative |
| QA SME | 3.5–4 days total | Gold cases, human-review checks, candidate-test review and demo acceptance |
| QA Lead | 1 day total, to confirm | Help deploy and run the test pack containing the generated test case; retain execution evidence |
| DevOps | 1 day total | Provision PostgreSQL 16 + `pgvector` and the vLLM runtime; support deployment and database backup/restore |
| Sponsor/demo decision owner | 1 hour each week; 5 hours total | Weekly scope/milestone review and final stop/go decision |

SME validation should be booked before development starts: week-1 knowledge-source review, week-2 unified
graph review, week-3 QA review, week-4 test-pack deployment/acceptance and week-5 demo/sign-off. Book
the QA Lead for weeks 4–5 and the sponsor's one-hour review as a recurring weekly checkpoint.

### Compute and storage resources

- One PostgreSQL 16 instance with the `pgvector` extension enabled. Relational tables store the DKG;
  vector columns/indexes support semantic retrieval. Deployment may be local or shared, subject to
  the remaining PoC HA/scope decision.

- One vLLM inference instance serving an approved multimodal vision-language model with text-and-image
  input support. It reads rendered architecture diagrams and receives extracted HTML/SVG labels and
  structure as supporting text. GPU/VRAM capacity and model size are to be confirmed using one
  representative architecture-diagram benchmark.

- LLM token capacity: **to be calculated** from the three code repositories and selected Confluence
  pages using the formulas below. Measure one representative code chunk and one representative page
  first, then replace the averages with actual input/output usage. Reserve 30% contingency for prompt
  tuning, retries and demo rebuilds.

Token cost, once model rates are known:

```text
LLM_cost = (input_tokens / 1,000,000 × input_rate)
         + (output_tokens / 1,000,000 × output_rate)
```

Code-repository graph token formula:

```text
Code_input_tokens =
  passes × retry_factor ×
  [LOC_in_scope × avg_chars_per_LOC / chars_per_token × (1 + overlap_rate)
   + code_chunks × prompt_overhead_tokens]

Code_output_tokens =
  passes × retry_factor ×
  [graph_nodes_edges_emitted × avg_output_tokens_per_item]

Code_total_tokens = Code_input_tokens + Code_output_tokens
```

Apply the formula across all three repositories. Exclude generated code, vendored dependencies,
binaries and unchanged files outside the declared scope. `retry_factor = 1 + expected_retry_rate`.

Confluence/document graph token formula:

```text
Document_input_tokens =
  passes × retry_factor ×
  [document_chars_in_scope / chars_per_token × (1 + overlap_rate)
   + document_chunks × prompt_overhead_tokens]

Document_output_tokens =
  passes × retry_factor ×
  [(claims + entities + relationships) × avg_output_tokens_per_item]

Document_total_tokens = Document_input_tokens + Document_output_tokens
```

Measure `document_chars_in_scope` after removing navigation, repeated templates and unsupported
macro payloads, but before chunk overlap. Keep tables and headings when they carry business meaning.
Use version hashes to avoid recompiling unchanged pages.

Storage is part of this resource allocation. Size it as:

```text
Storage_total =
  (source_snapshots + source_graphs + DKG + embeddings + logs + artifacts)
  × retained_versions × backup_factor
```

Use `backup_factor = 2` for one working copy plus one backup. Allocate separate retention boundaries
for immutable source snapshots, source-specific graphs, PostgreSQL data, `pgvector` indexes, logs
and approval/demo artifacts.

## 4. Assumptions, constraints and open decisions

1. “ADO graph” means an Azure DevOps work-item/project graph, initially limited to a small set of
   epics, features, stories, links and source references.
2. Three Java repositories, 1–5 version-pinned Confluence pages and 10–30 ADO items form the gold
   demo slice. Sources and graph content are limited to the Netting domain.
3. Each available developer contributes 2.5 person-days per five-day week. Extra time is not included
   in committed capacity, milestones or dependencies.
4. Lu Shuai takes leave in weeks 2 and 3 and returns for weeks 4 and 5.
5. **Standard Knowledge Source Interface:** each knowledge source publishes knowledge in one
   normalized format. For code, Confluence and ADO this includes stable IDs, source versions, source
   status, immutable evidence references and graph proposals. Source-tool-native schemas remain private to their
   adapters. Whether the existing interface can be reused unchanged or needs a domain-specific
   amendment must be agreed and frozen in week 1.
6. **Agreed storage technology:** the Domain Knowledge Graph is persisted in PostgreSQL 16 with the
   `pgvector` extension. Domain nodes, edges, provenance, versions and governance state use relational
   tables; `pgvector` stores embeddings and supports vector similarity search. It is not the graph
   data model by itself.
7. **Open scope decision requiring agreement:** whether production HA, formal IAM and release
   approval are excluded from the PoC.
8. Source systems are read-only. Generated tests remain drafts and are not written to a codebase or
   executed automatically.
9. ADO is part of the required knowledge-source scope. If live ADO access slips, its interface and
   demonstration may use checked-in fixtures.
10. Existing-test integration and test-case generation are separate functions. Integration of existing
   test cases is outside the committed baseline and is the first scope cut. Generating at least one
   reviewable draft test case from approved domain-graph knowledge is mandatory.
11. With 17 planned person-days, knowledge-source deliverables are narrow interface-complete slices, not
   production-ready integrations. Fixture-backed capability is acceptable when live access or tooling
   would put the critical path at risk.
12. The current development interface is VS Code with GitHub Copilot.

## 5. Capacity and ownership

| Week | Song Han | Lu Shuai | Gross capacity | Planned capacity | Buffer |
|---|---|---|---:|---:|---:|
| 1 | 0.5 day/day | 0.5 day/day | 5 person-days | 4.25 | 0.75 |
| 2 | 0.5 day/day | Leave | 2.5 person-days | 2 | 0.5 |
| 3 | 0.5 day/day | Leave | 2.5 person-days | 2 | 0.5 |
| 4 | 0.5 day/day | 0.5 day/day | 5 person-days | 4.25 | 0.75 |
| 5 | 0.5 day/day | 0.5 day/day | 5 person-days | 4.5 | 0.5 |
| **Total** |  |  | **20 person-days** | **17** | **3 (15%)** |

One person-day means one full working day of effort. The official plan therefore assumes each
available developer contributes half a person-day per calendar workday. Any voluntary extra effort
may consume risk or optional scope but is not needed to claim a committed milestone.

Song Han and Lu Shuai are joint project owners. Component ownership remains TBD until they agree the
work split.

The leave creates a key-person risk. Before the end of week 1, Lu Shuai must leave runnable
fixtures, setup notes, a recorded walkthrough and no unshared credentials.

## 6. Week-by-week plan

### Week 1 — Independent source graphs and shared evidence contract

**Goal:** establish independently runnable code, Confluence and ADO source slices that publish the
same Standard Knowledge Source Interface.

| Workstream | Owner | Deliverable | Verification |
|---|---|---|---|
| Standard Knowledge Source Interface | TBD | Freeze identifiers, source versions, evidence references, source status and graph proposal schemas | Schema validation against positive, missing, stale and malformed fixtures |
| Code graph | TBD | Selected Java 17 repositories/change sets indexed to symbols, calls and source spans | Architect validates 10–30 representative entities and links |
| Confluence graph | TBD | Version-pinned page snapshots, claims/entities and exact spans | BA validates claims against the source pages |
| ADO graph | TBD | Narrow adapter or fixture path for work items, hierarchy, links and source references | BA/architect validates item semantics and traceability |
| Gold set | SMEs | True, false, ambiguous and changed-source examples | Signed-off expected-results file |

**Showcase milestone:** three separate source views run from the same manifest. A reviewer can open
one code entity, one document claim and one ADO item and resolve each back to exact source evidence.

**Exit gate:** knowledge sources do not need to be production-grade, but each must be independently
runnable from checked-in fixtures. Prioritize one live source path only when access and tooling are ready at
the start of the week; additional live paths are optional.

### Week 2 — Persistent DKG and first cross-source links

**Goal:** load selected domain anchors from all knowledge sources into the Domain Knowledge Graph and
prove the first evidence-backed
cross-source links.

| Workstream | Owner | Deliverable | Verification |
|---|---|---|---|
| Domain Knowledge Graph | TBD | PostgreSQL 16 relational nodes, edges, provenance, versions and bounded query API; `pgvector` embeddings support semantic retrieval | Code-only, document-only and ADO-only partitions survive restart; vector search returns expected gold candidates |
| Knowledge Linker | TBD | Deterministic tiers: explicit IDs/URLs, Java symbols, paths, ADO source links and governed aliases | Known positives link; known negatives do not |
| Unified ingest | TBD | Idempotent proposal path from each knowledge source into the Domain Knowledge Graph | Re-running the same manifest creates no duplicates |
| SME validation | Architect + BA | Review canonical identities, edge types and first unified subgraph | Ambiguity is retained instead of silently merged |

**Showcase milestone:** navigate a persistent unified subgraph from an ADO work item to a Confluence
behavior and then to Java evidence, with provenance on every edge.

**Exit gate:** at least five expected links are queryable; negative and ambiguous examples remain
honest; all detailed source data remains source-owned.

### Week 3 — Human review and mandatory candidate-test generation

**Goal:** turn linked candidates into governed knowledge and demonstrate the safe downstream test
boundary.

| Workstream | Owner | Deliverable | Verification |
|---|---|---|---|
| Knowledge Governance | TBD | Minimum immutable review packet, item decision, rationale and history path | Approve/qualify/reject/clarify actions are append-only and idempotent |
| Review Workbench | TBD | Minimum side-by-side evidence view and decision controls | Evidence-hash change blocks a stale decision |
| Test Case Generator — mandatory | TBD | One draft test-case format generated from current approved DKG knowledge, with model/template/evidence lineage | QA accepts it as reviewable or records correction; no existing-test import, repo write or execution |
| Semantic linker — stretch | TBD | Model-assisted candidates only after deterministic matching | Structured output rejects invented IDs/spans; ambiguity remains visible |

**Showcase milestone:** a human reviews one linked candidate, records a decision, sees the DKG status
update and generates a draft test case for QA review.

**Exit gate:** human review and one reviewable generated test case are mandatory. Existing-test
integration and semantic enrichment do not block week 4.

### Week 4 — Current development environment and VS Code integration

**Goal:** make the vertical slice reproducible in the team's actual development workflow.

| Workstream | Owner | Deliverable | Verification |
|---|---|---|---|
| Environment integration | TBD | Approved runtime/model configuration, secret injection, dependency pinning and local/shared profiles | Clean setup on a second developer machine |
| VS Code + GitHub Copilot workflow | TBD | VS Code tasks/run configurations and Copilot interaction for ingest, query, review and export | Cold developer completes the golden path from VS Code with GitHub Copilot |
| End-to-end integration | TBD | Knowledge-source orchestration, health/status handling and approval-pack export | Full manifest run succeeds; an absent source returns a useful partial result |
| Hardening | TBD | Fix integration defects; add required contract/smoke checks | Repeat run is idempotent; restart retains graph and decisions |
| Test-pack deployment and run | QA Lead + developer owner TBD | Deploy the test pack containing the QA-accepted generated test case; run it and retain execution evidence | Test command completes in the target environment and records pass/fail plus logs |
| SME acceptance | Architect + BA + QA + QA Lead | Integrated walkthrough and issue triage | Only demo-blocking findings enter week 5 |

**Showcase milestone:** from VS Code with GitHub Copilot, a developer starts the services, ingests the gold slice,
opens linked evidence, records a human decision, deploys/runs the test pack and exports the approval
pack.

**Exit gate:** no hidden database edits or developer-only steps; the generated test runs from the
deployed test pack with execution evidence; credentials stay outside source and artifacts; fixture/live
status is explicit.

### Week 5 — Demo readiness, evidence pack and final demonstration

**Goal:** deliver a repeatable, evidence-backed demonstration and an honest next-step decision.

| Workstream | Owner | Deliverable | Verification |
|---|---|---|---|
| Demo scenario | TBD + BA | 15–20 minute story: independent sources → unified domain graph → ambiguity → human decision → generated test → test-pack execution | BA confirms business narrative and terminology |
| Operational rehearsal | TBD | Setup script/runbook, resettable demo data, backup and fallback fixtures | Two clean rehearsals, including one fallback-mode run |
| Quality sign-off | QA + QA Lead | Demo checklist, known limitations, generated-test assessment and test-pack execution result | No unresolved critical demo defects; test-pack result is reproducible |
| Architecture sign-off | Architect | Contract/ownership/dependency review and scale-out recommendations | Stop/go and production gaps recorded |
| Final showcase | Song Han + Lu Shuai + SMEs | Live demo plus approval pack, metrics and next-step backlog | Audience can trace every showcased conclusion to evidence |

**Showcase milestone:** final live demonstration with a reproducible approval pack and a clearly
labelled live-versus-fixture capability matrix.

**Exit gate:** demo passes from a clean environment; fallback is rehearsed; limitations, token usage,
link-quality results and deferred production controls are documented.

## 7. Critical path and scope order

```text
shared contracts
  -> independent source adapters/fixtures
  -> persistent Domain Knowledge Graph
  -> candidate Knowledge Links
  -> Human Review
  -> mandatory draft Test Generation
  -> Test Pack Deployment and Execution
  -> environment/VS Code integration
  -> demo
```

Cut scope in this order if capacity is exceeded:

1. integration of existing test cases;
2. additional or advanced generated test-case formats, retaining one mandatory format;
3. semantic linking beyond the small gold slice;
4. live ADO access, retaining the ADO fixture contract;
5. UI polish, retaining the minimal review interaction.

Do not cut evidence provenance, ambiguity handling, human decision history, one reviewable generated
test case, repeatable setup or the required contract/smoke checks.

## 8. Required validation and minimum checks

The generated test case is a required PoC output. Integrating existing test cases is optional. These
checks are release gates for the PoC:

- interface/schema validation for every knowledge source;
- positive, negative and ambiguous linker fixtures;
- evidence reference resolution on every displayed edge;
- idempotent ingest and decision writes;
- persistence across process restart;
- stale evidence blocks or invalidates prior approval correctly;
- useful partial result when one knowledge source is absent;
- clean-environment VS Code + GitHub Copilot smoke run;
- QA-accepted generated test is included in the deployed test pack and produces retained execution
  evidence;
- approval-pack ID/hash consistency; and
- one approved DKG item produces a reviewable draft test case with source, model and template lineage.

## 9. Risks and mitigations

| Risk | Impact | Mitigation / owner |
|---|---|---|
| Lu Shuai's leave creates knowledge concentration | Week-2/3 blocker | Complete handoff, fixtures and credential map in week 1; agree the covering owner before leave |
| Both developers are allocated only 0.5 day/day | Context switching or unofficial overtime becomes an implicit dependency | Protect fixed focus blocks; use 17 planned person-days only; treat extra time as uncommitted |
| Three knowledge-source streams exceed two-person capacity | Weak or late adapters | Limit all sources to one gold slice; allow ADO fixture fallback; request a third engineer only if all three must be live |
| Source/API access arrives late | Cannot prove live integration | Make fixture execution a first-class capability; developers confirm access readiness before day 1 |
| Semantic linker creates false links | Loss of trust | Deterministic-first ladder, gold negatives, visible alternatives and mandatory review |
| LLM cost/latency spikes | Budget or demo failure | Hash-based cache, incremental rebuild, token caps and prebuilt demo snapshot |
| Test generation is mistaken for test coverage | Incorrect assurance | Label output as draft; coverage remains `UNKNOWN` without complete test inventory |
| Mandatory test generation competes with governance in a two-person-day week | Week-3 milestone slips | Support one test format and one approved gold item; defer semantic linking and all existing-test integration |
| `pgvector` is treated as the graph model | Graph traversal and provenance become awkward or incomplete | Model DKG nodes/edges relationally; use `pgvector` only for embedding similarity and candidate retrieval |
| Environment integration is deferred until week 4 | Late incompatibility | Run a thin environment spike in week 1; week 4 completes—not discovers—the integration path |
| Human review is mistaken for formal approval | Governance risk | Label it PoC/manual/non-release approval in UI and exports |

## 10. Decisions and inputs still needed

Confirm these before the staffed clock starts:

1. confirmation of Lu Shuai's exact leave dates;
2. exact Java repository/commit range, Confluence page IDs/versions and ADO project/item scope;
3. whether each knowledge source must be live for the final demo or whether ADO fixtures are acceptable;
4. operating system, CI/runtime and deployment constraints for VS Code and GitHub Copilot;
5. approved text/embedding model and multimodal vision-language model for vLLM, endpoint,
   architecture-diagram input formats, data-egress rule, GPU/VRAM requirement and spend/token cap;
6. whether the existing Standard Knowledge Source Interface can be reused unchanged or needs a
   domain-specific amendment;
7. PostgreSQL 16 provisioning location, credentials/backup owner, approved `pgvector` version,
   embedding dimensions and initial exact/HNSW index approach;
8. whether production HA, formal IAM and release approval are excluded from the PoC;
9. retention, confidentiality and redaction requirements for source snapshots and model prompts;
10. named architect, BA, QA, QA Lead, DevOps contact and final stop/go decision owner;
11. mandatory target test type/framework, test-pack deployment target, execution command and QA
    acceptance criteria for the generated test case; and
12. quantitative demo thresholds, especially expected linker precision on the gold set and maximum
    acceptable runtime/token consumption.
