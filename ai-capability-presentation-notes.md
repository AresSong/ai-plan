# Oral Presentation Notes: Capability-First Applied AI

## Purpose

Help the audience stop thinking about AI adoption as a list of use cases and start thinking in a more durable sequence:

Capabilities -> levels -> deployment envelopes -> applications -> model routing.

## Draft v1

Today I want to reframe how we think about applying AI. Most conversations start with use cases: customer service bot, coding assistant, document search, visual assistant. Those examples are useful, but they hide the deeper engineering question: what capability is being used, how strong does that capability need to be, and where can it run?

The mind map starts with AI systems and branches into three ideas. First are fundamental capabilities: multimodal perception, reasoning, context and memory, tool use, and grounding. Second are deployment envelopes: mobile or on-device, workstation or self-hosted, and cloud frontier. Third are leaf applications: accessibility assistants, enterprise document copilots, customer-service agents, coding agents, and search-grounded answer engines.

The new addition is model choice. We should not ask only whether to use a big general LLM such as Claude Sonnet. We should ask whether a small specialist model can handle a narrow capability first. Function-calling models can route stable API requests. Embedding models can retrieve relevant memory. Vision-language edge models can do local OCR or accessibility. Code models can handle bounded coding tasks. Safety classifiers can guard inputs and outputs.

The practical architecture is a routing policy. Start with the cheap specialist when the task is predictable and measurable. Escalate to Sonnet when the task becomes ambiguous, multi-step, cross-domain, multimodal, or failure-prone. Measure cost per successful task, not token price alone.

The conclusion is that the best applied AI system is rarely one model for everything. It is a capability map plus a deployment map plus a routing policy.

## Storyteller Review

The draft is accurate, but it reads like an executive summary. It needs more narrative tension. The audience should feel the pain of the old approach before they hear the framework.

Suggested improvements:

1. Start with a concrete failure mode: two teams both say they are building an AI assistant, but one needs a phone-local classifier and the other needs a frontier reasoning agent.
2. Use the mind map as a journey, not a taxonomy: first ask "what can the system do?", then "how much of that capability do we need?", then "where can it run?", then "what application becomes possible?"
3. Introduce specialist models as the plot twist: smaller does not always mean weaker; sometimes it means narrower, faster, cheaper, and easier to measure.
4. End with a decision rule the audience can remember: specialists for predictable work, Sonnet for ambiguous work, routing for production systems.

## Refined Presentation Script

### Opening

Let me start with a simple problem.

Two teams can both say, "We are building an AI assistant," and mean completely different things.

One team may need a private, instant, on-device model that classifies messages or reads a receipt. Another team may need a cloud reasoning agent that reads a million-token case file, calls tools, writes code, checks its work, and explains its answer.

Both are "AI assistants," but they are not the same engineering problem.

That is why starting from use cases can mislead us. The better starting point is capability.

### Transition 1: From Use Cases To Capabilities

The first question is not "What app should we build?"

The first question is: "What fundamental capability are we using?"

In the mind map, AI systems branch into a few core capabilities.

Multimodal perception means the system can understand text, images, audio, video, or live environment signals. Reasoning means it can do multi-step transformation before it answers. Context and working memory determine how much material it can hold in one pass. Tool use turns the model from a generator into an actor. Grounding and control decide whether the answer is based on the right evidence, policies, and constraints.

This is the first move: decompose the application into capabilities.

### Transition 2: From Capabilities To Levels

The second move is to ask how much of each capability we need.

For multimodal perception, text plus image is very different from real-time video and audio. For reasoning, a direct response is very different from test-time compute or tool-using planning. For context, 32k tokens, 400k tokens, and 1M tokens create very different product possibilities and very different costs.

This is where the mind map becomes practical. A capability is not just present or absent. It has levels.

### Transition 3: From Levels To Deployment Envelopes

Once we know the level, the next question is where it can run.

If the task is private, repetitive, bounded, and latency-sensitive, on-device or edge deployment may be the best answer. If the task needs local data handling or customization, a workstation or self-hosted model may be enough. If the task is long-horizon, tool-heavy, ambiguous, or high-value, then cloud frontier models become more attractive.

This is the deployment envelope: phone, workstation, cloud frontier, or rack-scale infrastructure.

And this matters because quality, latency, and cost do not improve together. Heavy reasoning may improve task success but harm turn-taking UX. Long context may reduce retrieval work but increase prefill cost and memory pressure. A stronger model can still be the wrong product choice.

### Transition 4: The Specialist Model Layer

Now comes the important addition.

Apart from general-purpose LLMs, there are specialist small models for individual capabilities.

But we need one distinction: small generalist versus specialist.

A small generalist is broad but compressed. A specialist is narrow by design. It may only do function calling, embeddings, safety classification, code generation, document vision, or bounded reasoning.

That narrowness is not a weakness when the task is predictable. It can mean lower latency, lower cost, better privacy, simpler evaluation, and fewer unnecessary tokens.

For example, an embedding model should not replace Sonnet. It should retrieve the right evidence before Sonnet sees the task. A function-calling specialist should not replace a full agent. It should route stable tool calls cheaply and quickly. A safety classifier should not answer business questions. It should guard the system before and after a generalist model runs.

### Transition 5: From Model Choice To Architecture

So the right question is not "Should we use Sonnet or many small models?"

The right question is: "What should be routed to specialists, and what should escalate to Sonnet?"

The architecture is:

Start with a specialist when success criteria are narrow and measurable.

Escalate to Sonnet when confidence is low, tool calls fail, the task crosses domains, the user needs explanation, or the work becomes ambiguous and multi-step.

This gives us a small-model front layer plus a frontier-generalist exception path.

### Closing

The key message is simple:

Do not choose an AI model first.

Map the capability first. Decide the level. Check the deployment envelope. Then route the task to the smallest reliable model, with a strong generalist ready for escalation.

That is how we move from AI experiments to AI systems.

## Short Version

Use this if you only have two minutes:

Most AI adoption starts with use cases, but use cases hide the engineering reality. A customer-service bot, a coding agent, and a visual assistant are really bundles of fundamental capabilities: multimodal perception, reasoning, context, tool use, and grounding.

Each capability has levels. Text plus image is not the same as real-time multimodal interaction. Direct response is not the same as test-time reasoning. A 32k context window is not the same as 1M tokens.

Those levels imply deployment envelopes: on-device, workstation, cloud frontier, or rack-scale serving. This matters because quality, latency, cost, privacy, and ease of use do not move together.

The new layer is specialist small models. Small does not always mean compressed generalist. Sometimes it means a narrow specialist: embeddings for retrieval, FunctionGemma or xLAM-style models for tool routing, Qwen-Coder for bounded code tasks, Gemma 3n for local multimodal work, ShieldGemma for safety classification.

The practical design is not one model for everything. It is specialists first for predictable measurable work, and Sonnet or another frontier generalist as escalation for ambiguous, multi-step, high-value work.

Capability first. Deployment second. Routing third. Applications last.
