import logging
from pathlib import Path
import click
from .version import __version__
from .buildkml import import_geojson, build_kml

LOG_FORMAT = "%(asctime)s %(levelname)-8s %(message)s"


@click.command()
@click.version_option(version=__version__, prog_name="geojson2kml")
@click.argument("geojsonfile", type=click.Path(exists=True))
@click.option("-v", "--verbose", is_flag=True, help="Will print verbose messages.")
@click.option(
    "--outdir",
    "-o",
    type=click.Path(exists=True),
    default=".",
    help="The output folder to save to",
)
def main(geojsonfile, verbose, outdir):
    """geojson2kml

    Convert GeoJSON to KML file
    """
    if verbose:
        logging.basicConfig(level="DEBUG", format=LOG_FORMAT)
    else:
        logging.basicConfig(level="INFO", format=LOG_FORMAT)

    geojson = import_geojson(geojsonfile)
    stem = Path(geojsonfile).stem
    output_path = Path(outdir) / f"{stem}.kml"
    build_kml(geojson, output_path)
