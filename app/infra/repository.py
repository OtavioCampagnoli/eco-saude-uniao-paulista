from __future__ import annotations

from typing import Protocol

from app.domain.models import Inspection


class InspectionRepository(Protocol):
    def add(self, inspection: Inspection) -> None: ...
    def list(self) -> list[Inspection]: ...