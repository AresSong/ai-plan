# Confluence Subtree Export Solution for AI Knowledge Base Bootstrap

## 1. Objective

The goal is to export a collection of Confluence pages under a selected root page and prepare them as a clean, structured source corpus for an AI knowledge base such as LLM Wiki.

The target scenario is:

- There are 100+ Confluence pages.
- The required pages form a subtree inside a larger Confluence space.
- The user is not necessarily a Confluence Space Admin.
- The initial export can be a one-off bootstrap.
- The exported content should later support incremental synchronization.
- The resulting files should preserve page identity, hierarchy, metadata, and attachments.
- The AI should not need to traverse the Confluence page tree itself.

---

## 2. Recommended Approach

For a user who is not a Space Admin, the recommended approach is:

> Use the Confluence REST API with the user's own identity to deterministically discover and export the selected root page and all descendants that the user is authorized to view.

This is preferable to asking an AI agent to navigate page-by-page through MCP.

The high-level flow is:

```text
Selected Confluence Root Page
            |
            v
Confluence REST API
            |
            |-- Discover descendants
            |-- Fetch page content
            |-- Fetch metadata
            |-- Fetch attachments
            v
Local Markdown Corpus
            |
            v
LLM Wiki / Knowledge Compiler
            |
            v
Semantic Knowledge Base
```

---

## 3. Why Not Use MCP for Initial Bootstrap?

MCP is useful for live access to Confluence, but it is not the ideal bootstrap mechanism for hundreds of pages.

An MCP-driven AI workflow may look like this:

```text
LLM
 |
 v
MCP
 |
 v
Read root page
 |
 v
Reason about which child pages to follow
 |
 v
Read child
 |
 v
Reason again
 |
 v
Continue recursively
```

This has several disadvantages:

- The LLM spends tokens on navigation rather than understanding content.
- Traversal can be slow.
- It may accidentally follow cross-links outside the intended subtree.
- It is harder to guarantee complete coverage.
- It is harder to reproduce exactly.
- Failures midway through traversal can leave an incomplete corpus.

The preferred bootstrap model is:

```text
Deterministic Export Script
 |
 v
Root Page ID
 |
 v
Confluence API discovers descendants
 |
 v
Pages downloaded programmatically
 |
 v
Markdown corpus
 |
 v
LLM Wiki
```

The AI performs no navigation reasoning during acquisition.

---

## 4. Permissions Model

Being a Space Admin is not strictly required.

There are three relevant cases.

### Case A — User already has Export Space permission

If the user can access:

```text
Space settings
    ->
Export space
```

then a Confluence HTML Custom Export may be sufficient.

This is the easiest manual approach.

### Case B — User does not have Export Space permission, but API access is allowed

Use the Confluence REST API.

The API operates using the user's identity and therefore returns only content the user is already permitted to view.

This is the recommended option for the 100+ page subtree scenario.

### Case C — API access is prohibited by corporate policy

Ask the Space Admin for:

> Export Space permission

rather than:

> Space Admin permission

This grants significantly less authority while still enabling the user to perform a bulk export.

---

## 5. Selecting the Root Page

The exporter should accept one Confluence page ID as its starting point.

Example:

```text
ROOT_PAGE_ID=123456789
```

The selected page represents the root of the knowledge subtree.

Example Confluence hierarchy:

```text
Whole Confluence Space
|
|-- Team Administration
|
|-- HR
|
|-- Workflow Platform          <-- selected root
|   |
|   |-- Requirements
|   |   |-- Workflow Builder
|   |   |-- Approval
|   |   `-- SLA
|   |
|   |-- Architecture
|   |   |-- UI
|   |   |-- Backend
|   |   `-- Database
|   |
|   `-- Operations
|       |-- Deployment
|       `-- Support
|
`-- Other Projects
```

Only this subtree should be exported:

```text
Workflow Platform
|
|-- Requirements
|-- Architecture
`-- Operations
```

The exporter should rely on Confluence parent/child relationships, not hyperlinks embedded in page bodies.

This avoids accidentally following links to unrelated pages.

---

## 6. Subtree Discovery

The exporter should:

1. Fetch the root page.
2. Request all descendants of the root page.
3. Handle pagination.
4. Create a complete list of visible page IDs.
5. Fetch the page data for each ID.

Conceptually:

```python
root = get_page(ROOT_PAGE_ID)

descendants = get_all_descendants(ROOT_PAGE_ID)

pages = [root] + descendants

for page in pages:
    export(page)
```

A deterministic script should perform the traversal rather than an LLM.

---

## 7. Data to Export for Each Page

At minimum, preserve:

- Page ID
- Page title
- Parent page ID
- Ancestor hierarchy
- Root page ID
- Source URL
- Page version
- Last modified timestamp
- Page body
- Attachments
- Relevant page links
- Content hash
- Export timestamp

This allows the original Confluence source to remain traceable.

---

## 8. Recommended Output Format

Use:

> One Confluence page = one Markdown file

Suggested structure:

```text
knowledge/
`-- raw/
    `-- confluence/
        |-- workflow-platform/
        |   |-- 123456789-workflow-platform.md
        |   |-- 123456800-requirements.md
        |   |-- 123456801-workflow-builder.md
        |   |-- 123456802-approval.md
        |   |-- 123456900-architecture.md
        |   |-- 123456901-ui.md
        |   `-- 123456902-backend.md
        |
        `-- attachments/
```

Using the page ID in the filename helps maintain stable identity even when the Confluence page title changes.

---

## 9. Markdown Frontmatter

Each Markdown file should contain structured metadata.

Example:

```yaml
---
source_system: confluence
space_key: WORKFLOW
page_id: "123456801"
title: "Workflow Builder"
root_page_id: "123456789"

parent:
  id: "123456800"
  title: "Requirements"

ancestors:
  - id: "123456789"
    title: "Workflow Platform"
  - id: "123456800"
    title: "Requirements"

source_url: "https://company.atlassian.net/wiki/..."
version: 17
last_modified: "2026-08-20T04:17:00Z"
content_hash: "sha256:..."
exported_at: "2026-08-24T..."
---
```

The original page content follows the frontmatter.

Example:

```markdown
# Workflow Builder

## Purpose

...

## Business Rules

...

## Related Components

...
```

---

## 10. Preserve Hierarchy Explicitly

Do not rely only on folders to represent hierarchy.

The hierarchy should also be recorded in metadata.

For example:

```text
UI Architecture
    |
    `-- parent: Architecture
            |
            `-- parent: Workflow Platform
```

This allows the hierarchy to later become explicit relationships in the knowledge graph.

For example:

```text
UI Architecture
    -- belongs_to --> Architecture
    -- belongs_to --> Workflow Platform
```

---

## 11. Attachments

Attachments can contain substantial business and technical knowledge.

Examples include:

- Architecture diagrams
- Excel spreadsheets
- PDFs
- Screenshots
- Word documents
- PowerPoint files
- Process diagrams
- Sequence diagrams

Recommended structure:

```text
123456901-ui-architecture.md

123456901-ui-architecture.assets/
    |-- sequence-diagram.png
    |-- data-model.xlsx
    `-- architecture-v3.pdf
```

The Markdown file can reference local assets:

```markdown
## Sequence

![Sequence diagram](./123456901-ui-architecture.assets/sequence-diagram.png)
```

Attachments should not be discarded during the bootstrap process.

---

## 12. Suggested Exporter Components

A simple implementation can be structured as:

```text
confluence-exporter/
|
|-- config/
|   |-- base_url
|   `-- root_page_id
|
|-- discovery/
|   `-- descendants
|
|-- extraction/
|   |-- page_content
|   |-- metadata
|   `-- attachments
|
|-- transformation/
|   |-- html_to_markdown
|   `-- metadata_to_frontmatter
|
`-- output/
    `-- raw/confluence/
```

A Python implementation is sufficient for the initial version.

---

## 13. Logical Processing Flow

```text
ROOT_PAGE_ID
     |
     v
Fetch root page
     |
     v
Fetch descendants
     |
     v
Handle pagination
     |
     v
Collect page IDs
     |
     v
For every page
     |
     |-- Fetch content
     |-- Fetch metadata
     |-- Fetch attachments
     |-- Calculate content hash
     |
     v
Convert content to Markdown
     |
     v
Add YAML frontmatter
     |
     v
Write local file
     |
     v
Feed raw corpus into LLM Wiki
```

---

## 14. Initial Bootstrap vs Incremental Synchronization

The same exporter should eventually support two modes.

### Bootstrap Mode

Export every page under the root:

```text
Root
 |
 v
All descendants
 |
 v
Download everything
```

### Incremental Mode

Compare:

- Page version
- Last modified timestamp
- Content hash

Example:

```text
Confluence page
      |
      v
Compare version/hash
      |
   +--+--+
   |     |
unchanged changed
   |     |
 skip   download
          |
          v
     update raw file
          |
          v
 recompile affected knowledge
```

This means the initial one-off exporter can later become a synchronization service without changing the core architecture.

---

## 15. Role of MCP

MCP should still be part of the architecture, but with a different responsibility.

Recommended separation:

### Snapshot / Export Pipeline

Purpose:

> Knowledge acquisition

Responsibilities:

- Discover all pages under a root.
- Export large collections.
- Preserve source metadata.
- Download attachments.
- Detect changes.
- Maintain the raw corpus.

### LLM Wiki

Purpose:

> Semantic compilation

Responsibilities:

- Read the raw corpus.
- Extract concepts.
- Connect related knowledge.
- Synthesize higher-level documentation.
- Build navigable knowledge structures.

### MCP

Purpose:

> Live retrieval interface

Responsibilities:

- Retrieve the latest Confluence content during an agent session.
- Verify source evidence.
- Access pages not currently compiled into the knowledge base.
- Fetch recently changed information.
- Support targeted lookups.

The overall architecture becomes:

```text
                  Confluence
                      |
          +-----------+-----------+
          |                       |
          v                       v
 Snapshot Exporter               MCP
          |                       |
          v                       |
 Immutable Raw Corpus             |
          |                       |
          v                       |
       LLM Wiki                   |
          |                       |
          v                       |
 Compiled Semantic Knowledge      |
          |                       |
          +-----------+-----------+
                      |
                      v
                Coding Agent
```

---

## 16. Longer-Term Semantic Layer Architecture

The Confluence exporter can eventually become one ingestion path in a larger enterprise engineering knowledge architecture.

```text
                       SOURCE SYSTEMS
                            |
       +--------------------+--------------------+
       |                    |                    |
       v                    v                    v
   Confluence          Azure DevOps             Git
       |                    |                    |
       v                    v                    v
 Snapshot Exporter    Work Item Exporter     Code Parser
       |                    |                    |
       +--------------------+--------------------+
                            |
                            v
                  Immutable Source Store
                            |
                 +----------+----------+
                 |                     |
                 v                     v
      Deterministic Extraction    LLM Compilation
                 |                     |
                 v                     v
            Source Graph        Semantic Knowledge
                 |                     |
                 +----------+----------+
                            |
                            v
                 Unified Knowledge Graph
                            |
                            v
                     Evidence Layer
               +------------+-----------+-----------+
               |            |           |           |
               v            v           v           v
        deterministic     human      inferred    proposed
                            |
                            v
                         Gold KB
                            |
                +-----------+-----------+
                |           |           |
                v           v           v
              Agent       Coding      Search
```

---

## 17. Recommended Decision Tree

```text
Can you view the required Confluence subtree?
                    |
                   Yes
                    |
                    v
Do you have Export Space permission?
            /                   \
          Yes                    No
           |                      |
           v                      v
HTML Custom Export         Is REST API allowed?
                               /        \
                             Yes         No
                              |           |
                              v           v
                       API Subtree     Ask Admin for
                        Exporter       Export permission
                              |
                              v
                       Markdown Corpus
                              |
                              v
                           LLM Wiki
```

For a subtree containing 100+ pages, the API subtree exporter is generally preferable even when HTML export is available because it creates a repeatable process that can later support incremental synchronization.

---

## 18. Recommended Implementation Sequence

### Phase 1 — Bootstrap

1. Select the Confluence root page.
2. Record its page ID.
3. Authenticate to Confluence using the user's normal identity.
4. Discover descendants through the REST API.
5. Fetch page content and metadata.
6. Fetch attachments.
7. Convert page bodies to Markdown.
8. Add YAML metadata.
9. Store one page per file.
10. Feed the resulting directory into LLM Wiki.
11. Review generated knowledge for quality and coverage.

### Phase 2 — Add Change Detection

1. Persist page versions and hashes.
2. Query the subtree periodically.
3. Identify added pages.
4. Identify changed pages.
5. Identify removed or inaccessible pages.
6. Re-export only affected pages.
7. Trigger incremental knowledge recompilation.

### Phase 3 — Integrate Other Engineering Sources

Add:

- Azure DevOps Boards
- Git repositories
- Test repositories
- CI/CD pipelines
- Architecture documents
- Figma / UX artifacts

The resulting system evolves from a Confluence knowledge base into a semantic layer spanning business intent, architecture, code, tests, and operational evidence.

---

## 19. Final Recommendation

For the current use case:

> Use a small deterministic Confluence REST API subtree exporter, authenticated as the normal user, with a single root page ID as input.

Export:

- the root page,
- every authorized descendant,
- page metadata,
- hierarchy,
- attachments,
- and stable source identifiers,

into a Markdown corpus with YAML frontmatter.

Then use LLM Wiki to compile that corpus into semantic knowledge.

Use MCP later for live retrieval and verification rather than as the bulk bootstrap mechanism.

This approach provides a clean evolution path:

```text
One-off export
      ->
Repeatable snapshot
      ->
Incremental synchronization
      ->
Multi-source engineering semantic layer
```
