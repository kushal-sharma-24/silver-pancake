# HiveShip — Business Case

## The Problem

Service companies bill for developer time, but margins are shrinking. Clients demand faster delivery, competitive bids drive rates down, and developers are expensive. AI coding tools (Copilot, Claude Code) help individual developers write code faster — but they don't change team-level economics. A developer with Copilot is still one developer. They still context-switch, still review PRs manually, still spend time on boilerplate, and still can't work on two things at once.

The throughput bottleneck isn't typing speed. It's the overhead surrounding code production:

1. Boilerplate stories that take a full sprint slot but produce predictable output (log formatters, contract tests, K8s manifests, API scaffolds)
2. PR review comments that require the original developer to context-switch back, re-read the code, make the fix, and push
3. Fleet-wide mechanical changes (dependency bumps, compliance updates, migration patterns) that multiply linearly with the number of repos
4. Off-hours idle time where the codebase sits untouched

AI autocomplete tools accelerate coding (**step 1** of the lifecycle). They don't touch steps 2-4 because those require automation that runs without a developer at a keyboard.

## The Opportunity

HiveShip addresses the gap between "AI helps developers code faster" and "AI handles work when no developer is present." It's not a better Copilot — it's infrastructure for the work that happens around and between developer sessions.

## Who Is This For?

### Primary: Your Own Delivery Team (Internal Use)

| Scenario | Without HiveShip | With HiveShip |
|----------|------------------|---------------|
| 9-developer team, 8 sprints, Jul 7 deadline | 9 developers × 14 days × 8 sprints = 1,008 person-days | Same team + HiveShip automating boilerplate stories = ~850 effective person-days from 9 people |
| Boilerplate sprint stories (contract tests, log formatters, manifests) | 1 developer × 5-7 SP per sprint = ~6 days/sprint consumed | HiveShip generates PR, developer reviews (~1 hour). Saves 2-3 days/dev/sprint |
| PR review comments ("fix error handling in auth.py") | Developer context-switches back, re-reads code, makes fix, pushes. ~30 min per PR | Webhook triggers HiveShip, fix is pushed automatically. Developer stays on current work |
| Dependency bump across 30 services | 30 developers × 2 hours each = 60 person-hours, takes a week to coordinate | 1 HiveShip trigger → 30 PRs overnight. Developers review in the morning |

**The value:** A 9-person team delivers like an 11-12 person team while billing for 9. On a project billing at $800-1200/day per developer, **15-20% throughput improvement = $120,000-240,000 in additional margin per project.**

### Secondary: Managed Codebase Health for Existing Clients

You built the client's system. You know the codebase. HiveShip watches it and keeps it healthy:

- Dependency updates that actually fix the breaking changes (not just version bumps)
- Test coverage generation for untested modules
- Linting and style migrations applied consistently
- Security findings from Snyk/SonarQube fixed with actual code, not just alerts

**Revenue model:** $2,000-5,000/month per client as a managed service subscription. Recurring revenue on top of project revenue.

### Tertiary: Migration-as-a-Service

Legacy modernization contracts where HiveShip does the mechanical conversion:

- Java 8 → Java 21 (records, sealed classes, virtual threads)
- AngularJS → Angular 17 (standalone components)
- Synchronous Flask → async FastAPI
- Python 2 → Python 3

**Revenue model:** Win migration contracts at lower bids. HiveShip + 2 reviewers does in 3 months what traditionally takes a 6-person team 12 months. Charge $800K for work that previously cost $1.5M. Client saves 40%, you make more margin with fewer people.

### Quaternary: White-Label License to Peer Service Companies

Other service companies face the same margin pressure. License HiveShip as a "delivery accelerator" they deploy internally.

**Revenue model:** $10,000-30,000/year per licensee. They get the orchestrator, model integration, and pre-built strategies. You get recurring license revenue with zero COGS (they host it).

---

## Value Proposition

### Defensible metrics (honest)

| Metric | Estimate | Basis |
|--------|----------|-------|
| Throughput improvement on well-scoped tasks | 15-20% | Boilerplate automation + PR auto-fix + batch operations |
| Boilerplate stories automated per sprint | 2-4 stories (~10-20 SP) | Contract tests, log formatters, K8s manifests, API scaffolds |
| Time saved per PR review comment cycle | ~30 minutes per PR | Webhook auto-fix eliminates developer context-switch |
| Fleet-wide operation speedup | 10-50x | 1 trigger → N PRs overnight vs. N developers × 2 hours each |
| Margin improvement per project (9-person team) | $120K-240K | 15-20% throughput × $800-1200/day × 9 developers × 4 months |

### What we do NOT claim

| Inflated Claim | Reality |
|---------------|---------|
| "16-64x faster than developers" | HiveShip is faster for boilerplate. For complex features, a developer with Copilot is better. |
| "$0.01 per feature" | Only true with self-hosted LLM on pre-paid GPU. Real per-job cost: $0.04 (Gemini Flash) to $1.10 (Opus) |
| "400-80,000x cheaper" | Only if you compare frontier LLM cost against a senior developer's hourly rate. The comparison is misleading. |
| "Unbounded parallel scaling" | Max 8 agents per job, 4 concurrent threads. Real scaling is linear with number of jobs. |

### Qualitative value

1. **Consistency**: Every PR follows the same pipeline — plan → execute → review → fix. No "it depends on who wrote it."
2. **Auditability**: Full event log of every agent decision, every artifact, every review cycle. Every step is traceable.
3. **Off-hours productivity**: HiveShip runs on webhooks and cron. PRs appear overnight; developers review in the morning.
4. **LLM portability**: No vendor lock-in. Switch from Gemini to Ollama to vLLM without changing application code.

---

## Cost Analysis

### Per-job LLM costs (typical 6-agent job)

| LLM Provider | Cost per job | Jobs per day to break even vs. one A100 ($1,500/month) |
|---|---|---|
| Gemini 2.5 Flash | ~$0.04 | N/A — cheapest option, no GPU needed |
| Gemini 2.5 Pro | ~$0.30 | N/A |
| Claude Opus 4.6 | ~$1.10 | ~45 jobs/day |
| Self-hosted 30B on A100 | $0.00/job (fixed $1,500/month) | Breaks even at ~45 Opus-equivalent jobs/day |
| Self-hosted MoE 30B-A3B on 4090 | $0.00/job (one-time $1,600) | Pays for itself after ~1,500 Opus-equivalent jobs |

### Recommended approach

| Role | Model | Rationale |
|------|-------|-----------|
| Planner | Gemini Flash or Sonnet ($0.02/call) | Needs reasoning quality, but only 1-2 calls per job |
| Executor agents (×6) | Self-hosted 30B or MoE via Ollama ($0/call) | Pattern-heavy, low-reasoning tasks — quality is sufficient |
| Reviewer | Gemini Flash ($0.01/call) | Needs to catch errors, but structured output keeps it focused |
| Fixer | Self-hosted ($0/call) | Mechanical edits don't need frontier models |
| **Total per job** | **~$0.03** | Hybrid: frontier for planner, self-hosted for everything else |

### Why frontier-only is not viable

At $1.10/job (Opus) × 50 jobs/day = $55/day = **$1,650/month**. If you're charging $2,000/month for a managed codebase health subscription, your margin is $350. If the client has a bad month with 80 jobs, you lose money. Fixed-cost self-hosted inference is the only path to sustainable margins.

---

## What HiveShip Is NOT

| HiveShip is NOT | Because |
|:------|:--------|
| A replacement for senior developers | It cannot make architectural decisions, negotiate trade-offs, or understand unstated business context |
| An IDE or pair programmer | It's fire-and-forget, not interactive. Use Claude Code or Copilot for that |
| A product competing with Copilot | They solve different problems at different layers. Don't position against a $10/month tool backed by Microsoft |
| Suitable for security-critical code without review | The AI reviewer catches common issues but cannot replace a human security audit |
| A CI/CD system | It generates code. It does not build, test, or deploy (yet) |

---

## Revenue Model

| Model | Description | Target | Revenue Potential |
|-------|-------------|--------|-------------------|
| **Internal margin improvement** | Use HiveShip to make your delivery team faster. Don't sell the tool — sell faster delivery outcomes | Your own projects | $120-240K margin improvement per project |
| **Managed codebase health** | Monthly subscription for existing clients: dependency updates, test generation, security fixes | Clients whose systems you built | $2-5K/month per client |
| **Migration-as-a-service** | Win modernization contracts at lower bids using HiveShip + reviewers | CTOs with legacy codebases | $500K-3M per engagement |
| **White-label license** | License to peer service companies as a delivery accelerator | Other service companies | $10-30K/year per licensee |

**Primary strategy:** Don't sell HiveShip as a product. Sell your team's delivery, and use HiveShip as the internal engine that makes you faster and cheaper than competitors bidding on the same contract.

---

## Summary

HiveShip is not a new category of AI coding tool. The market has matured and multiple tools now do autonomous code generation. HiveShip's value is narrower but real: it's internal infrastructure that handles the work no IDE-based tool can — webhook-triggered PR revision, fleet-wide batch operations, CI-integrated auto-fix, and off-hours automation.

For a service company, the business case is straightforward: a 15-20% throughput improvement on a delivery team translates directly to margin. The tool is invisible to the client — they see PRs landing faster. You pocket the efficiency gain
| Reviewer | Gemini Flash ($0.01/call) | Needs to catch errors, but structured output keeps it focused |
| Fixer | Self-hosted ($0/call) | Mechanical edits don't need frontier models |
| **Total per job** | **~$0.03** | Hybrid: frontier for planner, self-hosted for everything else |

### Why frontier-only is not viable

At $1.10/job (Opus) × 50 jobs/day = $55/day = **$1,650/month**. If you're charging $2,000/month for a managed codebase health subscription, your margin is $350. If the client has a bad month with 80 jobs, you lose money. Fixed-cost self-hosted inference is the only path to sustainable margins.

---

## What HiveShip Is NOT

| HiveShip is NOT | Because |
|:------|:--------|
| A replacement for senior developers | It cannot make architectural decisions, negotiate trade-offs, or understand unstated business context |
| An IDE or pair programmer | It's fire-and-forget, not interactive. Use Claude Code or Copilot for that |
| A product competing with Copilot | They solve different problems at different layers. Don't position against a $10/month tool backed by Microsoft |
| Suitable for security-critical code without review | The AI reviewer catches common issues but cannot replace a human security audit |
| A CI/CD system | It generates code. It does not build, test, or deploy (yet) |

---

## Revenue Model

| Model | Description | Target | Revenue Potential |
|-------|-------------|--------|-------------------|
| **Internal margin improvement** | Use HiveShip to make your delivery team faster. Don't sell the tool — sell faster delivery outcomes | Your own projects | $120-240K margin improvement per project |
| **Managed codebase health** | Monthly subscription for existing clients: dependency updates, test generation, security fixes | Clients whose systems you built | $2-5K/month per client |
| **Migration-as-a-service** | Win modernization contracts at lower bids using HiveShip + reviewers | CTOs with legacy codebases | $500K-3M per engagement |
| **White-label license** | License to peer service companies as a delivery accelerator | Other service companies | $10-30K/year per licensee |

**Primary strategy:** Don't sell HiveShip as a product. Sell your team's delivery, and use HiveShip as the internal engine that makes you faster and cheaper than competitors bidding on the same contract.

---

## Summary

HiveShip is not a new category of AI coding tool. The market has matured and multiple tools now do autonomous code generation. HiveShip's value is narrower but real: it's internal infrastructure that handles the work no IDE-based tool can — webhook-triggered PR revision, fleet-wide batch operations, CI-integrated auto-fix, and off-hours automation.

For a service company, the business case is straightforward: a 15-20% throughput improvement on a delivery team translates directly to margin. The tool is invisible to the client — they see PRs landing faster. You pocket the efficiency gain.
