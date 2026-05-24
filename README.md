# Korea AI Basic Act Compliance MCP

> ## 🧱 Part of the MEOK Governance Substrate (£499/mo)
> See [meok.ai/governance](https://meok.ai/governance).

# Korea AI Basic Act — in force since 22 January 2026

<!-- mcp-name: io.github.CSOAI-ORG/korea-ai-basic-act-mcp -->

[![PyPI](https://img.shields.io/pypi/v/korea-ai-basic-act-mcp)](https://pypi.org/project/korea-ai-basic-act-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## What this covers

The Republic of Korea's **Framework Act on the Development of AI and Establishment of a Foundation for Trustworthiness** — promulgated 21 January 2025, **in force since 22 January 2026** with a one-year MSIT grace on administrative fines (until 22 January 2027).

If you develop OR deploy AI products serving Korean users, you're in scope. Foreign businesses are explicitly covered.

## Tools

| Tool | Purpose |
|---|---|
| `classify_system_impact(description)` | Is this a "high-impact" AI system under the Act? |
| `check_genai_labelling_required(system_type)` | Is mandatory GenAI labelling required? |
| `assess_business_type(activities)` | AI developer vs utilisation operator (or both) |
| `get_obligations_checklist(business_type, impact_level)` | Full checklist |
| `sign_compliance_attestation(assessment)` | HMAC-signed MSIT-ready evidence |
| `cross_walk_eu_ai_act(assessment)` | Korea ↔ EU AI Act mapping |
| `cross_walk_jp_ai_promotion(assessment)` | Korea ↔ Japan parallel |

## Why this matters NOW

The Korea AI Basic Act came into force less than 4 months ago. Most Korean firms — and almost all foreign firms serving Korean users — are still scoping their obligations. The MSIT grace on administrative fines runs out 22 January 2027, but disclosure + GenAI labelling obligations apply NOW.

This MCP saves you the consultancy hours of mapping which obligations apply to your business type + impact level + GenAI use case.

## Sister MCPs

Part of the MEOK **Governance** pack:

- `eu-ai-act-compliance-mcp` — EU AI Act (cross-walks below)
- `iso-42005-impact-mcp` — for impact-assessment evidence
- `watermarking-authenticity-mcp` — for GenAI labelling (C2PA + invisible watermark)
- `ai-incident-reporting-mcp` — 5-clock incident chain

Full catalogue: [meok.ai/anthropic-registry](https://meok.ai/anthropic-registry)

## Protocol coverage + Universal PAYG

| Option | Price |
|---|---|
| Self-host MIT | £0 |
| Universal PAYG | £29/mo + £0.0002/call |
| Governance Substrate | £499/mo |
| Universe | £1,499/mo |
| Defence | £4,990/mo |

Buy: https://meok.ai/governance

## Wire it up — full stack

Pair this with the MEOK chain that turns one agent action into ONE signed compliance event:

1. **bft-progress-council-mcp** — anti-loop guardrail
2. **agent-token-budget-mcp** — hard spend cap
3. **agent-prompt-injection-firewall-mcp** — OWASP LLM01 scan
4. **agent-audit-logger-mcp** — hash-chained evidence
5. **a2a-governance-bridge-mcp** — fold N attestations → 1 signed event
6. **agent-incident-relay-mcp** — broadcast incidents to 5 regimes simultaneously

See [meok.ai/mcp-stack](https://meok.ai/mcp-stack) for the full architecture and [meok.ai/mcp-stack/demo](https://meok.ai/mcp-stack/demo) for the live in-browser demo.

## Licence

MIT. By [MEOK AI Labs](https://meok.ai) (CSOAI LTD, UK Companies House 16939677). Not legal advice — pair with qualified Korean counsel for production deployments.
