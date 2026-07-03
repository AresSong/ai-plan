# Email Template Workflow Component

Date: 2026-07-02

Assumption: the product reference "828" is interpreted as n8n. If this meant another product, replace the n8n row in the competitor notes.

Design prototype: [prototype.html](./prototype.html)

## Goal

Add a workflow component that lets a builder generate an email from a reusable template, using data from earlier workflow steps, then pass the generated email to a send-email step or another downstream action.

The component should be easy enough for an operations admin to configure, but strict enough for engineering and compliance teams to trust in production workflows.

## Competitor Takeaways

| Product | Observed pattern | Product implication |
| --- | --- | --- |
| n8n | Send Email is a workflow node with SMTP credentials, to/subject/body fields, HTML or text format, attachments, and dynamic expressions. | Make "Generate email" a first-class workflow step with variable insertion, not a hidden notification setting. Separate template generation from delivery so teams can preview, approve, or route before sending. |
| Retool Workflows | Workflows are blocks connected by control flow. Blocks can reference previous block results. Run history shows success/failure by block. Global error handlers can run outside the main path. | Add run preview, block-level validation, output fields, and failure branches. Builders need to know what data the email component emits and how failures behave. |
| Qingliu/Qingflow | Public positioning emphasizes AI/no-code system building, private deployment, customization, process engine nodes, branch judgment, and automation. | Keep the UX business-user friendly, support enterprise deployment/permission needs, and make branch conditions around generated email visible on the canvas. |
| Pega | Email correspondence uses case data, participants, user references, and reusable templates. Outbound email templates support consistent branding. | Support participant-style recipients, reusable/versioned templates, case/workflow data binding, permissions, and audit history. |
| Jotform | Email notifications and autoresponders are template-like objects with recipients; paid accounts support multiple email templates/recipients; autoresponders support attachments and send options. | Non-technical users expect recipient setup, PDF/file attachments, and testable templates in one place. Keep common notification setup fast. |
| FcDesigner | Form-create's FcDesigner emphasizes visual low-code authoring and custom template/component combinations. | Make the configuration panel schema-driven and extensible. Reusable snippets and drag/drop-like insertion reduce repeated setup. |

Sources:
- n8n Send Email node: https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.sendemail/
- n8n expressions: https://docs.n8n.io/code/expressions/
- Retool workflow blocks: https://docs.retool.com/workflows/concepts/blocks
- Retool workflow triggers: https://docs.retool.com/workflows/concepts/triggers
- Qingflow product page: https://qingflow.com/
- Pega email correspondence: https://academy.pega.com/topic/email-correspondence/v1
- Pega outbound email templates: https://docs.pega.com/bundle/platform/page/platform/conversational-channels/creating-outbound-email-templates.html
- Jotform multiple recipients: https://www.jotform.com/help/39-send-notifications-to-multiple-recipients/
- Jotform autoresponder setup: https://www.jotform.com/help/26-setting-up-an-autoresponder-email/
- FcDesigner templates: https://view.form-create.com/en/template

## Proposed Component Shape

Component name: Generate Email

Primary job: produce a structured email object from a template and workflow data.

Suggested output:

```json
{
  "email": {
    "to": ["customer@example.com"],
    "cc": [],
    "bcc": [],
    "replyTo": "support@example.com",
    "subject": "Order ORD-1048 is ready",
    "html": "<p>Hello Mei...</p>",
    "text": "Hello Mei...",
    "attachments": [
      {
        "sourceStep": "Generate invoice PDF",
        "fileId": "file_123",
        "fileName": "invoice-ORD-1048.pdf"
      }
    ],
    "templateId": "tpl_order_ready",
    "templateVersion": 3
  }
}
```

Recommended downstream actions:
- Send Email
- Approval
- Add comment/note
- Store generated email
- Branch by validation status

## MVP Scope

Include:
- Add "Generate Email" action to workflow palette.
- Select existing template or create local template.
- Configure sender, recipients, reply-to, subject, HTML body, and plain-text fallback.
- Insert variables from trigger and previous steps.
- Preview with sample run data.
- Validate required fields and unresolved variables.
- Emit structured email output for downstream steps.
- Test generation without sending.
- Show run log with rendered subject, recipient count, template version, and validation errors.

Do not include in MVP:
- Full drag-and-drop email design builder.
- A/B testing.
- Marketing campaign scheduling.
- Deliverability analytics beyond send/generation status.
- Multi-language template management, unless required by current enterprise customer.

## User Roles

Workflow Builder: configures the workflow and email component.

Template Manager: creates and approves reusable email templates.

Workflow Operator: monitors runs and fixes failed email generation.

Compliance/Admin: controls who can edit sender identities, templates, and external recipients.

## User Stories

### 1. Add Generate Email Step

Description: As a Workflow Builder, I want to add a Generate Email step to a workflow, so that I can create an email message from workflow data before deciding how to send or route it.

Design: [prototype.html](./prototype.html)

Acceptance Criteria:
1. The action palette includes a "Generate Email" action under Communication.
2. Dragging or selecting the action adds a workflow node with an editable name.
3. The node exposes outputs for subject, html, text, recipients, attachments, template id, and validation status.
4. The node can be connected before Send Email, Approval, Branch, or Store Record actions.
5. The workflow cannot be published when the node has missing required configuration.

### 2. Configure Recipients From Workflow Data

Description: As a Workflow Builder, I want to set recipients using fixed addresses, user fields, participants, or variables from previous steps, so that the right people receive the generated email.

Design: [prototype.html](./prototype.html)

Acceptance Criteria:
1. The builder can configure To, CC, BCC, From, and Reply-To.
2. Recipient fields accept static email addresses and variable tokens.
3. The system validates email format for static values and flags unresolved variables for dynamic values.
4. The builder can choose whether empty optional recipient fields are ignored or treated as errors.
5. The run log records rendered recipient count without exposing hidden BCC values to unauthorized viewers.

### 3. Create Template With Variables

Description: As a Template Manager, I want to write a subject and body with approved workflow variables, so that each generated email is personalized and consistent.

Design: [prototype.html](./prototype.html)

Acceptance Criteria:
1. The editor supports subject, HTML body, and plain-text fallback.
2. A variable picker lists fields from the trigger and previous workflow steps.
3. Inserted variables use a consistent token format such as `{{customer.name}}`.
4. The editor highlights unresolved, misspelled, or unauthorized variables.
5. The system stores the template id and version used by each workflow run.
6. The builder can save the template as local to the workflow or reusable in the template library.

### 4. Preview With Sample Data

Description: As a Workflow Builder, I want to preview the email using sample run data, so that I can catch mistakes before publishing.

Design: [prototype.html](./prototype.html)

Acceptance Criteria:
1. The preview renders the subject, recipients, HTML body, plain-text body, and attachments.
2. The builder can switch between sample data, last successful run data, and manual test data where available.
3. Missing variables appear as validation errors and are visually marked in the preview.
4. Preview generation does not send an email or trigger downstream actions.
5. The preview updates within two seconds after the builder changes template text or selected data.

### 5. Attach Files From Earlier Steps

Description: As a Workflow Builder, I want to attach files generated earlier in the workflow, so that emails can include invoices, reports, or submitted documents.

Design: [prototype.html](./prototype.html)

Acceptance Criteria:
1. The builder can select file outputs from previous steps.
2. The builder can rename an attachment using static text or variables.
3. The system validates file availability, file size, file type, and permission access before publish and during runs.
4. The preview displays attachment name, source step, size when known, and validation state.
5. If an attachment is missing at runtime, the configured failure policy is applied.

### 6. Handle Validation, Retry, And Failure Branches

Description: As a Workflow Operator, I want clear validation errors and failure behavior for generated emails, so that failed runs can be diagnosed and recovered.

Design: [prototype.html](./prototype.html)

Acceptance Criteria:
1. The configuration panel shows blocking errors separately from warnings.
2. Runtime errors include unresolved variables, missing recipients, invalid addresses, missing attachments, and template permission failures.
3. The builder can choose failure behavior: stop workflow, continue without sending, retry generation, or route to failure branch.
4. Run history shows the selected template version, rendered subject, status, and error detail.
5. Failure details avoid exposing sensitive rendered body content to users without permission.

### 7. Manage Template Reuse And Permissions

Description: As a Compliance/Admin, I want template and sender permissions, so that only approved people can use customer-facing email content and identities.

Design: [prototype.html](./prototype.html)

Acceptance Criteria:
1. Admins can restrict who can create reusable templates, edit approved templates, and use sender identities.
2. A reusable template can be draft, approved, deprecated, or archived.
3. Publishing a workflow with an unapproved reusable template requires an explicit permission or approval.
4. Changes to a reusable template create a new version without silently changing published workflow behavior.
5. Audit logs include editor, approver, timestamp, template version, and workflows using the template.

## Prototype Notes

The prototype shows the recommended first implementation, not a final visual design system:
- Canvas node is selected for "Generate customer email."
- Right panel has tabs for Setup, Template, Preview, and Failure.
- Preview uses sample order data and token replacement.
- Validation checklist models publish blockers and warnings.
- The component emits a generated email object, which can then feed a separate Send Email step.

## Open Questions

1. Should this component send email directly, or only generate an email object? Recommendation: generate only in MVP, with Send Email as a separate downstream action.
2. Do we already have a template library, sender identity model, or file object model? If yes, bind to those instead of creating new systems.
3. Should templates be global, app-scoped, workflow-scoped, or all three?
4. Are external recipients allowed by default, or should they require admin policy?
5. Which expression syntax should match the rest of the platform: `{{field}}`, JavaScript, JSONPath, or formula builder?
6. What email provider integration is planned for the Send Email step: SMTP, SendGrid, SES, Microsoft Graph, or customer-managed connector?

## Suggested Build Sequence

1. Schema and runtime output contract.
2. Workflow palette action and canvas node.
3. Configuration panel for recipients, subject, body, and variables.
4. Preview/test generation with sample data.
5. Validation and publish blockers.
6. Attachments from previous steps.
7. Template library, versioning, approval, and admin permissions.
