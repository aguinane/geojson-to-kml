import logging
from pathlib import Path
from collections.abc import Iterable

import geojson
import simplekml

log = logging.getLogger(__name__)


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


def build_kml(geojson: dict, output_path="out.kml"):
    kml = simplekml.Kml()
    try:
        features = geojson["features"]
    except KeyError:
        features = [geojson]
    for feature in features:
        feature_id = feature.get("id", None)
        feature_name = feature.get("name", str(feature_id))
        geometry = feature["geometry"]
        properties = feature["properties"]
        desc = get_popup_table(properties)
        coords = convert_coords(geometry["coordinates"])
        if geometry["type"] == "Point":
            pnt = kml.newpoint(name=str(feature_id), coords=coords, description=desc)
            pnt.style.iconstyle.icon.href = properties.get(
                "iconstyle.icon.href",
                "https://maps.google.com/mapfiles/kml/paddle/red-circle.png",
            )
            pnt.style.iconstyle.color = properties.get("iconstyle.color", "ffff0000")
            pnt.style.iconstyle.scale = properties.get("iconstyle.scale", 1.0)
            pnt.style.labelstyle.scale = properties.get("labelstyle.scale", 1.0)
        elif geometry["type"] == "LineString":
            ls = kml.newlinestring(name=feature_name, description=desc)
            ls.coords = coords
            ls.extrude = 1
            ls.altitudemode = simplekml.AltitudeMode.relativetoground
            ls.style.linestyle.color = properties.get("linestyle.color", "ffff0000")
            ls.style.linestyle.width = properties.get("linestyle.width", 5)
        elif geometry["type"] == "Polygon":
            pol = kml.newpolygon(name=feature_name, description=desc)
            pol.outerboundaryis = coords
            pol.style.linestyle.color = properties.get("linestyle.color", "ffff0000")
            pol.style.linestyle.width = properties.get("linestyle.width", 5)
            pol.style.polystyle.color = properties.get("polystyle.color", "ffff0000")
        else:
            log.warning("Geometry type %s not supported", geometry["type"])

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
        row = f"<dt>{key}</dt><dd>{value}</dd>"
        html += row
    return html


def convert_file(geojsonfile, outdir):
    geojson = import_geojson(geojsonfile)
    stem = Path(geojsonfile).stem
    output_path = Path(outdir) / f"{stem}.kml"
    build_kml(geojson, output_path)
    return output_path
