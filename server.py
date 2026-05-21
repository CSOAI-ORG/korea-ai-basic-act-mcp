#!/usr/bin/env python3
"""
Korea AI Basic Act Compliance MCP
==================================

By MEOK AI Labs · https://meok.ai · MIT
<!-- mcp-name: io.github.CSOAI-ORG/korea-ai-basic-act-mcp -->

WHAT THIS COVERS
----------------
The Republic of Korea's Framework Act on the Development of Artificial
Intelligence and Establishment of a Foundation for Trustworthiness
(commonly: AI Basic Act / AI Framework Act).

- Promulgated 21 January 2025
- IN FORCE since 22 January 2026 (one-year transition period)
- Administered by MSIT (Ministry of Science and ICT)
- One-year grace period on administrative fines, but obligations apply now

KEY OBLIGATIONS
---------------
1. High-impact AI systems (healthcare, energy, public services, infrastructure)
   require specific safety + transparency measures
2. Generative AI MUST be labeled (mandatory disclosure for certain applications)
3. AI development AND AI utilization businesses are both covered
4. National AI Committee oversight + 3-year basic AI plan
5. Disclosure obligations for some AI systems
6. Cross-border applicability for businesses serving Korean users

TOOLS
-----
- classify_system_impact(description): is this "high-impact" under the Act?
- check_genai_labelling_required(system_type): is mandatory labelling required?
- assess_business_type(activities): AI developer vs utilization operator
- get_obligations_checklist(business_type, impact_level): what to do
- sign_compliance_attestation(assessment): HMAC-signed evidence
- cross_walk_eu_ai_act(korea_assessment): Korea ↔ EU AI Act alignment
- cross_walk_jp_ai_promotion(korea_assessment): Korea ↔ Japan parallel

PRICING
-------
Free MIT self-host · £29/mo Starter · £79/mo Pro · Governance Substrate
£499/mo · Universe £1,499/mo. For Korean firms hitting the 22 Jan 2026
deadline: pays for itself in one consultancy-hour avoided.
"""

from __future__ import annotations
import hashlib
import hmac
import json
import os
import time
from datetime import datetime, timezone
from typing import Optional
from mcp.server.fastmcp import FastMCP


mcp = FastMCP("korea-ai-basic-act")

_HMAC_SECRET = os.environ.get("MEOK_HMAC_SECRET", "")


HIGH_IMPACT_SECTORS = [
    "healthcare", "medical", "hospital", "patient",
    "energy", "electricity", "grid", "nuclear",
    "public", "government", "civic", "municipality",
    "infrastructure", "transportation", "rail",
    "financial", "banking", "credit",
    "education", "school", "student",
    "judicial", "law-enforcement", "court",
    "safety", "emergency",
]


GENAI_LABEL_REQUIRED_APPLICATIONS = [
    "deepfake", "synthetic media", "generated image", "generated video",
    "generated audio", "generated text", "ai-written", "ai-created",
    "voice cloning", "face swap", "translation", "summarization-publication",
    "news-generation", "advertising-creative",
]


def _sign(payload: dict) -> str:
    if not _HMAC_SECRET:
        return "unsigned-no-key-configured"
    return hmac.new(_HMAC_SECRET.encode(), json.dumps(payload, sort_keys=True).encode(), hashlib.sha256).hexdigest()


def _ts() -> str:
    return datetime.now(timezone.utc).isoformat()


# ────────────────────────────────────────────────────────────────────────
# Tools
# ────────────────────────────────────────────────────────────────────────

@mcp.tool()
def classify_system_impact(description: str) -> dict:
    """
    Classify whether an AI system is "high-impact" under the Korea AI Basic Act.

    Args:
        description: Free-text description of the AI system + intended use.

    Returns:
        {impact_level, hit_sectors, obligations_count, signed}
    """
    text = description.lower()
    hit = [s for s in HIGH_IMPACT_SECTORS if s in text]
    if len(hit) >= 2:
        impact = "HIGH_IMPACT"
    elif len(hit) == 1:
        impact = "POTENTIALLY_HIGH_IMPACT"
    else:
        impact = "STANDARD"

    obligation_count = {"HIGH_IMPACT": 12, "POTENTIALLY_HIGH_IMPACT": 8, "STANDARD": 4}[impact]
    payload = {
        "act": "Republic of Korea AI Basic Act (Framework Act on AI Development)",
        "in_force_since": "2026-01-22",
        "description": description[:300],
        "impact_level": impact,
        "hit_sectors": hit,
        "obligations_count": obligation_count,
        "grace_period_admin_fines": "Until 2027-01-22 (1-year MSIT grace)",
        "ts": _ts(),
    }
    return {**payload, "signature": _sign(payload), "verify_url": "https://verify.meok.ai"}


@mcp.tool()
def check_genai_labelling_required(system_type: str) -> dict:
    """
    Check whether mandatory GenAI labelling applies under the Korea AI Basic Act.

    Args:
        system_type: Description of the generative output / use case.

    Returns:
        {required, matched_application_keywords, recommendation}
    """
    text = system_type.lower()
    hits = [k for k in GENAI_LABEL_REQUIRED_APPLICATIONS if k in text]
    required = len(hits) >= 1
    return {
        "labelling_required": required,
        "matched_application_keywords": hits,
        "recommendation": (
            "MUST label all generated content with a machine-readable + human-readable disclosure. "
            "Disclosure must identify the system as AI-generated and (where applicable) the underlying model."
            if required else
            "Voluntary labelling encouraged but not strictly mandated for this use case."
        ),
        "implementation_hint": "Use the meok watermarking-authenticity-mcp (C2PA manifest + invisible watermark + signed conformity attestation) — same MCP that satisfies EU AI Act Article 50.",
        "standard_reference": "Republic of Korea AI Basic Act (in force 22 Jan 2026)",
    }


@mcp.tool()
def assess_business_type(activities: str) -> dict:
    """
    Determine whether the business is an AI development operator or AI utilization
    operator (or both) under the Act.

    Args:
        activities: Free-text describing what the business does with AI.

    Returns:
        {types, obligations_overview}
    """
    t = activities.lower()
    is_developer = any(k in t for k in ["train", "develop", "build model", "fine-tune", "release model", "publish weights"])
    is_utilization = any(k in t for k in ["deploy", "use", "integrate", "incorporate", "embed", "serve users", "customer-facing", "saas"])

    types = []
    if is_developer:
        types.append("AI development business operator")
    if is_utilization:
        types.append("AI utilization business operator")
    if not types:
        types.append("Not yet in scope (re-assess if AI deployed at scale)")

    obligations = {
        "AI development business operator": [
            "Disclose model card + foreseeable misuse",
            "Maintain training-data provenance records",
            "Test for safety + bias before release",
            "Cooperate with MSIT inspections",
        ],
        "AI utilization business operator": [
            "Notify users of AI use (mandatory for some applications)",
            "GenAI labelling for synthetic content",
            "Maintain incident-response procedures",
            "Risk-based safety measures for high-impact systems",
        ],
    }
    overview = []
    for t_name in types:
        if t_name in obligations:
            overview.append({"type": t_name, "obligations": obligations[t_name]})

    return {
        "business_types": types,
        "obligations_overview": overview,
        "covered_by_act": is_developer or is_utilization,
        "note": "The Act applies broadly to anyone developing or commercially deploying AI in Korea, including foreign businesses serving Korean users.",
    }


@mcp.tool()
def get_obligations_checklist(business_type: str, impact_level: str = "STANDARD") -> dict:
    """
    Get the full obligations checklist for a business type + impact level.

    Args:
        business_type: "developer", "utilization", or "both".
        impact_level: "STANDARD", "POTENTIALLY_HIGH_IMPACT", or "HIGH_IMPACT".

    Returns:
        {checklist, deadline, fine_grace_until}
    """
    base = [
        "Designate an internal AI compliance contact",
        "Document AI system inventory + intended purposes",
        "Implement incident response procedure",
        "Maintain audit logs for AI decisions",
    ]
    high_impact_add = [
        "Submit notification of high-impact AI system to MSIT (where required)",
        "Perform impact assessment before deployment",
        "Maintain quarterly risk re-assessment",
        "Implement human oversight for irreversible decisions",
        "Pre-deployment safety testing + sign-off",
        "Maintain redress mechanism for affected users",
        "Disclose system existence + purpose to affected users (mandatory)",
        "Cooperate with National AI Committee evaluations",
    ]
    developer_add = [
        "Publish model card (capabilities + limitations + foreseeable misuse)",
        "Maintain training-data provenance (CycloneDX ML-BOM recommended)",
        "Disclose foundational data sources where commercially feasible",
    ]
    utilization_add = [
        "Notify users of AI involvement in user-facing decisions",
        "Apply GenAI labelling per mandatory categories",
        "Maintain procurement-side AI risk register",
    ]

    checklist = list(base)
    if impact_level in ("HIGH_IMPACT", "POTENTIALLY_HIGH_IMPACT"):
        checklist += high_impact_add
    if business_type in ("developer", "both"):
        checklist += developer_add
    if business_type in ("utilization", "both"):
        checklist += utilization_add

    return {
        "act": "Republic of Korea AI Basic Act",
        "in_force_since": "2026-01-22",
        "business_type": business_type,
        "impact_level": impact_level,
        "checklist": checklist,
        "fine_grace_until": "2027-01-22 (MSIT 1-year grace on administrative fines)",
        "next_step": "Run impact assessment via iso-42005-impact-mcp for ISO 42005 cross-walk evidence.",
    }


@mcp.tool()
def sign_compliance_attestation(assessment: dict) -> dict:
    """HMAC-sign a completed Korea-AI-Basic-Act assessment."""
    aid = f"krai_{int(time.time())}_{os.urandom(4).hex()}"
    payload = {
        "assessment_id": aid,
        "act": "Republic of Korea AI Basic Act",
        "in_force_since": "2026-01-22",
        "ts": _ts(),
        "impact_level": assessment.get("impact_level", "UNKNOWN"),
        "business_types": assessment.get("business_types", []),
    }
    sig = _sign(payload)
    return {
        "assessment_id": aid,
        "signature": sig,
        "verify_url": f"https://verify.meok.ai?assessment={aid}",
        "chain_entry": payload,
        "audit_value": "Use as MSIT inspection evidence + cross-jurisdictional compliance proof.",
    }


@mcp.tool()
def cross_walk_eu_ai_act(korea_assessment: dict) -> dict:
    """Map Korea AI Basic Act obligations to EU AI Act articles."""
    return {
        "standards": ["Korea AI Basic Act", "EU AI Act (Regulation (EU) 2024/1689)"],
        "mappings": [
            {"korea": "High-impact AI system measures", "eu": "Article 6 + Annex III high-risk classification"},
            {"korea": "GenAI mandatory labelling", "eu": "Article 50 transparency obligations"},
            {"korea": "Incident response + AI safety", "eu": "Article 73 serious-incident reporting"},
            {"korea": "Risk-based safety measures", "eu": "Article 9 Risk Management System"},
            {"korea": "Training-data provenance", "eu": "Article 10 Data and Data Governance"},
            {"korea": "Human oversight for irreversible decisions", "eu": "Article 14 human oversight"},
            {"korea": "User notification of AI use", "eu": "Article 50 + Article 26 deployer obligations"},
        ],
        "audit_value": "EU + Korea evidence in one chain — minimises duplicate compliance work for firms serving both markets.",
    }


@mcp.tool()
def cross_walk_jp_ai_promotion(korea_assessment: dict) -> dict:
    """Map Korea AI Basic Act to the Japan AI Promotion Act (2025)."""
    return {
        "standards": ["Korea AI Basic Act (mandatory)", "Japan AI Promotion Act (honour-system)"],
        "mappings": [
            {"korea": "High-impact AI system measures (mandatory)", "japan": "Voluntary risk assessment under METI guidelines"},
            {"korea": "MSIT inspection cooperation", "japan": "Self-attestation to METI framework"},
            {"korea": "GenAI labelling (mandatory)", "japan": "Voluntary GenAI disclosure"},
            {"korea": "Administrative fines (after grace)", "japan": "Honour-system only — no fines"},
        ],
        "audit_value": "Korea is stricter; Japan implementation usually requires a Korea-grade approach by default for firms serving both.",
    }


if __name__ == "__main__":
    mcp.run()
