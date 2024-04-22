from flask import Flask, render_template, request, jsonify
import json
import filter_function
import os
import dijkstra_routing
import dangerous_junctions
import safest_route
import map_generation
import road_length_calculator

app = Flask(__name__, template_folder='template', static_folder='./static')
current_layer = None
#Directory where the jsons are located
current_directory = os.path.dirname(__file__) + "/jsons/"

#Method to fetch routes to frontend
@app.route('/load-route', methods=['GET'])
def load_route():
    global current_layer
    route_type = request.args.get('type')
    input_geojson_file = os.path.join(current_directory,'UT_Area_Roads.geojson')
    output_geojson_file = os.path.join(current_directory, f'{route_type}_route.geojson')
    
    try:
        if route_type == 'car':
            filter_function.create_geojson(["car"], input_geojson_file, output_geojson_file)
        elif route_type == 'cycling':
            filter_function.create_geojson(["cycling"], input_geojson_file, output_geojson_file)
        elif route_type == 'walking':
            filter_function.create_geojson(["walking"], input_geojson_file, output_geojson_file)
        elif route_type == 'walking-car':
            filter_function.create_geojson(["walking", "car"], input_geojson_file, output_geojson_file)
        elif route_type == 'walking-cycling':
            filter_function.create_geojson(["walking", "cycling"], input_geojson_file, output_geojson_file)
        elif route_type == 'cycling-car':
            filter_function.create_geojson(["cycling", "car"], input_geojson_file, output_geojson_file)
        current_layer = route_type

        with open(output_geojson_file) as f:
            data = json.load(f)
            #Adding coverage information to the json
            data["coverage"] = road_length_calculator.calculate_layer_coverage(input_geojson_file, output_geojson_file)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

#Method to fetch the shortest route to frontend
@app.route('/shortest-route', methods=['POST'])
def shortest_route():
    global current_layer
    g = dijkstra_routing.Graph()
    file_path = os.path.join(current_directory, f'{current_layer}_route.geojson')
    with open(file_path, "r") as file:
        geojson_data = json.load(file)
    for feature in geojson_data["features"]:
        if feature["geometry"]["type"] == "LineString":
            g.add_line_string(feature)

    data = request.json
    start_point = tuple(data['start_point'])  
    end_point = tuple(data['end_point'])
    if start_point not in g.vertices:
        start_point = g.find_closest_point(start_point)
    if end_point not in g.vertices:
        end_point = g.find_closest_point(end_point)

    shortest_path, total_distance = g.shortest_path(start_point, end_point)

    result_geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": shortest_path
                },
                "properties": {
                    "distance": total_distance
                }
            }
        ]
    }

    return jsonify({"shortest_route": result_geojson})

#Method to fetch the safest route to frontend
@app.route('/safest-route', methods=['POST'])
def safest_routing():
    global current_layer
    g = safest_route.Graph()
    file_path = os.path.join(current_directory, f'{current_layer}_route.geojson')
    with open(file_path, "r") as file:
        geojson_data = json.load(file)
    file_path1 = os.path.join(current_directory, "dangerous_junctions_location.geojson")    
    with open(file_path1, "r") as file:
        dangerous_junctions_data = json.load(file)

    dangerous_junctions = [tuple(junction["geometry"]["coordinates"]) for junction in dangerous_junctions_data["features"]]

    for feature in geojson_data["features"]:
        if feature["geometry"]["type"] == "LineString":
            g.add_line_string(feature)

    data = request.json
    start_point = tuple(data['start_point'])  
    end_point = tuple(data['end_point'])
    if start_point not in g.vertices:
        start_point = g.find_closest_point(start_point)
    if end_point not in g.vertices:
        end_point = g.find_closest_point(end_point)

    safest_path, total_dangerous_junctions = g.safest_path(start_point, end_point, dangerous_junctions)

    result_geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": safest_path
                },
                "properties": {
                    "dangerous_junctions": total_dangerous_junctions
                }
            }
        ]
    }

    return jsonify({"safest_route": result_geojson})

#Method to fetch dangerous junctions to frontend
@app.route('/get-dangerous-junctions', methods=['GET'])
def find_dangerous_junctions_endpoint():
    try:
        file_path = os.path.join(current_directory, 'UT_Area_Roads.geojson')
        dangerous_junctions.find_dangerous_junctions(file_path)
        output_file_path = os.path.join(current_directory, "dangerous_junctions_location.geojson")
        with open(output_file_path, "r") as output_file:
            data = json.load(output_file)
        return jsonify(data)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#fetch roads under construction
@app.route('/get-roads-under-construction', methods=['GET'])
def get_roads_under_construction():
    try:
        file_path = os.path.join(current_directory, 'roads_under_construction.geojson')
        with open(file_path, "r") as file:
            data = json.load(file)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/')  
def testing():
    map_generation.query_osm()
    return render_template('LoadingDataLayers.html')


if __name__ == '__main__':
    app.run(port = 8000, debug=True)
