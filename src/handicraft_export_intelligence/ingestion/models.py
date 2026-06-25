"""Data structures for workbook ingestion."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class WorkbookMetadata:
    """Metadata captured for a source workbook."""

    workbook: str
    district: str
    path: Path
    size_bytes: int
    modified_at: str
    sheet_count: int = 0
    status: str = "pending"
    error: str | None = None


@dataclass(frozen=True)
class SheetMetadata:
    """Metadata captured for one worksheet."""

    workbook: str
    district: str
    sheet: str
    sheet_type: str
    row_count: int
    column_count: int
    header_count: int
    parsed_data_rows: int
    status: str = "ok"
    error: str | None = None


@dataclass(frozen=True)
class ParsedProductSheet:
    """Raw product sheet rows with source metadata preserved."""

    metadata: SheetMetadata
    rows: tuple[dict[str, Any], ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class IngestionResult:
    """Complete result of an ingestion run."""

    workbook_inventory: tuple[WorkbookMetadata, ...]
    sheet_inventory: tuple[SheetMetadata, ...]
    parsed_product_sheets: tuple[ParsedProductSheet, ...]
    output_dir: Path

    @property
    def successful_workbooks(self) -> int:
        """Return the number of workbooks opened successfully."""

        return sum(item.status == "ok" for item in self.workbook_inventory)

    @property
    def failed_workbooks(self) -> int:
        """Return the number of workbooks that failed to open."""

        return sum(item.status == "error" for item in self.workbook_inventory)

    @property
    def product_sheet_count(self) -> int:
        """Return the number of product sheets discovered."""

        return sum(item.sheet_type == "product" for item in self.sheet_inventory)

    @property
    def no_details_sheet_count(self) -> int:
        """Return the number of No Details sheets discovered."""

        return sum(item.sheet_type == "no_details" for item in self.sheet_inventory)
