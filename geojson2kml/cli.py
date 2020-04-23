import logging
import click
from .version import __version__
from .buildkml import convert_file

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
    convert_file(geojsonfile, outdir)
