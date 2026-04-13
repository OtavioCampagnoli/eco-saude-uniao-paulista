from __future__ import annotations

from app.domain.models import Inspection, ItemStatus

PENALTIES: dict[ItemStatus, int] = {
    ItemStatus.OK: 0,
    ItemStatus.ATTENTION: -10,
    ItemStatus.CRITICAL: -25,
}


def score_inspection(inspection: Inspection) -> int:
    if not inspection.items:
        return 100

    total = 100 + sum(PENALTIES[item.status] for item in inspection.items)
    return max(0, min(100, total))