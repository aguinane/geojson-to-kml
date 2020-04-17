"""
    geojson2kml
    ~~~~~
    Convert GeoJSON to KML file
"""

import logging
from logging import NullHandler

from .version import __version__

# Set default logging handler to avoid "No handler found" warnings.
logging.getLogger(__name__).addHandler(NullHandler())
