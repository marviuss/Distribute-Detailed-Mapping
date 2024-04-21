import os

import requests
import json

# Define the Overpass QL query
# IMPORTANT: You can replace "Universiteit Twente" with desired location from OSM database.
overpass_url = "http://overpass-api.de/api/interpreter"
overpass_query = """
[out:json];
area[name="Universiteit Twente"]->.searchArea;
(
  // Select all ways (roads) within the specified area
  way(area.searchArea)[highway];
);
out geom;
"""


def query_osm():
    # Send the query to Overpass API
    response = requests.post(overpass_url, data=overpass_query)
    data = response.json()

    # Restructure the data into the desired GeoJSON format
    geojson = {
        "type": "FeatureCollection",
        "features": []
    }

    for element in data["elements"]:
        feature = {
            "id": element["id"],
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "LineString",
                "coordinates": [(node["lon"], node["lat"]) for node in element["geometry"]]
            }
        }
        if "tags" in element:
            feature["properties"] = element["tags"]
        geojson["features"].append(feature)

    current_directory = os.path.dirname(__file__) + "/jsons/"
    file_path = os.path.join(current_directory, "UT_Area_Roads.geojson")
    with open(file_path, "w") as f:
        json.dump(geojson, f)

    print("GeoJSON file has been generated.")