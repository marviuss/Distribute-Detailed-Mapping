import os

from shapely.geometry import LineString
import pyproj
import json

utm_proj = pyproj.Proj(proj="utm", zone=32, ellps="WGS84")

def convert_to_meters(coords):
    lon, lat = coords
    x, y = utm_proj(lon, lat)
    return x, y


def calculate_total_road_length(geojson_file_path):
    try:
        current_directory = os.path.dirname(__file__) + "/jsons/"
        with open(os.path.join(current_directory,geojson_file_path), "r") as geojson_file:
            data = json.load(geojson_file)

        features = data['features']
        total_length = 0
        list_of_coordinates = []

        for feature in features:
            feature_type = feature['geometry']['type']
            coordinates = feature['geometry']['coordinates']

            if feature_type == "LineString" and coordinates not in list_of_coordinates:
                coords_in_meters = [convert_to_meters(coord) for coord in coordinates]
                linestring_obj = LineString(coords_in_meters)
                if linestring_obj.is_valid:
                    length = linestring_obj.length
                    total_length += length
                else:
                    print("Invalid LineString geometry detected.")

            list_of_coordinates.append(coordinates)
        return total_length

    except Exception as e:
        print(f"An error occurred: {e}")
