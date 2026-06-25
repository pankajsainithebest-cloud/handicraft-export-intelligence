"""Report writers for ingestion outputs."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from openpyxl import Workbook

from handicraft_export_intelligence.ingestion.models import (
    IngestionResult,
    SheetMetadata,
    WorkbookMetadata,
)


def write_ingestion_outputs(result: IngestionResult) -> None:
    """Write all ingestion inventory and summary outputs."""

    result.output_dir.mkdir(parents=True, exist_ok=True)
    _write_workbook_inventory(
        result.output_dir / "workbook_inventory.xlsx",
        result.workbook_inventory,
    )
    _write_sheet_inventory(
        result.output_dir / "sheet_inventory.xlsx",
        result.sheet_inventory,
    )
    _write_summary_json(result.output_dir / "ingestion_summary.json", result)
    _write_report_markdown(result.output_dir / "ingestion_report.md", result)


def _write_workbook_inventory(
    output_path: Path,
    inventory: tuple[WorkbookMetadata, ...],
) -> None:
    rows = [
        {
            **asdict(item),
            "path": str(item.path),
        }
        for item in inventory
    ]
    _write_xlsx(output_path, rows)


def _write_sheet_inventory(
    output_path: Path,
    inventory: tuple[SheetMetadata, ...],
) -> None:
    _write_xlsx(output_path, [asdict(item) for item in inventory])


def _write_xlsx(output_path: Path, rows: list[dict[str, Any]]) -> None:
    workbook = Workbook(write_only=True)
    worksheet = workbook.create_sheet("Inventory")

    headers = tuple(rows[0].keys()) if rows else ("message",)
    worksheet.append(headers)
    if rows:
        for row in rows:
            worksheet.append([row.get(header) for header in headers])
    else:
        worksheet.append(["No records found"])

    workbook.save(output_path)


def _write_summary_json(output_path: Path, result: IngestionResult) -> None:
    output_path.write_text(
        json.dumps(_summary_payload(result), indent=2),
        encoding="utf-8",
    )


def _write_report_markdown(output_path: Path, result: IngestionResult) -> None:
    payload = _summary_payload(result)
    failed_workbooks = [
        item for item in result.workbook_inventory if item.status == "error"
    ]

    lines = [
        "# Ingestion Report",
        "",
        "## Summary",
        "",
        f"- Workbooks discovered: {payload['workbooks_discovered']}",
        f"- Workbooks processed: {payload['workbooks_processed']}",
        f"- Workbooks failed: {payload['workbooks_failed']}",
        f"- Sheets discovered: {payload['sheets_discovered']}",
        f"- Product sheets: {payload['product_sheets']}",
        f"- No Details sheets: {payload['no_details_sheets']}",
        f"- Parsed product rows: {payload['parsed_product_rows']}",
        "",
    ]

    if failed_workbooks:
        lines.extend(["## Workbook Errors", ""])
        for workbook in failed_workbooks:
            lines.append(f"- `{workbook.workbook}`: {workbook.error}")
        lines.append("")

    output_path.write_text("\n".join(lines), encoding="utf-8")


def _summary_payload(result: IngestionResult) -> dict[str, int | str]:
    return {
        "output_dir": str(result.output_dir),
        "workbooks_discovered": len(result.workbook_inventory),
        "workbooks_processed": result.successful_workbooks,
        "workbooks_failed": result.failed_workbooks,
        "sheets_discovered": len(result.sheet_inventory),
        "product_sheets": result.product_sheet_count,
        "no_details_sheets": result.no_details_sheet_count,
        "parsed_product_rows": sum(
            sheet.metadata.parsed_data_rows for sheet in result.parsed_product_sheets
        ),
    }
