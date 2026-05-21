"""Smoke tests for korea-ai-basic-act-mcp."""
import sys, os, inspect, traceback
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import (
    classify_system_impact,
    check_genai_labelling_required,
    assess_business_type,
    get_obligations_checklist,
    sign_compliance_attestation,
    cross_walk_eu_ai_act,
    cross_walk_jp_ai_promotion,
)


def test_high_impact_for_healthcare_ai():
    r = classify_system_impact("AI diagnosis system for hospital patients, also reads medical records")
    assert r["impact_level"] == "HIGH_IMPACT"
    assert any(s in r["hit_sectors"] for s in ["healthcare", "medical", "hospital", "patient"])


def test_standard_impact_for_innocuous():
    r = classify_system_impact("AI recipe recommendation tool for home cooking")
    assert r["impact_level"] == "STANDARD"


def test_genai_labelling_required_for_deepfake():
    r = check_genai_labelling_required("deepfake video editor for entertainment")
    assert r["labelling_required"] is True


def test_genai_labelling_voluntary_for_normal():
    r = check_genai_labelling_required("internal Q&A bot for staff")
    assert r["labelling_required"] is False


def test_business_type_developer():
    r = assess_business_type("we train and release LLMs on HuggingFace")
    assert "AI development business operator" in r["business_types"]


def test_business_type_both():
    r = assess_business_type("we train models AND deploy them in customer-facing SaaS products")
    assert len(r["business_types"]) >= 2


def test_obligations_high_impact_developer():
    r = get_obligations_checklist("developer", "HIGH_IMPACT")
    assert len(r["checklist"]) >= 10
    assert any("MSIT" in c for c in r["checklist"])


def test_obligations_standard_utilization():
    r = get_obligations_checklist("utilization", "STANDARD")
    assert any("GenAI" in c or "users" in c for c in r["checklist"])


def test_attestation_signs():
    r = sign_compliance_attestation({"impact_level": "HIGH_IMPACT"})
    assert r["assessment_id"].startswith("krai_")
    assert len(r["signature"]) > 10


def test_cross_walk_eu():
    r = cross_walk_eu_ai_act({})
    assert any("Article 50" in m["eu"] for m in r["mappings"])
    assert any("Article 73" in m["eu"] for m in r["mappings"])


def test_cross_walk_jp():
    r = cross_walk_jp_ai_promotion({})
    assert "Japan" in r["standards"][1]


if __name__ == "__main__":
    g = dict(globals())
    fns = [v for k, v in g.items() if k.startswith("test_") and inspect.isfunction(v)]
    p = f = 0
    for fn in fns:
        try:
            fn(); print(f"✓ {fn.__name__}"); p += 1
        except Exception as e:
            print(f"✗ {fn.__name__}: {type(e).__name__}: {e}"); traceback.print_exc(); f += 1
    print(f"\n{p} passed, {f} failed")
