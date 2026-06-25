"""Typed application settings loaded from YAML."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ConfigDict, Field

from handicraft_export_intelligence.constants import DEFAULT_CONFIG_PATH
from handicraft_export_intelligence.exceptions import ConfigurationError


class ProjectSettings(BaseModel):
    """Project identity and runtime environment."""

    model_config = ConfigDict(frozen=True)

    name: str
    environment: str = "development"


class PathSettings(BaseModel):
    """Application path settings."""

    model_config = ConfigDict(frozen=True)

    data_dir: Path
    config_dir: Path
    docs_dir: Path
    logs_dir: Path
    output_dir: Path
    reports_dir: Path
    raw_workbook_dir: Path


class ExcelSettings(BaseModel):
    """Excel workbook conventions."""

    model_config = ConfigDict(frozen=True)

    no_details_sheet: str = "No Details"
    required_columns: tuple[str, ...] = Field(default_factory=tuple)


class MasterDatasetSettings(BaseModel):
    """Expected output paths for generated master datasets."""

    model_config = ConfigDict(frozen=True)

    master_artisan: Path
    master_skill: Path
    master_craft: Path
    master_district: Path
    no_details: Path


class Settings(BaseModel):
    """Complete platform settings."""

    model_config = ConfigDict(frozen=True)

    project_root: Path
    project: ProjectSettings
    paths: PathSettings
    excel: ExcelSettings
    master_datasets: MasterDatasetSettings


def get_project_root() -> Path:
    """Return the repository root inferred from the package location."""

    return Path(__file__).resolve().parents[2]


def load_settings(config_path: str | Path | None = None) -> Settings:
    """Load typed settings from YAML configuration."""

    root = get_project_root()
    selected_config = (
        config_path
        if config_path is not None
        else os.getenv("HEI_CONFIG_PATH", str(DEFAULT_CONFIG_PATH))
    )
    selected_path = Path(selected_config)
    if not selected_path.is_absolute():
        selected_path = root / selected_path

    if not selected_path.exists():
        raise ConfigurationError(f"Configuration file not found: {selected_path}")

    with selected_path.open("r", encoding="utf-8") as config_file:
        raw_config = yaml.safe_load(config_file) or {}

    if not isinstance(raw_config, dict):
        raise ConfigurationError("Configuration file must contain a YAML mapping.")

    normalized_config = _resolve_path_fields(raw_config, root)
    return Settings(project_root=root, **normalized_config)


def _resolve_path_fields(raw_config: dict[str, Any], root: Path) -> dict[str, Any]:
    config = dict(raw_config)
    config["paths"] = _resolve_mapping_paths(
        dict(config.get("paths", {})),
        root,
        fields={
            "data_dir",
            "config_dir",
            "docs_dir",
            "logs_dir",
            "output_dir",
            "reports_dir",
            "raw_workbook_dir",
        },
    )
    config["master_datasets"] = _resolve_mapping_paths(
        dict(config.get("master_datasets", {})),
        root,
        fields={
            "master_artisan",
            "master_skill",
            "master_craft",
            "master_district",
            "no_details",
        },
    )
    return config


def _resolve_mapping_paths(
    values: dict[str, Any],
    root: Path,
    fields: set[str],
) -> dict[str, Any]:
    for field in fields:
        if field in values:
            values[field] = _resolve_path(root, values[field])
    return values


def _resolve_path(root: Path, value: object) -> Path:
    path = Path(str(value))
    if path.is_absolute():
        return path
    return root / path
