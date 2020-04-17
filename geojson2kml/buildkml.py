import logging
import geojson
import simplekml
from typing import List, Tuple

log = logging.getLogger(__name__)


def import_geojson(file_path):
    """ Get geojson object
    """
    with open(file_path) as f:
        return geojson.load(f)


def convert_coords(coords: List[List[float]]) -> List[Tuple[float, float]]:
    """ Change coords to tuples """
    if type(coords[0]) == float:
        # Single point
        lon, lat = coords
        return [(lon, lat)]
    new_coords = []
    if len(coords) == 0:
        coords = coords[0]
    for x in coords:
        new_coords.append((x[0], x[1]))
    return new_coords


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
            pnt.style.iconstyle.color = properties.get("iconstyle.color", "ffffffff")
            pnt.style.iconstyle.scale = properties.get("iconstyle.scale", 1.0)
            pnt.style.labelstyle.scale = properties.get("labelstyle.scale", 1.0)
        elif geometry["type"] == "MultiLineString":
            ls = kml.newlinestring(name=feature_name, coords=coords, description=desc)
            ls.style.linestyle.color = properties.get("linestyle.color", "ffffffff")
            ls.style.linestyle.width = properties.get("linestyle.width", 5)
        elif geometry["type"] == "Polygon":
            kml.newlinestring(name=feature_name, coords=coords, description=desc)
            pol = kml.newpolygon(
                name=feature_name, outerboundaryis=coords, innerboundaryis=coords
            )
            pol.style.linestyle.color = properties.get("linestyle.color", "ffffffff")
            pol.style.linestyle.width = properties.get("linestyle.width", 5)
            pol.style.polystyle.color = properties.get("polystyle.color", "ffffffff")
        else:
            log.warning("Geometry type %s not supported", geometry["type"])

    kml.save(output_path)
    log.info("Created %s", output_path)


def get_popup_table(properties: dict) -> str:
    """ Convert any additional columns into a HTML table """
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
