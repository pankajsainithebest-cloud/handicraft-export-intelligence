# Architecture

The Rajasthan Handicraft Export Intelligence Platform is organized as a layered
Python application. Sprint 1 establishes package boundaries only; domain logic is
deferred to later sprints.

## Layers

- `ingestion`: source workbook discovery and reading.
- `normalization`: text, district, craft, contact, and field normalization.
- `validation`: schema and data quality validation.
- `models`: typed domain models.
- `repositories`: persistence and file access boundaries.
- `services`: application orchestration for master datasets.
- `analytics`: descriptive artisan, craft, district, women, and multiskill analysis.
- `intelligence`: export scoring, GI analysis, marketplace scoring, and recommendations.
- `reporting`: Excel reports, dashboards, and executive summaries.

## Data Policy

The 33 district Excel workbooks remain in `data/` as the source dataset. Sprint 1
does not move, edit, or transform them.
