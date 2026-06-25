"""CLI smoke tests."""

from typer.testing import CliRunner

from handicraft_export_intelligence.cli import app


def test_cli_info_starts_successfully() -> None:
    runner = CliRunner()

    result = runner.invoke(app, ["info"])

    assert result.exit_code == 0
    assert "Rajasthan Handicraft Export Intelligence Platform" in result.stdout
