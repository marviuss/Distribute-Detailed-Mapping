import json
import os

# Define wanted values for different filters
wanted_values = {
    "walking": ["path", "pedestrian", "cycleway", "footway", "living_street", "unclassified", "service", "services"],
    "footway": ["footway"],
    "cycleway": ["cycleway"],
    "path": ["path"],
    "living_street": ["living_street"],
    "unclassified": ["unclassified"],
    "residential": ["residential"],
    "service": ["service", "services"],
    "motorway": ["motorway"],
    "trunk": ["trunk"],
    "primary": ["primary"],
    "secondary": ["secondary"],
    "allononeroad": ["living_street", "unclassified", "residential", "service", "services", "path"],
    "cycling": ["cycleway", "path", "living_street", "residential", "unclassified", "service", "services", "living_street"],
    "car": ["motorway", "trunk", "primary", "secondary", "residential", "unclassified", "service", "services", "living_street"],
    "weird": ["path", "footway", "service", "services", "pedestrian", "cycleway", "trunk", "primary", "secondary", "motorway", "residential", "unclassified", "living_street"]
}

# Function to check if a feature is a LineString
def get_lines(entry):
    path_key = entry['geometry']['type']
    if path_key == 'LineString':
        return True
    else:
        return False

# Function to filter features based on highway values
def filter_function(entry, wanted_values):
    path_key = entry['properties']['highway']
    return path_key in wanted_values

# Function to combine results
def combine_results(result, paths):
    if result is None:
        result = paths
    else:
        result.extend(paths)
    return result

# Function to filter out features with duplicate IDs
def filter_duplicates(features):
    unique_ids = set()
    unique_features = []
    for feature in features:
        feature_id = feature['id']
        if feature_id not in unique_ids:
            unique_ids.add(feature_id)
            unique_features.append(feature)
    return unique_features

# Main function to create GeoJSON file with specified filters
def create_geojson(filters, input_geojson_file, output_geojson_file):
    current_directory = os.path.dirname(__file__)
    j = open(os.path.join(current_directory, input_geojson_file))
    data = json.load(j)
    # # Open input GeoJSON file
    # with open(input_geojson_file) as f:
    #     data = json.load(f)

    # Filter features to keep only LineString geometries
    data_features = [feature for feature in data['features'] if get_lines(feature)]
    result = None

    # Iterate over each filter
    for filter_name in filters:
        # Get the wanted values for the current filter
        filter_values = wanted_values.get(filter_name, [])
        # Filter features based on the current filter values
        paths = [entry for entry in data_features if filter_function(entry, filter_values)]
        # Combine filtered features with existing result
        result = combine_results(result, paths)

        # Filter out features with duplicate coordinates
    result = filter_duplicates(result)

    # Update data with filtered features
    if result is not None:
        data['features'] = result
    else:
        data['features'] = []

    # Write the result to the output GeoJSON file
    with open(output_geojson_file, "w") as outfile:
        json.dump(data, outfile, indent=4)


