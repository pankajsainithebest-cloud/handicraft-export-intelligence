# Rajasthan Handicraft Export Intelligence Platform

Professional Python platform for building export intelligence from Rajasthan
Government Handicraft portal artisan data.

Sprint 1 establishes the project foundation only. It does not implement
ingestion, normalization, validation, analytics, scoring, reporting, or
procurement logic.

## Source Data

The source dataset consists of 33 Rajasthan district Excel workbooks stored in
`data/`. These workbooks are part of the repository and must not be moved by
application code.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## CLI

```powershell
hei --help
hei info
```

Placeholder commands are available for future sprints:

- `hei validate`
- `hei build-master`
- `hei analyze`
- `hei intelligence`
- `hei report`

## Development

```powershell
ruff format .
ruff check .
mypy
pytest
```

## Layout

```text
src/handicraft_export_intelligence/
  ingestion/
  normalization/
  validation/
  models/
  repositories/
  services/
  analytics/
  intelligence/
  reporting/
```

Configuration lives in `config/`. Documentation lives in `docs/`. Tests live in
`tests/`.
