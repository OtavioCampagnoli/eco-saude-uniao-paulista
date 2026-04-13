from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Annotated
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class ItemStatus(str, Enum):
    OK = "OK"
    ATTENTION = "ATENÇÃO"
    CRITICAL = "CRÍTICO"


class InspectionItem(BaseModel):
    name: Annotated[str, Field(min_length=2, max_length=80)]
    status: ItemStatus
    comment: str | None = Field(default=None, max_length=200)


class Inspection(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    school_name: str = Field(default="União Paulista", min_length=2, max_length=120)
    sector: Annotated[str, Field(min_length=2, max_length=80)]
    items: list[InspectionItem] = Field(default_factory=list)
    notes: str | None = Field(default=None, max_length=500)