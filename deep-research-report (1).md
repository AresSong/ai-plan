# Lightweight Copilot Harness for React, Java, and PostgreSQL in VS Code

## Recommended direction

The best **initial** solution is not a heavy bespoke framework. It is a **layered harness** built mostly from features that already exist in GitHub Copilot and VS Code, then backed by deterministic checks in your repository and CI. In practical terms, that means:

- **Context harness** at the start of work: repository instructions, file-specific instructions, and reusable prompt files in `.github/`.
- **Verification harness** after code is generated: React tests, Java tests with Testcontainers against PostgreSQL, and database tests with pgTAP.
- **Enforcement harness** at pull request time: CodeQL, SonarQube quality gates, and optionally Semgrep plus branch rules / CODEOWNERS.

That combination fits your stack, aligns with what the VS Code and GitHub platforms already support, and avoids building an extension from scratch. It also matches what the recent research says matters most: repository context, explicit task prompts, executable tests, and deterministic validation around generated code. citeturn27view1turn26view0turn24view1turn24view3turn24view4turn24view10turn24view11turn24view7turn24view8

Your instinct about the examples is right:

- A **SonarQube check after a Copilot session** is **part of** a harness, but only as an **output validator**.
- A **mandatory context injection step at the start of the session** is also **part of** a harness, but on the **input side**.
- A **hook** is not the harness itself; it is one mechanism to automate harness behaviour at specific lifecycle events. citeturn24view2turn29view0turn24view4

The important design choice is to treat “harness” as a **control layer around Copilot**, not as one single tool. citeturn27view1turn19view3

## What counts as a harness here

For your use case, a Copilot development harness is best understood as a **repeatable control loop** around AI-assisted code generation:

1. **Inject the right context** before or during generation.
2. **Constrain how work is performed** when the task is agentic.
3. **Validate the output deterministically** before it reaches `main`. citeturn27view1turn24view2turn24view3turn24view4

This maps neatly onto the capabilities that VS Code now exposes. Custom instructions are designed to make AI responses match your coding practices and project requirements, and file-based instructions can target particular frameworks or folders. Prompt files turn common workflows into reusable slash commands. MCP can connect the model to tools, databases, and services. Hooks run your own commands automatically at lifecycle points in the agent loop. VS Code’s own documentation explicitly recommends adopting these capabilities incrementally: start with project-wide instructions, add targeted instructions, then add skills, agents, hooks, and external tools only where they earn their keep. citeturn26view0turn27view1turn25view3turn24view2

There is one crucial limitation to keep in mind. **Custom instructions do not apply to inline suggestions as you type in the editor.** They apply to chat and agent-style workflows. That means a serious harness cannot rely on “always-on instructions” alone; it also needs repository tests and PR gates, because developers can still accept inline completions that bypass those instruction files. citeturn26view0

So, in your environment, the harness should be split into three concrete layers:

### Context layer

Use `.github/copilot-instructions.md` for project-wide rules, then add `*.instructions.md` files for `frontend`, `backend`, and `database` paths. This is exactly what the VS Code model supports. It is also the lowest-friction way to approximate “mandatory context injection” without building custom tooling. citeturn26view0

### Workflow layer

Use prompt files for repeatable tasks such as “implement a full-stack feature”, “add a DB migration”, “generate tests”, or “review changed files”. Prompt files are explicitly intended for scaffolding common tasks, running and fixing tests, and standardising multi-step workflows. The official docs even include a React component example, which is directly relevant for your stack. citeturn24view1turn27view0

### Validation layer

Use deterministic, executable checks for each part of the stack, then enforce them in CI. That is where Testcontainers, pgTAP, CodeQL, SonarQube, and optionally Semgrep belong. SonarQube can fail the workflow on a red quality gate; CodeQL can scan Java/Kotlin and JavaScript/TypeScript; Semgrep can scan on pushes and pull requests; pgTAP was explicitly designed to emit TAP output for harvesting by a harness. citeturn24view3turn24view4turn24view5turn25view8turn25view9turn25view10

## What the research says

The academic picture is surprisingly consistent: AI code generation benefits from **better repository context and executable feedback**, but remains too variable and too error-prone to trust without a harness.

A major line of research shows that **repository-level context matters a lot**. Work on repository-level code completion found that LLMs often struggle to use long cross-file context effectively, even when relevant APIs and similar code are present; newer approaches such as CoLA are specifically designed to improve cross-file context use. Other work on API completion for unseen repositories found that adding global and local repository context mitigates hallucinations and improves API completion accuracy. In plain English: if Copilot does not get project- and stack-specific context, it is much more likely to guess. citeturn24view10turn24view11

A second line of research shows that **prompting details change outcomes a great deal**. An empirical study on GitHub Copilot generated 892 Java methods from semantically equivalent descriptions and found that rewording the description changed the generated recommendation in about **46%** of cases, with correctness shifting by up to **±28%**. This strongly supports using standardised prompt files rather than leaving every developer to improvise their own prompt wording. citeturn24view6

A third line of research shows that **generated code and tests still need deterministic checking**. One empirical evaluation of Copilot’s code suggestions found correctness varied notably by language, with first-suggestion correctness at **57% for Java** and **27% for JavaScript** in the study’s setup. Research on project-level unit test generation found that even strong frontier models often produce compilation and cascade errors in generated tests, and that self-fixing still lags behind human correction. That is a strong argument for keeping the test runner, compiler, and CI as the real authority. citeturn22view1turn20view1turn20view2

A fourth line of research shows that **security is a non-trivial risk**. The well-known IEEE study on Copilot security generated **1,689 programs** across **89 scenarios** and found roughly **40%** to be vulnerable in that evaluation. A later empirical study of Copilot-generated code in GitHub projects found a substantial rate of security weaknesses in real-world snippets as well. This is exactly why tools such as CodeQL and SonarQube belong in the harness rather than being treated as optional extras. citeturn24view7turn23search4

There is also a particularly relevant testing insight for your plan. A 2026 study on test syntax structure found that test placement can measurably affect AI code generation quality, with co-located or inline test signals leading to much stronger preservation and correctness. You do not need to copy that exact test style, but it strengthens the broader idea that **keeping concrete tests and examples close to code and prompts improves AI output**. citeturn24view9

Taken together, the evidence points to the same practical architecture: **standardise context, generate through reusable workflows, then execute deterministic checks**. citeturn24view6turn24view10turn24view11turn20view2turn24view7

## What industry already provides

You do **not** need to build the entire solution from nothing. The current platform already gives you most of the control surface.

GitHub Copilot and VS Code already support the core customisation primitives you need. Repository instructions and file-based instructions live in `.github/`, prompt files live in `.github/prompts`, agent skills can package instructions with scripts and resources, and MCP servers can surface tools and database resources to the model. The documentation also explicitly encourages an incremental rollout rather than a big-bang design. citeturn26view0turn24view1turn16view0turn25view3turn27view1

The most relevant out-of-the-box GitHub starting point is **`github/awesome-copilot`**, which collects community-contributed instructions, agents, skills, hooks, workflows, and plugins. It is not a full React/Java/PostgreSQL harness on its own, but it is the closest ready-made library of examples for the Copilot side of the problem. citeturn14view2

For the Java/PostgreSQL verification layer, the strongest ready-made building blocks are:

- **`testcontainers/testcontainers-java-spring-boot-quickstart`**, which shows a Spring Boot application tested with JUnit and Testcontainers against a real relational database. Even if your backend is not Spring Boot, the underlying pattern generalises because Testcontainers for Java is a general library for JUnit-based tests with lightweight, throwaway database containers. citeturn14view1turn28view3turn28view2
- **`opencastsoftware/pgtap-java`**, which is specifically designed to run pgTAP tests via JUnit 5 and Testcontainers. If your PostgreSQL logic matters beyond ORM-level CRUD, this repository is almost tailor-made for your harness. citeturn14view0turn25view6
- **pgTAP / pg_prove**, which are explicitly framed as a database unit testing system whose TAP output can be harvested by a test harness. That is one of the rare places where the word “harness” is literally built into the toolchain. citeturn25view8turn25view9

For CI and enforcement, the industrial path is straightforward:

- **CodeQL** is GitHub’s own code analysis engine and can be enabled quickly with default setup. It supports **Java/Kotlin** and **JavaScript/TypeScript**, which covers your backend and frontend. citeturn24view3turn15view2turn25view10
- **SonarQube** provides an official GitHub Action and an official quality gate check action that can fail the workflow when your gate is red. citeturn14view3turn24view4
- **Semgrep** supports GitHub Actions and is designed to run on push and pull request events, which makes it a sensible optional second SAST layer if your team wants broader policy scanning or custom rules. citeturn24view5
- GitHub’s own guardrail guidance for Copilot cloud agent recommends using rulesets, code scanning / code quality requirements, and `CODEOWNERS` protection for important Copilot and MCP configuration files. Even if you remain primarily VS Code-based, that governance advice still applies to the repository. citeturn18view0

On hooks, the industrial story is mature enough to use selectively, but not as your first move. GitHub documents repository-level hooks for **Copilot cloud agent** and **Copilot CLI**, stored in `.github/hooks/*.json`, with lifecycle events such as `sessionStart`, `userPromptSubmitted`, `preToolUse`, and `postToolUse`. Hooks can approve or deny tool use, enforce policies, and log results. At the same time, the docs warn that hooks run synchronously and should normally stay below five seconds. Meanwhile, Microsoft’s VS Code learning material positions hooks very clearly as an automation mechanism for agent sessions and currently frames the VS Code hook tutorial around **VS Code Insiders**. That makes hooks powerful, but still a **phase-two** choice for a mainstream team rollout. citeturn29view0turn8view0

## A lightweight solution for your stack

### The recommendation in one sentence

Build a **Copilot Harness Repository Layer** first, then a **Stack Verification Layer**, and only add editor/agent hooks once your team has stabilised the first two layers. citeturn27view1turn29view0

### The repository shape

If your codebase is split by area, keep the harness alongside it and version it with the application:

```text
repo-root/
  frontend/
  backend/
  database/
  docs/
    architecture.md
    api-contracts.md
    db-schema.md
  .github/
    copilot-instructions.md
    instructions/
      frontend/react.instructions.md
      backend/java.instructions.md
      database/postgres.instructions.md
      testing/test-policy.instructions.md
    prompts/
      implement-full-stack.prompt.md
      add-db-migration.prompt.md
      generate-tests.prompt.md
      review-changes.prompt.md
    workflows/
      ci.yml
      codeql.yml
      sonar.yml
```

This layout follows how VS Code discovers instructions and prompt files, and it makes the harness visible, reviewable, and version-controlled. If you are in a monorepo and developers often open a subfolder rather than the repository root, enable `chat.useCustomizationsInParentRepositories` so that root-level customisations are still discovered. citeturn26view0turn27view0turn1view4

### The context layer

Use `.github/copilot-instructions.md` for rules that are true everywhere:

```md
# Project-wide Copilot rules

- This repository contains a React frontend, a Java backend, and PostgreSQL database code.
- Prefer small, reviewable changes over broad rewrites.
- Never invent tables, columns, API fields, or event names; inspect the codebase and docs first.
- Link implementation choices back to `docs/architecture.md`, `docs/api-contracts.md`, and `docs/db-schema.md`.
- For behavioural changes, propose or update tests before finalising code.
- For React changes, update Vitest and React Testing Library tests.
- For Java service or repository changes, add or update JUnit 5 tests; use Testcontainers for database integration where relevant.
- For PostgreSQL functions, triggers, constraints, or migrations, add or update pgTAP tests.
- In every answer, list assumptions, files changed, commands to run, and remaining risks.
```

This is exactly the kind of project-wide, always-on guidance the feature is designed for: technology stack declarations, architectural patterns, security requirements, and documentation standards. citeturn26view0

Then add file-specific instruction files so the AI receives the right rules for the right folder:

```md
---
name: React rules
applyTo: "frontend/**/*.{ts,tsx,js,jsx}"
---
- Use functional React components.
- Preserve accessibility semantics and labels.
- Prefer user-observable tests over implementation-detail tests.
- Keep API shapes aligned with `docs/api-contracts.md`.
```

```md
---
name: Java rules
applyTo: "backend/**/*.java"
---
- Keep controller, service, and repository boundaries explicit.
- Avoid hidden database access in controllers.
- Prefer clear exception mapping and validation.
- For database behaviour, prefer integration tests with Testcontainers.
```

```md
---
name: PostgreSQL rules
applyTo: "database/**/*.sql"
---
- Follow migration-first changes; do not rewrite old migrations unless explicitly asked.
- Prefer explicit constraints and indexes.
- Add pgTAP coverage for schema, functions, triggers, and permissions where applicable.
- Keep SQL consistent with `docs/db-schema.md`.
```

The reason to split the files this way is not just tidiness. Research and tooling both support more precise, project-level context rather than generic prompting. citeturn24view10turn24view11turn26view0

### The workflow layer

Prompt files are the most practical way to make team behaviour consistent. Unlike instructions, they are invoked manually, which makes them ideal for deliberate workflows such as implementing a feature, creating a migration, or generating tests. The official prompt-file docs already demonstrate this pattern with a React component example. citeturn24view1turn27view0

A strong initial prompt file for your stack would look like this:

```md
---
name: implement-full-stack
description: Implement a small full-stack change with tests
agent: agent
tools: ["search/codebase", "vscode/askQuestions"]
---

Read these files before planning:
- [docs/architecture.md](../docs/architecture.md)
- [docs/api-contracts.md](../docs/api-contracts.md)
- [docs/db-schema.md](../docs/db-schema.md)

Task:
${input:taskDescription:Describe the feature or bug}

Requirements:
- Produce a short implementation plan first.
- Do not invent schema or API contracts.
- If database changes are needed, add a migration under `database/`.
- If frontend changes are needed, update React code in `frontend/`.
- If backend changes are needed, update Java code in `backend/`.
- Add or update tests:
  - React: Vitest + React Testing Library
  - Java: JUnit 5
  - DB/integration: Testcontainers and/or pgTAP where appropriate
- Return:
  - assumptions
  - files changed
  - test commands to run
  - remaining risks
```

That prompt is simple, but it already acts as a harness: it standardises planning, context loading, file boundaries, and test expectations. citeturn27view0turn24view8

### The verification layer

For the frontend, a sensible baseline is **Vitest + React Testing Library**. React Testing Library is explicitly designed to keep tests maintainable and focused on how software is actually used, while Vitest is a Vite-native test framework that also works outside Vite and is Jest-compatible. citeturn28view0turn28view1

For the Java backend and integration boundary, **Testcontainers** should be your default harness mechanism for database-integrated tests. Testcontainers for Java is explicitly intended for JUnit tests with lightweight, throwaway databases, and its PostgreSQL module is straightforward to use. The Spring Boot quickstart shows the pattern in a concrete GitHub repository. citeturn28view3turn28view2turn25view7

For database-native logic, **pgTAP** is the cleanest option. If you want the least friction and you are happy keeping DB tests close to Java/JUnit-based tooling, **`pgtap-java`** is a very good match because it already combines JUnit 5, Testcontainers, and pgTAP. If you prefer a more direct SQL-native route, run `pg_prove` separately in CI. citeturn25view8turn25view9turn25view6

### The enforcement layer

Enable **CodeQL default setup** first, because it is very quick and already covers the source languages you care about. Then add **SonarQube** if you want broader code-quality policy and a pass/fail quality gate. If your security team wants a second static-analysis layer or custom patterns, add **Semgrep** later rather than on day one. Protect the harness files themselves with `CODEOWNERS` so that `.github/copilot-instructions.md`, `.github/instructions/**`, and `.github/prompts/**` cannot silently drift. citeturn24view3turn24view4turn24view5turn18view0

### Where hooks fit

Hooks are worth adding **only after** the repository-layer harness is stable.

If you later adopt Copilot CLI or Copilot cloud agent, repository-level hooks in `.github/hooks/*.json` can automate highly specific things, such as:

- `sessionStart`: print the current branch, changed files, and linked architecture docs.
- `userPromptSubmitted`: log prompts or attach a reminder about required docs.
- `preToolUse`: block risky commands or deny direct edits outside `frontend/`, `backend/`, and `database/`.
- `postToolUse`: run fast formatters or tests on touched areas. citeturn29view0

That is useful, but it is not the first thing I would deploy, because the official docs warn that hooks block agent execution and should remain fast. Also, the current VS Code learning material around hooks is tied to Insiders. citeturn29view0turn8view0

### Optional MCP use

If you later want stronger DB or service context without constantly maintaining hand-written docs, MCP is the next step. VS Code documents MCP as a way to connect AI models to external tools, including databases, and to provide resources that can be attached as prompt context. For your stack, the most useful safe pattern would be a **read-only database resource** or a **schema/documentation resource**, not write access. citeturn25view3

## Implementation plan

### The first iteration

The initial rollout should be deliberately modest and should avoid hooks.

Use the first pass to create a **repeatable, visible team process**:

- Add `.github/copilot-instructions.md`.
- Add `react`, `java`, `postgres`, and `test-policy` instruction files under `.github/instructions/`.
- Add three prompt files: `implement-full-stack`, `generate-tests`, and `review-changes`.
- Add or confirm these executable checks:
  - `npm test` or `vitest run` for the React area
  - `mvn test` or `gradle test` for Java
  - Testcontainers-backed database integration tests
  - pgTAP tests for SQL-heavy changes
- Enable CodeQL default setup.
- Add SonarQube if you already have it; otherwise make it a second step.
- Protect `.github/` harness files with `CODEOWNERS`. citeturn27view1turn26view0turn24view3turn24view4turn18view0

This gives you the harness concept immediately, without adopting experimental editor features.

### The team rule set

To make the harness real, document a small working agreement for engineers:

For any non-trivial feature, bug fix, or refactor, the developer should start in Copilot Chat or Agent mode with one of the repository prompt files rather than free-form prompting. They should not accept important inline suggestions blindly, because inline suggestions do not inherit the instruction files. Every behaviour-changing change must come with updated tests, and every pull request must pass the repository checks. citeturn26view0turn24view1turn24view3turn24view4

That process sounds simple, but it is exactly what turns a set of tools into a harness.

### The second iteration

Once the first iteration works for a few weeks, add more stack-specific verification rather than more AI complexity.

For React, tighten expectations around accessibility, labels, and user-path tests using React Testing Library. For Java, increase the share of integration-relevant tests that use Testcontainers with PostgreSQL rather than mocking everything. For PostgreSQL, identify where logic lives in migrations, functions, or permissions and add pgTAP around those boundaries. That gives Copilot a stronger “test target” and gives humans better confidence when reviewing AI-generated changes. citeturn28view0turn28view3turn25view8turn24view9

If you have a Spring Boot backend, the Testcontainers quickstart repository is a practical seed project. If your Java stack is not Spring, borrow the Testcontainers and pgTAP patterns rather than the whole example application. citeturn25view7turn25view6

### The third iteration

Only in the third iteration should you add agent-specific automation:

- a **custom agent** for “full-stack feature implementer” or “security reviewer”;
- an **agent skill** that packages your test/lint/review workflow;
- **hooks** for session lifecycle automation if the team standardises on Copilot CLI, cloud agent, or VS Code Insiders;
- optional **MCP** for read-only schema or service resources. citeturn16view1turn16view0turn29view0turn25view3

At that point, you are no longer guessing which automations matter; you are encoding practices that already proved useful.

### The most important non-technical decision

Keep the harness files themselves under review and treat them like source code. GitHub’s own guardrail guidance recommends protecting important Copilot and MCP configuration files with `CODEOWNERS` and rulesets. That is not bureaucracy; it is how you stop prompt drift, hidden policy changes, and accidental weakening of the harness. citeturn18view0

## Drawio diagram

The XML below is a simple diagrams.net / draw.io diagram for the recommended architecture. Import it directly into draw.io.

```xml
<mxfile host="app.diagrams.net" modified="2026-06-30T00:00:00.000Z" agent="GPT-5.2 Thinking" version="27.0.5">
  <diagram id="copilot-harness" name="copilot-harness">
    <mxGraphModel dx="1240" dy="760" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1600" pageHeight="900" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>

        <mxCell id="dev" value="Developer&#xa;VS Code" style="rounded=1;whiteSpace=wrap;html=1;" vertex="1" parent="1">
          <mxGeometry x="40" y="340" width="150" height="60" as="geometry"/>
        </mxCell>

        <mxCell id="copilot" value="GitHub Copilot&#xa;Chat or Agent Mode" style="rounded=1;whiteSpace=wrap;html=1;" vertex="1" parent="1">
          <mxGeometry x="240" y="320" width="190" height="100" as="geometry"/>
        </mxCell>

        <mxCell id="repoctx" value="Repository harness files&#xa;.github/copilot-instructions.md&#xa;.github/instructions/*.instructions.md&#xa;.github/prompts/*.prompt.md" style="rounded=1;whiteSpace=wrap;html=1;" vertex="1" parent="1">
          <mxGeometry x="480" y="100" width="280" height="150" as="geometry"/>
        </mxCell>

        <mxCell id="mcp" value="Optional external context&#xa;Read-only MCP resources&#xa;Schema docs / API docs / DB metadata" style="rounded=1;whiteSpace=wrap;html=1;" vertex="1" parent="1">
          <mxGeometry x="480" y="300" width="280" height="90" as="geometry"/>
        </mxCell>

        <mxCell id="hooks" value="Optional lifecycle automation&#xa;Hooks / skills / custom agent&#xa;Session start, prompt submit, post tool use" style="rounded=1;whiteSpace=wrap;html=1;" vertex="1" parent="1">
          <mxGeometry x="480" y="440" width="280" height="100" as="geometry"/>
        </mxCell>

        <mxCell id="changes" value="Code changes&#xa;Frontend React&#xa;Backend Java&#xa;Database PostgreSQL" style="rounded=1;whiteSpace=wrap;html=1;" vertex="1" parent="1">
          <mxGeometry x="820" y="320" width="200" height="110" as="geometry"/>
        </mxCell>

        <mxCell id="localchecks" value="Local deterministic checks&#xa;Vitest + React Testing Library&#xa;JUnit 5 + Testcontainers&#xa;pgTAP / pg_prove" style="rounded=1;whiteSpace=wrap;html=1;" vertex="1" parent="1">
          <mxGeometry x="1080" y="150" width="280" height="120" as="geometry"/>
        </mxCell>

        <mxCell id="cigates" value="PR and CI enforcement&#xa;CodeQL&#xa;SonarQube quality gate&#xa;Optional Semgrep&#xa;Rulesets + CODEOWNERS" style="rounded=1;whiteSpace=wrap;html=1;" vertex="1" parent="1">
          <mxGeometry x="1080" y="360" width="280" height="140" as="geometry"/>
        </mxCell>

        <mxCell id="review" value="Human review&#xa;Approve and merge" style="rounded=1;whiteSpace=wrap;html=1;" vertex="1" parent="1">
          <mxGeometry x="1410" y="320" width="160" height="90" as="geometry"/>
        </mxCell>

        <mxCell id="e1" value="" style="endArrow=block;html=1;rounded=0;" edge="1" parent="1" source="dev" target="copilot">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <mxCell id="e2" value="" style="endArrow=block;html=1;rounded=0;" edge="1" parent="1" source="repoctx" target="copilot">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <mxCell id="e3" value="" style="endArrow=block;html=1;rounded=0;" edge="1" parent="1" source="mcp" target="copilot">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <mxCell id="e4" value="" style="endArrow=block;html=1;rounded=0;" edge="1" parent="1" source="hooks" target="copilot">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <mxCell id="e5" value="" style="endArrow=block;html=1;rounded=0;" edge="1" parent="1" source="copilot" target="changes">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <mxCell id="e6" value="" style="endArrow=block;html=1;rounded=0;" edge="1" parent="1" source="changes" target="localchecks">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <mxCell id="e7" value="" style="endArrow=block;html=1;rounded=0;" edge="1" parent="1" source="changes" target="cigates">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <mxCell id="e8" value="" style="endArrow=block;html=1;rounded=0;" edge="1" parent="1" source="localchecks" target="review">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <mxCell id="e9" value="" style="endArrow=block;html=1;rounded=0;" edge="1" parent="1" source="cigates" target="review">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

This diagram reflects the recommended architecture: repository-managed context first, deterministic validation second, optional hooks and MCP later, and human review at the end. That ordering is the simplest way to get a real harness into day-to-day use without over-engineering the first release. citeturn27view1turn26view0turn24view1turn28view3turn25view8turn24view3turn24view4