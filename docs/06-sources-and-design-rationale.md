# 06 — Public sources and design rationale

Research context reviewed 11 October 2026. These sources explain why the workflow is worth investigating and what already exists. They do not establish demand for this implementation, verify vendor performance or prove novelty. Brief paraphrases and links are supplied; reports and proprietary product material are not redistributed.

## 1. Operational motivation

| Public source | Supported observation | Our design inference and limit |
|---|---|---|
| [PwC: AI-enabled content creation](https://www.pwc.com/us/en/industries/tmt/library/ai-enabled-content-creation.html), May 2026 | Disconnected content, metadata and operational information can constrain media AI deployment. | Model content dependencies and operational consequences together. The discussion largely concerns larger media organizations, not proof that small agencies need this product. |
| [McKinsey: Cutting the coordination tax](https://www.mckinsey.com/industries/industrials/our-insights/cutting-the-coordination-tax-how-agentic-ai-can-reshape-workflows), September 2026 | Organizational handoffs and coordination are potential workflow-automation targets. | Measure a completed handoff and its evidence, not just an agent's generated message. A broad analysis is not an ROI benchmark for this repository. |
| [Deloitte: Path to agentic transformation](https://www.deloitte.com/us/en/insights/industry/technology/path-to-agentic-transformation.html), August 2026 | Integration, data foundations and trust affect enterprise adoption. | Start with bounded contracts and explicit authority. No claim follows that a standalone orchestrator is the preferred purchasing choice. |

The combination of intake, dependency tracking, commercial choices, revision-bound approval and verified closure is this project's design synthesis. Consulting firms did not commission, endorse or validate the project.

## 2. Existing products and overlap

These are vendor descriptions, not independently tested functionality or purchasing recommendations. Product scope and availability can change; recheck before making current competitive claims.

| Product and public source | Advertised overlap | Consequence for this project |
|---|---|---|
| [Workamajig September 2026 update](https://www.workamajig.com/newsletter/workamajig-newsletter-september-2026) | Agency operations, project/client economics, assignments, scope visibility and AI access to operational information. | Budget-aware agency coordination already exists. Test actual content-dependency and closure behavior, not whether a dashboard can show margin. |
| [Productive manager checklist](https://help.productive.io/en/articles/17060782-getting-started-with-productive-the-manager-checklist) | Agency/service operations with AI assistance across deals, budgets, time, invoices and resource work; agent assignments and integrations are described. | A broad AI agency operations suite is not an empty category. Scope expansion alone is not differentiation. |
| [Kantata Expertise Agent announcement](https://www.kantata.com/blog/article/kantata-launches-expertise-agent-the-first-ai-superagent-built-for-professional-services), June 2026 | Agentic professional-services work across project, resource, financial and external-tool context. | Do not describe taking actions across service-delivery functions as unique. The prototype must earn any narrower engineering claim through evidence. |
| [Ziflow enterprise](https://www.ziflow.com/enterprise) | Creative proofing, versions, review and approval workflows. | Review, version history and automated routing are established capabilities. |
| [Planable approval guide](https://planable.io/guides/content-approvals-in-planable/) | Approval controls, locking/unapproval and approval-dependent scheduling. | Approval revocation and scheduling gates are not new ideas. Investigate changes originating outside the content object. |
| [Celtra creative tooling](https://celtra.com/blog/celtra-your-trusted-ads-design-tool/) | Linked creative variants and propagation of copy or offer updates. | A change-propagation demo must explain its supported cross-artifact boundary and cannot claim that updating variants is novel. |
| [FADEL Brand Vision](https://fadel.com/brand-vision/) | Rights tracking, asset use and workflows around expiry, renewal and takedown. | Avoid presenting rights expiry or asset-removal coordination as an invented category. |
| [Aprimo agentic DAM](https://www.aprimo.com/blog/agentic-dam-ai-agents-content-operations) | Governed content operations and approved-reference claim checking, alongside forward-looking capabilities. | Distinguish shipped claims from roadmap; do not infer a product gap solely because one page omits a feature. |

This list is illustrative, not exhaustive. Availability, implementation effort, accuracy, pricing and customer satisfaction were not tested. A landing page establishes advertised positioning, not proof that the workflow works well. Conversely, an omitted feature is not proof that a competitor cannot support it.

## 3. What this repository contributes if built

The proposed contribution is an inspectable implementation of a bounded agency workflow, explicit state/version/authority contracts, original synthetic scenarios and a reproducible comparison of revalidation strategies under a shared final guard. Any research claim must describe exactly that scope.

The semantic hypothesis is that reviewed content dependencies can focus corrective work and reduce unnecessary reopening of unrelated work. The execution hypothesis is that intent tracking and destination observation can prevent false completion claims within a defined connector contract. Neither hypothesis is demonstrated by having written expected outcomes.

The full delivery lifecycle makes those mechanisms understandable: a source change has consequences because there is an accepted scope, a budget, owners, pending tasks, reviewers and a destination. It is not a promise that one model autonomously replaces every role.

## 4. Attribution and future evidence

Public repositories may cite public reports and competitor documentation. Attribution is useful and belongs here; private interviews, identities, pricing negotiations, private contact access and commercial plans do not. Store any future private research outside this repository. Publish only authorized, reviewed aggregate observations and clearly label sample size and limitations.

Maintain a future evidence log with claim, source URL, publisher, publication date if known, access date, source type, exact supported point and limitation. For vendor sources, record whether the text describes generally available behavior, a pilot, a preview or a roadmap. For measurements from this project, link the actual run manifest rather than substituting a consulting report.

Do not copy long passages, imply endorsement, claim a competitor-free market, or treat a product announcement as evidence of customer outcomes. A negative experiment and a finding that existing tools are sufficient are both useful conclusions.
