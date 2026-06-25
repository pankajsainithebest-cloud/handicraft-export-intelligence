"""Settings loading tests."""

from pathlib import Path

from handicraft_export_intelligence.settings import load_settings


def test_load_settings_from_default_yaml() -> None:
    settings = load_settings()

    assert settings.project.name == "Rajasthan Handicraft Export Intelligence Platform"
    assert settings.paths.data_dir.name == "data"
    assert settings.paths.raw_workbook_dir == settings.project_root / "data"
    assert settings.excel.no_details_sheet == "No Details"
    assert "ArtisanId" in settings.excel.required_columns
    assert isinstance(settings.master_datasets.master_artisan, Path)
