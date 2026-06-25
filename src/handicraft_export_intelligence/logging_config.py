"""Logging configuration utilities."""

from __future__ import annotations

import logging.config
import os
from pathlib import Path
from typing import Any

import yaml

from handicraft_export_intelligence.constants import DEFAULT_LOGGING_CONFIG_PATH
from handicraft_export_intelligence.exceptions import ConfigurationError
from handicraft_export_intelligence.settings import get_project_root


def configure_logging(config_path: str | Path | None = None) -> None:
    """Configure logging from YAML."""

    root = get_project_root()
    selected_config = (
        config_path
        if config_path is not None
        else os.getenv("HEI_LOGGING_CONFIG_PATH", str(DEFAULT_LOGGING_CONFIG_PATH))
    )
    selected_path = Path(selected_config)
    if not selected_path.is_absolute():
        selected_path = root / selected_path

    if not selected_path.exists():
        raise ConfigurationError(
            f"Logging configuration file not found: {selected_path}"
        )

    with selected_path.open("r", encoding="utf-8") as config_file:
        raw_config = yaml.safe_load(config_file) or {}

    if not isinstance(raw_config, dict):
        raise ConfigurationError("Logging configuration must contain a YAML mapping.")

    config = _normalize_logging_paths(raw_config, root)
    logging.config.dictConfig(config)


def _normalize_logging_paths(config: dict[str, Any], root: Path) -> dict[str, Any]:
    normalized = dict(config)
    handlers = normalized.get("handlers", {})
    if not isinstance(handlers, dict):
        return normalized

    for handler in handlers.values():
        if not isinstance(handler, dict) or "filename" not in handler:
            continue
        log_path = Path(str(handler["filename"]))
        if not log_path.is_absolute():
            log_path = root / log_path
        log_path.parent.mkdir(parents=True, exist_ok=True)
        handler["filename"] = str(log_path)

    return normalized
