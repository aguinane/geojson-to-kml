import logging
from pathlib import Path

import typer

from . import convert_file

LOG_FORMAT = "%(asctime)s %(levelname)-8s %(message)s"
DEFAULT_DIR = Path(".")
app = typer.Typer()


@app.command()
def main(
    geojsonfile: Path,
    verbose: bool = typer.Option(False, "--verbose", "-v"),
    outdir: Path = typer.Option(
        DEFAULT_DIR, exists=True, file_okay=False, dir_okay=True, writable=True
    ),
):
    """Convert GeoJSON to KML file"""
    if verbose:
        logging.basicConfig(level="DEBUG", format=LOG_FORMAT)
    else:
        logging.basicConfig(level="INFO", format=LOG_FORMAT)
    convert_file(geojsonfile, outdir)
