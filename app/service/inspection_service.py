from __future__ import annotations

from app.domain.metrics import DashboardMetrics, aggregate_dashboard_metrics
from app.domain.models import Inspection
from app.domain.recommendations import generate_recommendations
from app.infra.repository import InspectionRepository


class InspectionService:
    def __init__(self, repo: InspectionRepository) -> None:
        self._repo = repo

    def create_inspection(self, inspection: Inspection) -> None:
        self._repo.add(inspection)

    def list_inspections(self) -> list[Inspection]:
        return self._repo.list()

    def get_dashboard_metrics(self) -> DashboardMetrics:
        return aggregate_dashboard_metrics(self.list_inspections())

    def get_recommendations_for(self, inspection: Inspection) -> list[str]:
        return generate_recommendations(inspection)