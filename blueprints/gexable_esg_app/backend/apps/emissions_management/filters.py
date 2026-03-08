from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from django.db.models import QuerySet

from .models import EmissionRecord


@dataclass
class EmissionRecordFilter:
    scope_code: Optional[str] = None
    source_type: Optional[str] = None

    def apply(self, queryset: QuerySet[EmissionRecord]) -> QuerySet[EmissionRecord]:
        if self.scope_code:
            queryset = queryset.filter(source__scope_classification__code=self.scope_code)
        if self.source_type:
            queryset = queryset.filter(source__source_type=self.source_type)
        return queryset
