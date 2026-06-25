"""Raw sheet parser tests."""

from openpyxl import Workbook

from handicraft_export_intelligence.ingestion.sheet_parser import (
    classify_sheet,
    parse_product_sheet,
)


def test_classify_sheet_identifies_no_details_case_insensitively() -> None:
    assert classify_sheet("No Details", "No Details") == "no_details"
    assert classify_sheet("no details", "No Details") == "no_details"
    assert classify_sheet("Blue Pottery", "No Details") == "product"


def test_parse_product_sheet_preserves_source_metadata() -> None:
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Blue Pottery"
    worksheet.append(["ArtisanId", "Name"])
    worksheet.append(["A-1", "Meera"])

    parsed = parse_product_sheet(
        worksheet=worksheet,
        workbook="Ajmer.xlsx",
        district="Ajmer",
    )

    assert parsed.metadata.sheet == "Blue Pottery"
    assert parsed.metadata.parsed_data_rows == 1
    assert parsed.rows[0]["ArtisanId"] == "A-1"
    assert parsed.rows[0]["_source_workbook"] == "Ajmer.xlsx"
    assert parsed.rows[0]["_source_district"] == "Ajmer"
    assert parsed.rows[0]["_source_sheet"] == "Blue Pottery"
    assert parsed.rows[0]["_source_row_number"] == 2
