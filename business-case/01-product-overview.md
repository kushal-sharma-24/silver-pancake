# HiveShip — Product Overview

## What Is HiveShip?

HiveShip is **internal delivery infrastructure** — a headless, API-triggered pipeline that turns a plain-English goal into a reviewed GitHub Pull Request. It runs without an IDE, without a developer session, and without human intervention between input and output.

It is not a product competing with Copilot or Claude Code. It is tooling that makes a service delivery team measurably faster by automating the work that happens when no developer is sitting at a keyboard.

### The 30-second pitch

> You describe what you want — via API call, webhook, Teams message, or cron schedule. HiveShip assembles a team of AI agents, each with a specific role. They collaborate through a dependency graph, produce files, self-review their work, and open a PR on your repo. If the review fails, they fix it automatically. You review a finished PR, not a work-in-progress chat.

### How it works (5 phases)

```
Goal (natural language — API, webhook, or Teams trigger)
  │
  ▼
┌─────────────────────────────────┐
│  PHASE 1: PLANNING              │
│  LLM decomposes goal into a     │
│  DAG of 1-8 specialized agents  │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│  PHASE 2: DAG EXECUTION         │
│  Agents run in parallel threads │
│  (up to 4 concurrent). Blocked  │
│  agents spawn helpers on-the-fly│
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│  PHASE 3: DELIVERY SYNTHESIS    │
│  Agent artifacts are merged     │
│  into self-contained, runnable  │
│  source files                   │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│  PHASE 4: SELF-REVIEW           │
│  Reviewer agent checks code.    │
│  If rejected → fixer agent      │
│  patches and re-submits         │
│  (up to N cycles)               │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│  PHASE 5: PR DELIVERY           │
│  Branch created, files pushed,  │
│  PR opened on GitHub            │
└─────────────────────────────────┘
```

### Key architectural properties

| Property | Detail |
|----------|--------|
| **Multi-agent DAG** | Work is decomposed into parallel specialist roles, not one monolithic prompt |
| **Self-healing** | Blocked agents trigger dynamic helper spawning; failed agents are pruned without killing the whole job |
| **Self-reviewing** | A separate reviewer agent evaluates the output before delivery |
| **BYO LLM** | Works with Gemini, any OpenAI-compatible API (vLLM, Ollama, LM Studio), or local models |
| **Headless / API-first** | No IDE required. FastAPI server with REST + SSE. Triggered by webhook, CLI, Teams, or cron |
| **Git-native output** | Output is a real PR on a real repo — not clipboard text or chat messages |
| **Container-ready** | Single Docker image, deploys to Azure Container Apps, AWS ECS, or any container host |

### Deployment model

```
┌──────────────┐       ┌──────────────────┐       ┌────────────┐
│  CLI / Teams │──────▶│  HiveShip API   │──────▶│  GitHub    │
│  Webhook/Cron│  HTTP │  (FastAPI on ACA)│  Git  │  (PR)      │
└──────────────┘       └────────┬─────────┘       └────────────┘
                                │
                                │ LLM calls
                                ▼
                       ┌──────────────────┐
                       │  Gemini / vLLM / │
                       │  Ollama / Any    │
                       │  OpenAI-compat   │
                       └──────────────────┘
```

---

## What HiveShip Is Best At

These are the use cases where HiveShip adds value that IDE-based tools (Copilot, Claude Code, Cursor) cannot replicate:

### 1. Headless automation — no developer session required

The `/github-webhook` endpoint listens for PR comments. When a reviewer writes "fix the error handling in auth.py," HiveShip clones the PR branch, generates a fix, pushes a commit, and replies — without any developer opening an IDE. This works at 3am, on weekends, and during holidays.

Similarly, CI failures can trigger HiveShip to read error output, generate a fix, and push a correction — turning it into a self-healing CI step.

### 2. Batch operations across repositories

"Update the logging library across all 50 microservices" is a single HiveShip goal that produces 50 PRs. No developer is going to open Copilot 50 times for the same mechanical change. HiveShip handles fleet-wide dependency bumps, compliance sweeps, and migration patterns from one API call.

### 3. Boilerplate and scaffold generation from well-scoped specs

When the specification is clear and the output format is predictable — test suites from requirements docs, K8s manifests from service definitions, API scaffolds from OpenAPI specs, structured logging formatters from a log contract — HiveShip's multi-agent pipeline produces consistent results faster than a developer doing it manually.

---

## Concrete Examples

### Webhook PR revision (no developer needed)

> A reviewer comments on PR #247: *"The retry logic in `expense_sync.py` doesn't handle 429 rate-limit responses — add exponential backoff with jitter."*
>
> HiveShip's `/github-webhook` endpoint fires. It clones the PR branch, reads the reviewer's comment and the target file, generates a fix (adds `tenacity` retry with exponential backoff + jitter), pushes a new commit, and replies on the PR thread — all within 2-3 minutes. The original developer never context-switches away from their current task.

### Fleet-wide dependency bump

> **Goal:** *"Update `pydantic` from v1 to v2 across all 30 microservices. Replace `validator` with `field_validator`, update `Config` classes to `model_config`, and fix any `from_orm` calls to `model_validate`."*
>
> HiveShip runs the goal against each repo: clones, reads existing code, generates the migration, opens a PR with a clear diff description. 30 PRs land overnight. Developers spend the morning reviewing diffs instead of spending a week doing 30 identical migrations by hand.

### Boilerplate sprint story — contract tests from API docs

> **Goal:** *"Given the `travel-profile-service` API documentation, generate pytest contract tests for all GET and POST endpoints. Each test should validate response schema, required fields, and HTTP status codes. Use `httpx` as the client."*
>
> The planner assigns agents: one reads the API doc and extracts endpoint signatures, another generates test cases, a third generates shared fixtures and conftest. The reviewer checks that every endpoint has at least one test. Output: a PR with `tests/contract/` containing 15-20 test files — a sprint story that would've taken a developer 2-3 days, done in minutes.

### CI auto-fix

> A GitHub Actions pipeline fails on `main` at 11pm:
> ```
> ModuleNotFoundError: No module named 'azure.identity'
> ```
> A CI webhook triggers HiveShip with the error output. HiveShip reads `requirements.txt`, adds `azure-identity>=1.16.0`, and pushes a fix commit. The pipeline re-runs and passes. Nobody was paged.

### Logging standardization across a project

> **Goal:** *"Audit all Python services in the CDE project. Replace any use of `print()`, bare `logging.info()`, or custom logger setup with the standard `structlog` configuration defined in `docs/logging-standard.md`. Ensure every log line includes `correlation_id`, `service_name`, and `timestamp`."*
>
> HiveShip processes each service: reads existing logging calls, reads the standard doc, generates replacements that follow the convention. One trigger, multiple PRs, all consistent.

### K8s manifest generation from a service definition

> **Goal:** *"Create Kubernetes deployment, service, HPA, and ingress manifests for the `expense-export-worker` service. Base image: `ghcr.io/amexgbt/expense-export-worker:latest`. Requires 512Mi memory, 250m CPU. Scales 2-8 replicas on CPU > 70%. Expose on port 8080 behind the internal ingress class."*
>
> Three agents: one generates the Deployment + Service, one generates the HPA, one generates the Ingress with annotations. Reviewer checks label selectors match across all manifests. Output: a PR with `k8s/expense-export-worker/` ready for `kubectl apply`.

### Migration-as-a-service — Java 8 to Java 21

> **Goal (per module):** *"Migrate `com.acme.billing.InvoiceProcessor` from Java 8 to Java 21. Replace anonymous inner classes with lambdas, convert POJOs to records where immutable, replace `Optional.get()` with `orElseThrow()`, and update `Stream` usage to use `toList()` instead of `collect(Collectors.toList())`."*
>
> Run across 200 classes in a legacy billing system. HiveShip + 2 senior reviewers delivers in 6 weeks what a 6-person team would take 6 months to do manually. The client pays $800K instead of $2M.

---

## What HiveShip Is NOT Best At

Being honest about where other tools win:

| Use Case | Better Tool | Why |
|----------|-------------|-----|
| Interactive, exploratory coding | Copilot Agent, Claude Code, Cursor | These tools have a human in the loop making decisions at each step, and they can run the code to verify it works |
| Complex architectural decisions | A senior developer (with or without AI) | HiveShip's planner cannot negotiate trade-offs or understand unstated business context |
| Code that needs execution feedback | Claude Code, Copilot (they run tests and iterate) | HiveShip generates code without executing it — the reviewer catches syntax issues but not subtle logic errors |
| Single-developer productivity | Copilot ($10/month unlimited) | For one developer writing code in an IDE, Copilot is cheaper and better. HiveShip adds nothing here |
| UI/frontend work requiring visual preview | Firebase Studio, Cursor, v0 | HiveShip has no visual rendering capability |

---

## What HiveShip Is NOT

| HiveShip is NOT | Because |
|:------|:--------|
| A replacement for senior developers | It cannot make architectural decisions, negotiate trade-offs, or understand unstated business context |
| An IDE or pair programmer | It's headless, fire-and-forget. Use Claude Code or Copilot if you need back-and-forth interaction |
| A CI/CD system | It generates code and opens PRs. It does not build, test, or deploy |
| Safe for security-critical code without human review | The AI reviewer catches common issues but is not a substitute for a human security audit |
| A product competing with Copilot | They solve different problems. Copilot helps a developer at a keyboard. HiveShip works when nobody is at a keyboard |
