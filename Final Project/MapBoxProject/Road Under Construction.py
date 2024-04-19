import json
import os

current_directory = os.path.dirname(__file__) + "/jsons/"
with open(os.path.join(current_directory, "UT_Area_Roads.geojson"), "r") as file:
    data = json.load(file)

# Create a filter for roads under construction
roads_under_construction = []
for feature in data['features']:
    properties = feature.get('properties', {})
    if 'highway' in properties and properties['highway'] == 'construction':
        roads_under_construction.append(feature)


geojson_data = {
    "type": "FeatureCollection",
    "features": roads_under_construction
}

with open(os.path.join(current_directory, "roads_under_construction.geojson"), "w") as output_file:
    json.dump(geojson_data, output_file)

print("Roads under construction have been extracted successfully.")
