"""Workbook discovery tests."""

from pathlib import Path

from handicraft_export_intelligence.ingestion.workbook_discovery import (
    discover_workbooks,
    district_from_workbook,
)


def test_discover_workbooks_finds_xlsx_recursively(tmp_path: Path) -> None:
    data_dir = tmp_path / "data"
    nested_dir = data_dir / "nested"
    nested_dir.mkdir(parents=True)
    first = data_dir / "Ajmer.xlsx"
    second = nested_dir / "Jaipur.xlsx"
    temp_file = data_dir / "~$Ignored.xlsx"
    text_file = data_dir / "notes.txt"

    first.touch()
    second.touch()
    temp_file.touch()
    text_file.touch()

    assert discover_workbooks(data_dir) == (first, second)


def test_district_from_workbook_uses_file_stem() -> None:
    assert district_from_workbook(Path("data/Sri Ganganagar.xlsx")) == "Sri Ganganagar"
