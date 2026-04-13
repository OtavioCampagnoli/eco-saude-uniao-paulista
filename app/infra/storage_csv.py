from __future__ import annotations

import csv
import json
from pathlib import Path

from app.domain.models import Inspection, InspectionItem, ItemStatus
from app.infra.repository import InspectionRepository


class CsvInspectionRepository(InspectionRepository):
    def __init__(self, csv_path: str) -> None:
        self.path = Path(csv_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self._init_file()

    def _init_file(self) -> None:
        with self.path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["id", "created_at", "school_name", "sector", "notes", "items_json"],
            )
            writer.writeheader()

    def add(self, inspection: Inspection) -> None:
        row = {
            "id": str(inspection.id),
            "created_at": inspection.created_at.isoformat(),
            "school_name": inspection.school_name,
            "sector": inspection.sector,
            "notes": inspection.notes or "",
            "items_json": json.dumps([item.model_dump() for item in inspection.items], ensure_ascii=False),
        }
        with self.path.open("a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["id", "created_at", "school_name", "sector", "notes", "items_json"],
            )
            writer.writerow(row)

    def list(self) -> list[Inspection]:
        inspections: list[Inspection] = []
        with self.path.open("r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                items_raw = json.loads(row["items_json"]) if row.get("items_json") else []
                items = [
                    InspectionItem(
                        name=i["name"],
                        status=ItemStatus(i["status"]),
                        comment=i.get("comment"),
                    )
                    for i in items_raw
                ]
                inspections.append(
                    Inspection(
                        id=row["id"],
                        created_at=row["created_at"],
                        school_name=row["school_name"],
                        sector=row["sector"],
                        notes=row.get("notes") or None,
                        items=items,
                    )
                )
        return inspections