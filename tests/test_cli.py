import pytest
from typer.testing import CliRunner

from geojson2kml.cli import app


@pytest.fixture
def runner():
    return CliRunner()


def test_cli_convert(runner):
    result = runner.invoke(app, ["examples/example1.geojson", "--outdir", "examples"])
    assert result.exit_code == 0
    assert not result.exception
