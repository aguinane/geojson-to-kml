import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from geojson2kml.buildkml import convert_file


def test_file_output():
    test_file = "examples/example1.geojson"
    outdir = "examples"
    output_path = convert_file(test_file, outdir)

    with open(output_path, "r") as f:
        data = f.read()
    assert "<kml xmlns=" in data
    assert "</kml>" in data
