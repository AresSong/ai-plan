# Copilot Memory and Audit Architecture for a Web Development Team

## Bottom line

You do **not** need to build this entirely from scratch. The best near-term fit is to combine four things that already exist:

1. **VS Code’s built-in OpenTelemetry export for Copilot Chat / agent interactions** as the primary telemetry source for prompts, tool calls, token usage, edit outcomes, session counts, and agent traces. It can emit directly to OTLP, a JSONL file, or a local SQLite traces database; it also supports content capture when you explicitly enable it. citeturn20view0turn20view1  
2. **VS Code / Copilot hooks** for automatic labelling, governance checks, and extra audit records at `SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, and `Stop`. Hooks are automatic, deterministic, JSON-driven, and specifically intended for audit trails and policy enforcement. citeturn8view0turn11view3turn12view3  
3. **GitHub Copilot Usage Metrics APIs** plus the open-source **`github-copilot-resources/copilot-metrics-viewer`** for organisation-wide adoption, chat/agent usage, inline completion acceptance, language/model breakdowns, and long-term history beyond GitHub’s rolling API window. citeturn23view3turn31view1turn31view0turn27view3turn26search10  
4. **Azure DevOps service hooks / webhooks** to correlate Copilot sessions with repository outcomes in your actual delivery platform, such as pushes, pull requests, and build events. citeturn28search0turn28search3turn28search9

For your environment, the most practical initial architecture is:

**VS Code + Copilot → local loopback OTel Collector with durable queue → central Azure Monitor / Application Insights or self-hosted Langfuse → warehouse / dashboards**, with **GitHub usage metrics** and **Azure DevOps webhooks** flowing in as separate feeds. This keeps **tracking, local storage, and upload decoupled**, which matches your requirement. citeturn20view0turn37view0turn37view1turn37view2turn32search0turn32search5

## What the research and platform evidence imply

The academic and practitioner literature points in the same direction: if you only log “prompt sent” and “response returned”, you will miss the most useful signals. The key unit is the **execution trajectory**: prompts, retrieved context, tool use, edits, memory, intermediate actions, and outcomes. Recent AgentOps work explicitly argues that observability should trace the full lifecycle of agent artefacts, not just final outputs, because that is what supports debugging, governance, and improvement. A recent provenance survey similarly frames traces, tool-use provenance, memory lineage, and auditability as the accountability layer for trustworthy agent systems. citeturn14view0turn14view3

Research on Copilot-assisted development also suggests that **provenance and post-acceptance behaviour matter**. In a lab study of developers validating Copilot-generated code, developers often did not recognise LLM-originated code unless told so; provenance awareness changed how they validated and repaired it. That makes it worth storing not only prompts, but also whether code was AI-assisted and what context or workflow produced it. citeturn14view1

Two more findings are especially relevant to your schema design. First, a study of self-declared AI-generated code found that developers benefit from documenting the **generation context**, including prompts, quality notes, and snippet-level provenance, because this improves later understanding and troubleshooting. Second, field studies of code-editing assistants show that developers frequently **edit accepted changes**, **delete parts after acceptance**, and **re-prompt** from the same region—so initial acceptance alone is a weak proxy for value. citeturn14view2turn16view2

That is consistent with industrial metrics work. The Ansible Lightspeed paper argues that “initial acceptance rate” is misleading and proposes a stronger acceptance notion that accounts for how much of an accepted suggestion actually survives subsequent editing. VS Code’s Copilot OTel already exposes very similar concepts, including `copilot_chat.edit.acceptance.count`, `copilot_chat.lines_of_code.count`, and `copilot_chat.edit.survival.four_gram`. In other words, the platform telemetry is now close to what the research says you should measure. citeturn16view1turn21view2

The main platform limitation is equally important: GitHub’s enterprise audit log **does not include local client session data or local prompts**. GitHub’s own documentation says a custom solution is required for that, and gives custom hooks / self-managed logging as the example. Public documentation also makes it clear that VS Code’s OTel monitoring is centred on **Copilot Chat agent interactions** and related edit/activity metrics, while GitHub usage metrics provide **aggregated** coverage for IDE chat, agent use, code completion, and CLI. That means you can get excellent **raw trace-level** visibility for chat/agent activity, but a fully detailed, public, prompt-level feed for every inline completion is **not clearly documented as available**; for that surface, the safe assumption is that the official path is aggregate metrics rather than per-suggestion raw content. citeturn29view0turn20view0turn21view2turn31view1turn23view3

## Best-fit solution stack

The best fit for your requirements is a **hybrid** of official telemetry plus a few open-source building blocks, not a single monolithic product.

### The official pieces you should use first

VS Code now has official **OpenTelemetry monitoring for Copilot Chat agent interactions**. It exports traces, metrics, and events; the signals follow OTel GenAI semantic conventions plus a `github.copilot.*` namespace; and it supports OTLP, console, file, and SQLite-backed export paths. It also instruments foreground agent traces and background/CLI agent traces, and it can capture content if you explicitly turn that on. citeturn20view0turn20view1

VS Code also now has official **hooks**. These run automatically at lifecycle events, receive structured JSON on stdin, and can emit JSON on stdout to influence behaviour. The documented hook events include `SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `PreCompact`, `SubagentStart`, `SubagentStop`, and `Stop`. Hooks are explicitly described as suitable for audit trails, logging, and control of approvals. citeturn8view0turn11view3turn12view3

For organisation-wide roll-up, GitHub’s **usage metrics** are the second official pillar. The metrics cover adoption, engagement, acceptance rates, lines of code, chat requests, agent adoption, model usage, language usage, and per-user fields such as `used_chat`, `used_agent`, `used_cli`, and `used_copilot_coding_agent`. They also expose pull-request metrics at GitHub scope, but because your repos live in Azure DevOps, those PR lifecycle figures should not be your source of truth for repo outcomes; use Azure DevOps events for that part. citeturn23view3turn31view1turn31view0turn36view2turn28search0turn28search9

### The open-source pieces that fit well

For a ready-made dashboard and historical metrics store, **`github-copilot-resources/copilot-metrics-viewer`** is the strongest match I found. It provides charts for Copilot metrics at organisation or enterprise level; in “historical mode” it adds PostgreSQL plus a sync service so you can persist data beyond the API’s rolling window and derive long-term team views. The marketplace entry describes per-user metrics, team comparison, CSV export, and self-hosting on Azure, Docker, or Kubernetes. citeturn26search2turn27view3turn26search10

For hook starters, the **`github/awesome-copilot`** repository is useful immediately, particularly the **Session Logger Hook** and **Governance Audit Hook**. The first logs session starts, ends, and user prompts in structured JSON; the second scans prompts for risky patterns and appends governance events. The separate **`hooks-demo`** repo is useful because it shows the expected hook payloads and event structure in practice. citeturn27view0turn27view1turn27view2

For the central backend, you have two strong options:

- **Azure-native**: OTel Collector → Azure Monitor / Application Insights → Grafana dashboards in Azure Monitor or Azure Managed Grafana. Microsoft now documents this specifically for AI coding agents, including GitHub Copilot, and provides purpose-built dashboards for cost, token usage, sessions, tool calls, latency, and errors. Azure Monitor also supports native OTLP ingestion through an OTel Collector. citeturn37view3turn37view2  
- **Open-source AI observability**: **Langfuse** is the cleaner open-source choice if you want trace inspection, prompt review, evals, and self-hosting. Langfuse supports OTLP ingestion and positions itself as an open-source AI engineering platform for observability and improvement loops. **OpenLIT** is another OTel-native open-source option, but Langfuse is the more mature fit for trace-centric prompt/agent analysis. citeturn32search0turn32search5turn32search13turn33search0turn33search1

My recommendation for your stack is therefore:

- **Primary recommendation**: Azure-native central plane, because you already live in Microsoft tooling and want a structurally simple rollout. citeturn37view3turn37view2  
- **Secondary recommendation**: add Langfuse if you later want richer AI-specific trace analysis, prompt comparison, evals, and annotations. citeturn32search0turn32search5

## Recommended architecture

Design the system as **three layers plus one correlation feed**.

The first layer is **capture on the developer machine**. Enable VS Code Copilot OTel export, but point it to a **local** collector endpoint such as `http://127.0.0.1:4318`, not directly to a cloud service. Keep `captureContent` **off** by default because the official docs warn that prompt content, file contents, tool arguments, and tool results can be sensitive. Turn it on only for a trusted pilot ring or after you add redaction and access controls. You can also enable the local SQLite DB exporter for break-glass debugging and offline triage. citeturn20view0

The second layer is **local persistence and decoupling**. Run an OTel Collector locally or on the developer workstation VM. Give that collector a **persistent sending queue** backed by file storage. The OTel docs explicitly say persistent queues use disk-backed storage, and if the collector restarts, buffered items are resumed and export continues. This is the cleanest way to decouple “tracking” from “upload”. citeturn37view0turn37view1

The third layer is **central storage and analytics**. For an Azure-first rollout, the collector exports to Azure Monitor / Application Insights. Microsoft’s current guidance for AI coding agents is Collector → Application Insights → Grafana, and Azure Monitor now supports OTLP ingestion from an OTel Collector. citeturn37view3turn37view2

The correlation feed is **Azure DevOps service hooks**. Use webhooks for code pushed, PR created/updated/merged, and build completion so you can join session-level Copilot activity with repository outcomes in the place where your repos and delivery workflow actually live. That lets you answer questions such as: “Which AI-assisted sessions led to successful PRs?”, “Which prompt categories correlate with build failures?”, and “Which teams are overusing agent mode without downstream acceptance?”. citeturn28search0turn28search3turn28search9

A simple but future-proof data model should store:

- **Raw trace/event layer**: every OTel span / metric / hook record, append-only.  
- **Enriched event layer**: add `repo`, `azure_devops_project`, `branch`, `user_alias`, `surface`, `mode`, `model`, `session_id`, `tool_name`, `tool_risk`, `workflow_label`, `story_label`, `privacy_level`.  
- **Analytical layer**: session outcomes, re-prompt rate, acceptance and survival, tool risk counts, prompt category trends, team-level adoption, and repo outcome correlations.  

That layered pattern is directly aligned with the provenance literature’s emphasis on trace sources, execution units, memory lineage, and trust functions, and with GitHub’s own daily per-user / per-team metrics shape. citeturn14view3turn14view0turn31view2

## Implementation plan

### The MVP you can roll out first

Start with a **one-week pilot** on a small team. Turn on VS Code Copilot OTel and point it at a local collector rather than a remote backend. Keep content capture off initially. citeturn20view0

Use a workspace-level `settings.json` like this:

```json
{
  "github.copilot.chat.otel.enabled": true,
  "github.copilot.chat.otel.exporterType": "otlp-http",
  "github.copilot.chat.otel.otlpEndpoint": "http://127.0.0.1:4318",
  "github.copilot.chat.otel.captureContent": false,
  "github.copilot.chat.otel.dbSpanExporter.enabled": true
}
```

This uses only documented settings and gives you immediate coverage for Copilot Chat / agent activity, plus a local trace DB export path. citeturn20view0

Next, add a repository-scoped hook file in `.github/hooks/ai-audit.json`. Use the VS Code-compatible event names so you can reuse logic across Copilot CLI / hook examples where possible. The initial hook set should be minimal: `SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, and `Stop`. That gets you the start, intent, action, result, and close of each session. citeturn11view3turn12view3

A starter hook config can look like this:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "type": "command",
        "command": "python .github/hooks/scripts/copilot_audit.py session_start"
      }
    ],
    "UserPromptSubmit": [
      {
        "type": "command",
        "command": "python .github/hooks/scripts/copilot_audit.py user_prompt"
      }
    ],
    "PreToolUse": [
      {
        "type": "command",
        "command": "python .github/hooks/scripts/copilot_audit.py pre_tool"
      }
    ],
    "PostToolUse": [
      {
        "type": "command",
        "command": "python .github/hooks/scripts/copilot_audit.py post_tool"
      }
    ],
    "Stop": [
      {
        "type": "command",
        "command": "python .github/hooks/scripts/copilot_audit.py stop"
      }
    ]
  }
}
```

The hook script should read stdin JSON and append **NDJSON** records to a local audit file, for example under `.copilot-audit/usage.ndjson`. Do **not** rely on `transcript_path` as a primary API, because the docs explicitly say it is not a stable hook API. Use the documented fields such as `prompt`, `tool_name`, and `tool_input`, and treat the transcript only as an optional convenience. citeturn12view3

### The collector pattern that keeps upload decoupled

Run a local OTel Collector with an OTLP receiver and a persistent queue. The official exporter helper documentation says that if you enable `sending_queue.storage`, the queue becomes persistent and can continue exporting after restart, with `filestorage` being a common safe choice. citeturn37view1

A generic starter collector config is:

```yaml
receivers:
  otlp:
    protocols:
      http:
        endpoint: 127.0.0.1:4318

extensions:
  file_storage:
    directory: /var/lib/otelcol/file_storage

processors:
  memory_limiter:
    check_interval: 1s
    limit_mib: 512

exporters:
  otlphttp/central:
    endpoint: https://YOUR-CENTRAL-OTLP-ENDPOINT
    headers:
      Authorization: Bearer ${CENTRAL_OTLP_TOKEN}
    sending_queue:
      storage: file_storage
      queue_size: 10000

service:
  extensions: [file_storage]
  pipelines:
    traces:
      receivers: [otlp]
      processors: [memory_limiter]
      exporters: [otlphttp/central]
    metrics:
      receivers: [otlp]
      processors: [memory_limiter]
      exporters: [otlphttp/central]
```

If you choose Azure Monitor, replace `YOUR-CENTRAL-OTLP-ENDPOINT` with the Azure Monitor collector / ingestion path described in Microsoft’s OTLP guidance, and authenticate using the Azure auth extension on the collector side. Microsoft documents both native OTLP ingestion and the recommended Application Insights path. citeturn37view2

### The central dashboards and long-term memory

For central visualisation, choose one of these two rollout paths.

**Azure-first path**: send the collector output to Application Insights and use Azure Monitor dashboards with Grafana or Azure Managed Grafana. Microsoft’s current documentation for AI coding agents already includes a GitHub Copilot dashboard covering operations, input/output tokens, chat sessions, tool calls, response time, and time to first token. citeturn37view3

**Open-source path**: send OTLP to Langfuse and use it as the prompt/trace analysis layer. Langfuse’s OTEL integration is designed for applications or collectors that already emit OTLP traces, which fits VS Code Copilot OTel very well. citeturn32search0turn32search5

In parallel, deploy **Copilot Metrics Viewer** in historical mode with PostgreSQL. That gives you a daily sync job and longer than 28-day history for organisation and team trends, while your trace backend gives you high-fidelity session memory. These two sources complement each other rather than competing. citeturn27view3turn26search10

### The labels and categories that actually matter

Do not over-design the taxonomy at the start. Use a small, stable set of dimensions that you can derive automatically from prompts, tool chains, and repo outcomes.

A sensible initial catalogue is:

- **Surface**: `chat`, `ask`, `edit`, `plan`, `agent`, `cli`, `cloud_agent`, `inline_completion_aggregate`. GitHub and VS Code already expose most of this distinction either in traces or metrics. citeturn31view1turn21view3  
- **Intent category**: `bugfix`, `feature`, `refactor`, `testing`, `docs`, `debugging`, `investigation`, `devops`, `security`, `scaffolding`. This is your own enrichment layer.  
- **Risk category**: `safe`, `review`, `blocked`, with optional subtypes like `credential_exposure`, `privilege_escalation`, `destructive_command`, inspired by the Governance Audit hook. citeturn27view1  
- **Outcome**: `accepted`, `rejected`, `edited_after_accept`, `re_prompted`, `build_pass`, `build_fail`, `pr_merged`, `pr_abandoned`. The first four come from Copilot telemetry and edit analysis; the last three come from Azure DevOps events. citeturn21view2turn16view2turn28search0turn28search9

This gives you enough structure to answer useful questions without inventing a brittle ontology too early.

### The metrics I would put on the first dashboard

Your first dashboard should focus on **behaviour quality**, not vanity usage counts.

I would include: session count, prompts per session, tool calls per session, time to first token, error count, acceptance count, edit survival, lines added/deleted, re-prompt rate, governance events, builds passed after AI session, builds failed after AI session, and PR merge rate after AI-assisted work. The core Copilot pieces are already available in current OTel and GitHub usage metrics, while the repo-outcome metrics come from Azure DevOps hooks. citeturn20view0turn21view2turn31view1turn28search0turn28search9

## Draw.io diagram

The XML below is a starter **draw.io** diagram for the recommended architecture. Import it directly into draw.io / diagrams.net. It shows the decoupled flow: **capture in VS Code**, **local durable collector**, **central analytics**, plus **GitHub usage metrics** and **Azure DevOps outcome correlation**. The structure follows the documented OTel + collector + dashboard path from Microsoft and the persistent-queue guidance from OpenTelemetry. citeturn20view0turn37view1turn37view2turn37view3

```xml
<mxfile host="app.diagrams.net" modified="2026-06-30T00:00:00.000Z" agent="ChatGPT" version="24.7.5">
  <diagram id="copilot-memory-architecture" name="Copilot Memory Architecture">
    <mxGraphModel dx="1600" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1600" pageHeight="1000" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>

        <mxCell id="2" value="Developers&#10;VS Code + GitHub Copilot" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=14;" vertex="1" parent="1">
          <mxGeometry x="40" y="120" width="180" height="80" as="geometry"/>
        </mxCell>

        <mxCell id="3" value="Built-in Copilot OTel export&#10;traces, metrics, events&#10;chat / agent / edit activity" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=13;" vertex="1" parent="1">
          <mxGeometry x="270" y="70" width="220" height="90" as="geometry"/>
        </mxCell>

        <mxCell id="4" value="Repository hooks&#10;.github/hooks/*.json&#10;SessionStart / UserPromptSubmit /&#10;PreToolUse / PostToolUse / Stop" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=13;" vertex="1" parent="1">
          <mxGeometry x="270" y="190" width="220" height="110" as="geometry"/>
        </mxCell>

        <mxCell id="5" value="Local audit store&#10;NDJSON hook logs&#10;local trace DB / JSONL export" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;fontSize=13;" vertex="1" parent="1">
          <mxGeometry x="540" y="210" width="210" height="80" as="geometry"/>
        </mxCell>

        <mxCell id="6" value="Local OTel Collector&#10;OTLP receiver&#10;persistent queue (file_storage)&#10;redaction / enrichment / routing" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;fontSize=13;" vertex="1" parent="1">
          <mxGeometry x="540" y="70" width="240" height="100" as="geometry"/>
        </mxCell>

        <mxCell id="7" value="Central Azure Monitor /&#10;Application Insights&#10;OTLP ingestion" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=13;" vertex="1" parent="1">
          <mxGeometry x="860" y="60" width="220" height="90" as="geometry"/>
        </mxCell>

        <mxCell id="8" value="Grafana / Azure dashboards&#10;usage, cost, latency, sessions,&#10;tool calls, survival, errors" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=13;" vertex="1" parent="1">
          <mxGeometry x="1140" y="60" width="230" height="90" as="geometry"/>
        </mxCell>

        <mxCell id="9" value="Warehouse / lakehouse&#10;Bronze raw events&#10;Silver enriched sessions&#10;Gold analytics" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=13;" vertex="1" parent="1">
          <mxGeometry x="860" y="200" width="220" height="100" as="geometry"/>
        </mxCell>

        <mxCell id="10" value="GitHub Copilot Usage Metrics API&#10;daily org / user / team reports" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;fontSize=13;" vertex="1" parent="1">
          <mxGeometry x="40" y="380" width="220" height="90" as="geometry"/>
        </mxCell>

        <mxCell id="11" value="Copilot Metrics Viewer&#10;PostgreSQL historical mode&#10;team and long-range adoption" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;fontSize=13;" vertex="1" parent="1">
          <mxGeometry x="320" y="380" width="230" height="90" as="geometry"/>
        </mxCell>

        <mxCell id="12" value="Azure DevOps service hooks&#10;push / PR / build / merge events" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;fontSize=13;" vertex="1" parent="1">
          <mxGeometry x="600" y="380" width="220" height="90" as="geometry"/>
        </mxCell>

        <mxCell id="13" value="Correlation and workflow mining&#10;AI session to repo outcome&#10;workflow / skill distillation" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=13;" vertex="1" parent="1">
          <mxGeometry x="1140" y="220" width="230" height="90" as="geometry"/>
        </mxCell>

        <mxCell id="20" style="endArrow=block;html=1;strokeWidth=2;" edge="1" parent="1" source="2" target="3">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="21" style="endArrow=block;html=1;strokeWidth=2;" edge="1" parent="1" source="2" target="4">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="22" style="endArrow=block;html=1;strokeWidth=2;" edge="1" parent="1" source="3" target="6">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="23" style="endArrow=block;html=1;strokeWidth=2;" edge="1" parent="1" source="4" target="5">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="24" style="endArrow=block;html=1;strokeWidth=2;" edge="1" parent="1" source="5" target="6">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="25" style="endArrow=block;html=1;strokeWidth=2;" edge="1" parent="1" source="6" target="7">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="26" style="endArrow=block;html=1;strokeWidth=2;" edge="1" parent="1" source="7" target="8">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="27" style="endArrow=block;html=1;strokeWidth=2;" edge="1" parent="1" source="7" target="9">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="28" style="endArrow=block;html=1;strokeWidth=2;" edge="1" parent="1" source="10" target="11">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="29" style="endArrow=block;html=1;strokeWidth=2;" edge="1" parent="1" source="11" target="9">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="30" style="endArrow=block;html=1;strokeWidth=2;" edge="1" parent="1" source="12" target="9">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="31" style="endArrow=block;html=1;strokeWidth=2;" edge="1" parent="1" source="9" target="13">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="32" style="endArrow=block;html=1;strokeWidth=2;" edge="1" parent="1" source="13" target="8">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

## Open questions and limitations

The main unresolved point is **raw inline completion capture**. The public documentation clearly supports trace-level export for Copilot Chat / agent interactions and aggregate code-completion metrics through GitHub usage reports, but it does **not** clearly document a public, prompt-level raw event stream for every inline suggestion shown in the editor. If you later decide you need that level of granularity, you may need either a custom editor extension strategy or to accept that inline completions remain an aggregate-only surface in the first release. citeturn20view0turn31view1turn23view3

Hooks are currently **preview** in VS Code and may be disabled by organisation policy. Also, the hook `transcript_path` is explicitly documented as a convenience field rather than a stable contract, so your implementation should depend on the documented hook payload fields instead. citeturn8view0turn12view3

Finally, because you use **Azure DevOps** for repos, you should treat GitHub’s organisation-level usage metrics as your **AI adoption / usage layer**, not as your full delivery-outcome layer. Delivery correlation should come from Azure DevOps events, since Azure DevOps service hooks are the supported way to emit push, PR, and build events to external systems. citeturn28search0turn28search3turn28search9