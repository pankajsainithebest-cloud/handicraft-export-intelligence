"""Workbook discovery for source Excel files."""

from __future__ import annotations

from pathlib import Path


def discover_workbooks(data_dir: Path) -> tuple[Path, ...]:
    """Discover source workbooks under the data directory."""

    workbooks = (
        path
        for path in data_dir.rglob("*.xlsx")
        if path.is_file() and not path.name.startswith("~$")
    )
    return tuple(sorted(workbooks, key=lambda item: str(item.relative_to(data_dir))))


def district_from_workbook(workbook_path: Path) -> str:
    """Infer the district name from the workbook filename."""

    return workbook_path.stem
