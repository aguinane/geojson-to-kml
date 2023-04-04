import logging
from collections.abc import Iterable
from pathlib import Path

import geojson
import simplekml

log = logging.getLogger(__name__)

DEFAULT_ICON = "http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png"
DEFAULT_COLOR = "FFFFFFFF"
DEFAULT_SCALE = 1.0
DEFAULT_WIDTH = 5.0


def import_geojson(file_path):
    """Get geojson object"""
    with open(file_path) as f:
        return geojson.load(f)


def convert_coords(coords: list[list[float]]) -> list[tuple[float, float]]:
    """Change coords to tuples"""
    if type(coords[0]) == float:
        # Single point
        return [parse_coords(coords)]
    new_coords = []
    for item in coords:
        if type(item[0]) == float:
            new_coords.append(parse_coords(item))
        else:
            for subitem in item:
                new_coords.append(parse_coords(subitem))
    return new_coords


def parse_coords(coords: Iterable[float]) -> tuple[float, float, float]:
    """Change coords to tuple"""
    lon = coords[0]
    lat = coords[1]
    try:
        alt = coords[2]
    except IndexError:
        alt = 0.0
    return lon, lat, alt


def build_kml(
    geojson: dict, output_path="", folder_attribute: str = "", zip: bool = False
):
    try:
        features = geojson["features"]
    except KeyError:
        features = [geojson]

    if not output_path:
        output_path = "out.kmz" if zip else "out.kml"

    # Get list of unique folders
    folders = []
    if folder_attribute:
        for feature in features:
            properties = feature["properties"]
            folder_name = properties.get(folder_attribute, None)
            if folder_name:
                folders.append(folder_name)
    folders = sorted(list(set(folders)))

    # Build KML tree
    kml = simplekml.Kml()
    targets = {}
    if folders:
        for folder in folders:
            fol = kml.newfolder(name=folder)
            targets[folder] = fol

    # Add features
    for feature in features:
        geometry = feature["geometry"]
        properties = feature["properties"]

        # Get the feature name
        feature_id = feature.get("id", None)
        feature_name = feature.get("name", None)
        if not feature_name:
            feature_name = properties.get("name", None)
        if not feature_name:
            feature_name = feature_id
        feature_name = str(feature_name)

        desc = get_popup_table(properties)
        coords = convert_coords(geometry["coordinates"])

        if folder_attribute:
            folder_name = properties.get(folder_attribute, None)
            if folder_name:
                target = targets[folder_name]
            else:
                target = kml
        else:
            target = kml

        if geometry["type"] == "Point":
            pnt = target.newpoint(name=feature_name, coords=coords, description=desc)
            pnt.style.iconstyle.icon.href = properties.get(
                "iconstyle.icon.href",
                DEFAULT_ICON,
            )
            pnt.style.iconstyle.color = properties.get("iconstyle.color", DEFAULT_COLOR)
            pnt.style.iconstyle.scale = properties.get("iconstyle.scale", DEFAULT_SCALE)
            pnt.style.labelstyle.scale = properties.get(
                "labelstyle.scale", DEFAULT_SCALE
            )
        elif geometry["type"] == "LineString":
            ls = target.newlinestring(name=feature_name, description=desc)
            ls.coords = coords
            ls.extrude = 1
            ls.altitudemode = simplekml.AltitudeMode.relativetoground
            ls.style.linestyle.color = properties.get("linestyle.color", DEFAULT_COLOR)
            ls.style.linestyle.width = properties.get("linestyle.width", DEFAULT_WIDTH)
        elif geometry["type"] == "Polygon":
            pol = target.newpolygon(name=feature_name, description=desc)
            pol.outerboundaryis = coords
            pol.style.linestyle.color = properties.get("linestyle.color", DEFAULT_COLOR)

            pol.style.linestyle.width = properties.get("linestyle.width", DEFAULT_WIDTH)
            pol.style.polystyle.color = properties.get("polystyle.color", DEFAULT_COLOR)
        else:
            log.warning("Geometry type %s not supported", geometry["type"])

    if zip:
        kml.savekmz(output_path)
    else:
        kml.save(output_path)
    log.info("Created %s", output_path)


def get_popup_table(properties: dict) -> str:
    """Convert any additional columns into a HTML table"""
    special = [
        "name",
        "iconstyle.icon.href",
        "iconstyle.color",
        "iconstyle.scale",
        "labelstyle.scale",
        "linestyle.color",
        "linestyle.width",
        "polystyle.color",
    ]
    for key in special:
        if key in properties:
            del properties[key]
    html = ""
    for key in properties.keys():
        value = properties[key]

        if isinstance(value, str) and value[0:4] == "http":
            value = f'<a href="{value}">{value}</a>'

        row = f"<dt>{key}</dt><dd>{value}</dd>"
        html += row
    return html


def convert_file(geojsonfile, outdir, folder_attribute: str = "", zip: bool = False):
    geojson = import_geojson(geojsonfile)
    stem = Path(geojsonfile).stem
    if zip:
        output_path = Path(outdir) / f"{stem}.kmz"
    else:
        output_path = Path(outdir) / f"{stem}.kml"
    build_kml(geojson, output_path, folder_attribute, zip=zip)
    return output_path
