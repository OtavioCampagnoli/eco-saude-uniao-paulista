from __future__ import annotations

from dataclasses import dataclass

from app.domain.models import Inspection, ItemStatus
from app.domain.scoring import score_inspection


@dataclass(frozen=True)
class DashboardMetrics:
    total_inspections: int
    issues_by_status: dict[str, int]
    score_by_sector: dict[str, int]
    top_problem_items: list[tuple[str, int]]


def aggregate_dashboard_metrics(inspections: list[Inspection]) -> DashboardMetrics:
    issues = {status.value: 0 for status in ItemStatus}
    sector_scores: dict[str, list[int]] = {}
    item_counts: dict[str, int] = {}

    for ins in inspections:
        issues[ItemStatus.OK.value] += sum(1 for i in ins.items if i.status == ItemStatus.OK)
        issues[ItemStatus.ATTENTION.value] += sum(
            1 for i in ins.items if i.status == ItemStatus.ATTENTION
        )
        issues[ItemStatus.CRITICAL.value] += sum(
            1 for i in ins.items if i.status == ItemStatus.CRITICAL
        )

        sector_scores.setdefault(ins.sector, []).append(score_inspection(ins))

        for it in ins.items:
            if it.status != ItemStatus.OK:
                item_counts[it.name] = item_counts.get(it.name, 0) + 1

    score_by_sector = {
        sector: int(round(sum(scores) / len(scores))) for sector, scores in sector_scores.items()
    }

    top_problem_items = sorted(item_counts.items(), key=lambda x: x[1], reverse=True)[:10]

    return DashboardMetrics(
        total_inspections=len(inspections),
        issues_by_status=issues,
        score_by_sector=dict(sorted(score_by_sector.items(), key=lambda x: x[0].lower())),
        top_problem_items=top_problem_items,
    )