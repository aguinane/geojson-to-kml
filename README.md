# geojson-to-kml

Convert GeoJSON to KML file

```shell
python -m geojson2kml "examples/example1.geojson" --outdir examples
```


### Display

The name of the feature will be taken from the `name` attribute if set, otherwise it will use the `id` of the feature. The attributes set in properites will be displayed as a table. 

```geojson
{
    "type": "Feature",
    "id": 1,
    "name": "ABBOTT NEIGHBORHOOD PARK",
    "geometry": {
        "type": "Point",
        "coordinates": [
            -80.870885,
            35.215151
        ]
    },
    "properties": {
        "name": "ABBOTT NEIGHBORHOOD PARK",
        "address": "1300  SPRUCE ST"
    }
}
```


### Folders

You can group features by folder by speciying `--folder-attribute` and the name of the property attribute that should be used to group by. 


### Styling

You can configure the styling of objects by adding these as properties on the feature:

| Property            | Default                                                    |
| ------------------- | ---------------------------------------------------------- |
| iconstyle.icon.href | https://maps.google.com/mapfiles/kml/paddle/red-circle.png |
| iconstyle.color     | FFFFFFFF                                                   |
| iconstyle.scale     | 1.0                                                        |
| labelstyle.scale    | 1.0                                                        |
| linestyle.color     | FFFFFFFF                                                   |
| linestyle.width     | 5                                                          |
| polystyle.color     | FFFFFFFF                                                   |