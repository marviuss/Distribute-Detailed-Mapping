import json
import os

from shapely.geometry import Point, shape
from collections import defaultdict

def find_dangerous_junctions(geojson_file_path):
    print('1')
    try:
        with open(geojson_file_path, "r") as geojson_file:
            geojson_data = json.load(geojson_file)
        print('2')
        endpoints = set()
        for feature in geojson_data["features"]:
            coords = shape(feature["geometry"]).coords
            endpoints.add(Point(coords[0]))
            endpoints.add(Point(coords[-1]))

        intersections = defaultdict(dict)
        for point in endpoints:
            intersecting_features = [f for f in geojson_data["features"] if shape(f["geometry"]).intersects(point)]
            if len(intersecting_features) > 1:  
                properties = {
                    "traffic_signals": any("traffic_signals" in f["properties"] for f in intersecting_features),
                    "maxspeed_more_than_40": any("maxspeed" in f["properties"] and f["properties"]["maxspeed"] and int(f["properties"]["maxspeed"]) > 40 for f in intersecting_features if "maxspeed" in f["properties"]),
                    "roundabout": any("junction" in f["properties"] and f["properties"]["junction"] == "roundabout" for f in intersecting_features),
                    "highway_trunk": any("highway" in f["properties"] and f["properties"]["highway"] == "trunk" for f in intersecting_features),
                    "highway_primary": any("highway" in f["properties"] and f["properties"]["highway"] == "primary" for f in intersecting_features),
                    "highway_secondary": any("highway" in f["properties"] and f["properties"]["highway"] == "secondary" for f in intersecting_features),
                    "highway_bus_stop": any("highway" in f["properties"] and f["properties"]["highway"] == "bus_stop" for f in intersecting_features),
                    "cycleway_opposite_lane": any("cycleway" in f["properties"] and f["properties"]["cycleway"] == "opposite_lane" for f in intersecting_features),
                    "cycleway_shared_lane": any("cycleway" in f["properties"] and f["properties"]["cycleway"] == "shared_lane" for f in intersecting_features),
                    "highway_crossing": any("highway" in f["properties"] and f["properties"]["highway"] == "crossing" for f in intersecting_features),
                    "highway_mini_roundabout": any("highway" in f["properties"] and f["properties"]["highway"] == "mini_roundabout" for f in intersecting_features),
                    "highway_motorway_junction": any("highway" in f["properties"] and f["properties"]["highway"] == "motorway_junction" for f in intersecting_features),
                    "highway_turning_circle": any("highway" in f["properties"] and f["properties"]["highway"] == "turning_circle" for f in intersecting_features),
                    "highway_turning_loop": any("highway" in f["properties"] and f["properties"]["highway"] == "turning_loop" for f in intersecting_features),
                }
                if any(properties.values()):
                    intersections[point] = properties

        feature_collection = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": point.__geo_interface__,
                    "properties": properties
                }
                for point, properties in intersections.items()
            ]
        }
        print('3')
        current_directory = os.path.dirname(__file__) + "/jsons/"
        file_path = os.path.join(current_directory, "dangerous_junctions_location.geojson")
        output_file_path = file_path
        with open(output_file_path, "w") as output_file:
            json.dump(feature_collection, output_file)

        print("Exported dangerous junctions as dangerous_junctions_location.geojson")
    except Exception as e:
        print(f"An error occurred: {e}")

