# geojson-to-kml

Convert GeoJSON to KML file

```shell
python -m geojson2kml "examples/example1.geojson" --outdir examples
```


### Styling

You can configure the styling of objects by adding these as properties on the feature:

| Property            | Default                                                    |
| ------------------- | ---------------------------------------------------------- |
| iconstyle.icon.href | https://maps.google.com/mapfiles/kml/paddle/red-circle.png |
| iconstyle.color     | ffff0000                                                   |
| iconstyle.scale     | 1.0                                                        |
| labelstyle.scale    | 1.0                                                        |
| linestyle.color     | ffff0000                                                   |
| linestyle.width     | 5                                                          |
| polystyle.color     | ffff0000                                                   |