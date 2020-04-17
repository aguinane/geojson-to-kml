import os
import sys
import pytest
from click.testing import CliRunner

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from geojson2kml.cli import main


@pytest.fixture
def runner():
    return CliRunner()


def test_cli(runner):
    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0
    assert not result.exception
    assert "geojson2kml" in result.output.strip()
