# Rule Conflict Analysis — Implementation Plan

Build a small CSV analysis application alongside the existing rule engine: **Python + Lark + Z3 for analysis, and Cytoscape.js for visualization.**

The first version should let a business user upload rules, see overlapping or conflicting rules, and inspect an example input explaining each finding.

## Assumptions and scope

- Keep the existing engine and rule syntax.
- Initially support string fields, `==`, `!=`, `in`, `&&`, `||`, and parentheses.
- Analyze conditions against one input record. If actions change inputs and trigger other rules, that needs additional modeling.
- With only `user_rule`, report overlaps. Label actual conflicts only when action metadata and execution policy are available.
- Confirm precedence, case sensitivity, missing-value behavior, and execution policy before implementing the translator.

## 1. Define the input and expected behavior

Start with this CSV structure:

| Column | Required? | Purpose |
|---|---|---|
| `rule_id` | Yes | Stable identifier |
| `user_rule` | Yes | Condition expression |
| `action_target` | For conflict classification | Field or decision affected |
| `action_value` | For conflict classification | Value assigned |
| `priority` | If used by the engine | Execution order |

For the initial implementation, actions are constant assignments such as `decision = ALLOW`. More complex actions need an explicit compatibility definition.

Document whether the engine allows multiple matches, uses first match, or applies priority. Do not infer this from the rules.

**Verify:** Agree on a small fixture containing overlapping, disjoint, conflicting, and invalid rules, with expected results.

## 2. Parse rules with Lark

Write a grammar matching the supported syntax. Parse every expression into a structured tree while retaining its rule ID and original text.

For example:

```text
Product == "A" && Entity == "2"
```

becomes:

```text
AND
├── EQUALS(Product, "A")
└── EQUALS(Entity, "2")
```

Return syntax errors with the rule ID and error location. Unsupported operators must be marked as unanalyzed.

**Verify:** Check nested parentheses, AND/OR precedence, membership lists, escaped strings, and malformed expressions. Compare evaluations with the existing engine on representative inputs.

## 3. Translate parsed rules into Z3

Declare each field once as a typed Z3 variable. Translate the parsed operations:

```text
EQUALS      → equality
NOT_EQUALS  → inequality
IN          → OR of equalities
AND         → Z3 And
OR          → Z3 Or
```

Include known constraints on valid inputs, such as allowed product values. Explicitly model missing values if the engine permits them.

**Verify:** Ensure contradictory conditions such as `Product == "A" && Product == "B"` cannot match. Check that translated expressions agree with the engine’s behavior.

## 4. Analyze overlaps and classify findings

For each pair of rules, ask Z3 whether both conditions can hold for a valid record.

Produce a structured finding containing:

```text
Rule IDs
Finding type
Solver status
Example matching input
Actions and execution policy
```

Classify findings as:

- **Overlap:** both rules can match.
- **Conflict:** the overlap violates the execution policy or produces incompatible actions.
- **Unresolved:** unsupported syntax, solver timeout, or `unknown`.

Also identify individually impossible rules. Keep duplicate and shadowing analysis outside the first version unless needed.

Replay generated examples in the existing engine where possible.

**Verify:** Find all expected overlaps in the fixture, reject known disjoint pairs, and generate replayable examples. Never treat an unresolved check as “no conflict.”

## 5. Build the graph and evidence panel

Use a simple browser page with Cytoscape.js.

- Each node represents a rule.
- Each edge represents a verified relationship.
- Red edges indicate conflicts; amber edges indicate overlaps.
- Edge labels identify the relationship without relying only on color.

Clicking an edge displays both expressions, actions, execution policy, and the example input. Provide a findings table alongside the graph.

Default to showing rules involved in findings. Allow users to focus on one rule and its neighbors.

**Verify:** Every displayed edge maps to an analyzer finding, and clicking it shows the correct evidence.

## 6. Add the selected-rule tree view

Convert a selected rule’s parsed structure into an AND/OR tree. Label it clearly as the expression structure.

This is simpler than generating one global decision tree and preserves the original grouping.

**Verify:** The tree’s operators, values, and grouping match the parsed expression exactly.

## 7. Package and validate the application

Use one Python application to serve the analysis endpoint and static browser page. FastAPI is a reasonable choice; no database or agent framework is required initially.

Keep the implementation small:

```text
parser.py       — Lark grammar and parsing
analyzer.py     — Z3 translation and checks
app.py          — CSV upload and results endpoint
static/         — graph, findings table, evidence panel
tests/          — semantic fixtures and integration checks
```

Measure analysis time using a representative rule set. If necessary, add caching and safe candidate pruning based on proven disjoint conditions.

**Verify:** A user can upload a CSV, inspect findings, view matching examples, and see which rules could not be analyzed.

## Completion criteria

The first release is complete when the parser agrees with the existing engine, expected conflicts are detected with reproducible evidence, and users can investigate them through the graph.

Add LLM explanations only after that deterministic workflow is reliable.
