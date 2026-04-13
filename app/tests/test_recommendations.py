from __future__ import annotations

from app.domain.models import Inspection, InspectionItem, ItemStatus
from app.domain.recommendations import generate_recommendations


def test_recommendation_for_leak_critical() -> None:
    ins = Inspection(
        sector="Pátio",
        items=[InspectionItem(name="Vazamento em torneiras", status=ItemStatus.CRITICAL)],
    )
    recs = generate_recommendations(ins)
    assert any("manutenção imediata" in r.lower() for r in recs)


def test_recommendation_for_no_soap() -> None:
    ins = Inspection(
        sector="Banheiros",
        items=[InspectionItem(name="Sem sabonete", status=ItemStatus.ATTENTION)],
    )
    recs = generate_recommendations(ins)
    assert any("repor sabonete" in r.lower() for r in recs)