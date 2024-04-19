import pyproj
import requests
from shapely import LineString
from shapely.geometry import Polygon
import math
import json

# Define a function to query road data within a polygon
def get_roads_in_polygon(polygon):
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = f"""
        [out:json];
        way["highway"](poly:"{" ".join([f'{lat} {lon}' for lon, lat in polygon.exterior.coords])}");
        (._;>;);
        out;
        """
    response = requests.get(overpass_url, params={'data': overpass_query})
    data = response.json()
    # Print Overpass API query for debugging
    print("Overpass API query:", overpass_query)
    return data

# Define the coordinates of the University of Twente area polygon
ut_polygon_coords = [(6.844664, 52.252301), (6.852250, 52.252065), (6.852502, 52.248841),
                     (6.858270, 52.242783), (6.865331, 52.241921), (6.866303, 52.235225),
                     (6.859830, 52.234496), (6.843962, 52.240474), (6.845790, 52.249975),
                     (6.844283, 52.252300)]

# Create a Shapely Polygon object
ut_polygon = Polygon(ut_polygon_coords)

# Get road data within the University of Twente area polygon
road_data = get_roads_in_polygon(ut_polygon)

# Define the output GeoJSON structure
geojson_output = {
    "type": "FeatureCollection",
    "features": []
}

# Function to convert geographic coordinates to UTM meters
utm_proj = pyproj.Proj(proj="utm", zone=32, ellps="WGS84")
def convert_to_meters(coords):
    lon, lat = coords
    x, y = utm_proj(lon, lat)
    return x, y

# Calculate total road length and add road features to the GeoJSON structure
total_length = 0
for feature in road_data:
    if 'geometry' in feature:
        coords_in_meters = [convert_to_meters((node['lon'], node['lat'])) for node in feature['geometry']]
        linestring_obj = LineString(coords_in_meters)
        if linestring_obj.is_valid:
            length = linestring_obj.length
            total_length += length
            feature_geojson = {
                "type": "Feature",
                "properties": {"id": feature['id'], "tags": feature['tags']},
                "geometry": {
                    "type": "LineString",
                    "coordinates": [[lat, lon] for lon, lat in coords_in_meters]  # GeoJSON coordinates format
                }
            }
            geojson_output["features"].append(feature_geojson)
        else:
            print("Invalid LineString geometry detected.")

# Write GeoJSON output to file
with open("road_data.geojson", "w") as geojson_file:
    json.dump(geojson_output, geojson_file)

print("Total length of roads within the University of Twente area (in meters):", total_length)

print(get_roads_in_polygon(ut_polygon))