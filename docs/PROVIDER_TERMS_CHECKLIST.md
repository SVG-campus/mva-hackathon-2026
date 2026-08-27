# Hosted-service processor checklist

Organizer source: https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/discussions/2, point-by-point answer timestamp `2026-08-26T22:28:34Z`.

Complete this record for every cloud, annotation, AI, storage, logging, or collaboration service that could receive gated or patient-derived material. A service is eligible only as a processor/tool, not as an independent recipient.

## Required record

| Field | Required evidence |
|---|---|
| Provider and service | Legal provider and exact product or endpoint |
| Plan or tier | Commercial, enterprise, academic, free, grant, sponsor-credit, or other exact tier |
| Applicable terms | Direct terms/privacy/data-use links and access date |
| No training | Written terms or settings showing inputs and outputs are not used to train or improve models |
| No provider rights | Terms showing the provider takes no independent rights or purpose in the content |
| Retention | Maximum duration and limited operational purpose, including abuse, safety, debugging, or service-quality logs |
| Exact settings | Training opt-outs, history/state, storage, feedback, telemetry, public links, third-party tools, and regional controls |
| Credit override | Separate grant, sponsor, or promotional terms checked and recorded |
| Feedback rule | Users must not rate outputs or submit feedback containing challenge material |
| Downstream parties | Any subprocessors, connectors, MCP servers, browsing, code execution, or external tools that may receive content |
| Methods disclosure | Provider, model/service, plan/tier, relevant settings, and retention summarized without exposing patient data |
| Decision | `PASS_PROCESSOR`, `HOLD_UNVERIFIED`, or `FAIL_RECIPIENT` with reviewer and date |

## Current route status

| Route | Status | Evidence and next action |
|---|---|---|
| Dedicated GCP compute/storage with deterministic Exomiser | `HOLD_UNVERIFIED` | Verify the exact Google Cloud terms/tier, telemetry and logging, storage lifecycle, region, IAM, and deletion behavior before gated upload. |
| Current Codex desktop / ChatGPT task | `HOLD_UNVERIFIED` | Exact workspace plan, training opt-out, retention, application state, tool routing, and feedback behavior are not recorded. Do not expose patient-derived material to this task. |
| OpenAI API | `POTENTIALLY_ELIGIBLE` | Official API documentation says API data are not used for training unless the organization explicitly opts in and describes default abuse-monitoring retention of up to 30 days. Eligibility still depends on the exact endpoint, project settings, storage/state behavior, tier, and downstream tools. Source: https://developers.openai.com/api/docs/guides/your-data |
| Anthropic sponsor credits | `HOLD_UNVERIFIED` | Inspect the exact commercial and credit-program terms, data controls, retention, feedback behavior, and model endpoint before use. |

`POTENTIALLY_ELIGIBLE` is not permission to run patient data. It means a route may be promoted to `PASS_PROCESSOR` after every required field is evidenced and reviewed.

## Stop rules

- Any training right, provider reuse right, indefinite or unrelated retention, unclear credit override, or undisclosed downstream recipient fails the route.
- Any account or endpoint whose exact settings cannot be verified remains on hold.
- Do not paste patient content into support tickets, feedback forms, ratings, issue trackers, public links, or this Codex task.
- A handful of manually reviewed named variants may be treated as a finding; a genome-wide or reconstructive artifact remains controlled data.
- Do not begin gated upload until GCP and every service reachable from the private environment have a dated `PASS_PROCESSOR` record.
