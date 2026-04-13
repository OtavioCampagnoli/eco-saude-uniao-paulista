from __future__ import annotations

from app.domain.models import Inspection, InspectionItem, ItemStatus
from app.domain.scoring import score_inspection


def test_score_all_ok_is_100() -> None:
    ins = Inspection(
        sector="Banheiros",
        items=[
            InspectionItem(name="Item 1", status=ItemStatus.OK),
            InspectionItem(name="Item 2", status=ItemStatus.OK),
        ],
    )
    assert score_inspection(ins) == 100


def test_score_with_attention_and_critical_is_penalized() -> None:
    ins = Inspection(
        sector="Bebedouros",
        items=[
            InspectionItem(name="Item 1", status=ItemStatus.ATTENTION),
            InspectionItem(name="Item 2", status=ItemStatus.CRITICAL),
        ],
    )
    assert score_inspection(ins) == 65