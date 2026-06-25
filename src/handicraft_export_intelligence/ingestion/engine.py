"""Ingestion engine orchestration."""

from __future__ import annotations

import logging
from pathlib import Path

from handicraft_export_intelligence.ingestion.excel_reader import read_workbook
from handicraft_export_intelligence.ingestion.models import (
    IngestionResult,
    ParsedProductSheet,
    SheetMetadata,
    WorkbookMetadata,
)
from handicraft_export_intelligence.ingestion.reports import write_ingestion_outputs
from handicraft_export_intelligence.ingestion.workbook_discovery import (
    discover_workbooks,
)
from handicraft_export_intelligence.settings import Settings

logger = logging.getLogger(__name__)


def run_ingestion(settings: Settings, data_dir: Path | None = None) -> IngestionResult:
    """Run workbook ingestion and generate inventory outputs."""

    source_dir = data_dir or settings.paths.raw_workbook_dir
    output_dir = settings.paths.output_dir / "ingestion"
    logger.info("Starting ingestion: source_dir=%s", source_dir)

    workbook_inventory: list[WorkbookMetadata] = []
    sheet_inventory: list[SheetMetadata] = []
    parsed_product_sheets: list[ParsedProductSheet] = []

    for workbook_path in discover_workbooks(source_dir):
        workbook_metadata, sheet_metadata, parsed_sheets = read_workbook(
            workbook_path=workbook_path,
            no_details_sheet=settings.excel.no_details_sheet,
        )
        workbook_inventory.append(workbook_metadata)
        sheet_inventory.extend(sheet_metadata)
        parsed_product_sheets.extend(parsed_sheets)

    result = IngestionResult(
        workbook_inventory=tuple(workbook_inventory),
        sheet_inventory=tuple(sheet_inventory),
        parsed_product_sheets=tuple(parsed_product_sheets),
        output_dir=output_dir,
    )
    write_ingestion_outputs(result)
    logger.info(
        "Completed ingestion: workbooks=%s sheets=%s parsed_rows=%s",
        len(result.workbook_inventory),
        len(result.sheet_inventory),
        sum(sheet.metadata.parsed_data_rows for sheet in result.parsed_product_sheets),
    )
    return result
