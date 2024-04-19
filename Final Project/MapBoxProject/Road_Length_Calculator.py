from shapely import Polygon
from shapely.geometry import shape, LineString
import json
import pyproj
import osmnx as ox

# Define the UTM projection (for example, UTM zone 32N for the Netherlands)
utm_proj = pyproj.Proj(proj="utm", zone=32, ellps="WGS84")

# This method converts a set of coordinaates to length in meters
def convert_to_meters(coords):
    lon, lat = coords
    x, y = utm_proj(lon, lat)
    return x, y

with open("result_4.geojson", "r") as geojson_file:
    data = json.load(geojson_file)



# Extract road network data using OSMnx
# Extract features from GeoJSON
features = data['features']
total_length = 0
list_of_coordinates = []


# Calculate total length of roads within file
for feature in features:
    # Extract geometry type and coordinates
    feature_type = feature['geometry']['type']
    coordinates = feature['geometry']['coordinates']

    if feature_type == "LineString" and coordinates not in list_of_coordinates:
        # Convert coordinates to meters
        coords_in_meters = [convert_to_meters(coord) for coord in coordinates]
        # Create a LineString object
        linestring_obj = LineString(coords_in_meters)
        # Ensure the LineString is valid
        if linestring_obj.is_valid:
            # Calculate length and add to total
            length = linestring_obj.length
            total_length += length
        else:
            print("Invalid LineString geometry detected.")

    list_of_coordinates.append(coordinates)

print("Total length of roads in the file:", round(total_length), "meters")
print("Or", round(total_length/1000,1), "kilometers")

