import json
import os

import folium
import random
import math
import networkx as nx
from heapq import heappop, heappush

#Disclamer: this class is not connected to the main project, as we found out that Dijkstra algorithm outperforms A-star,
# but it's usable on it's own, just change coordinates in the main method and it will generate you an HTML with the route

def read_geojson(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

# Function to find the closest node in the graph to a given coordinate
def find_closest_node(graph, coord):
    min_distance = float('inf')
    closest_node = None
    for node in graph:
        distance = math.sqrt((node[0] - coord[0]) ** 2 + (node[1] - coord[1]) ** 2)
        if distance < min_distance:
            min_distance = distance
            closest_node = node
    return closest_node

# Function to connect disconnected components in the graph
def connect_disconnected_components(graph):
    nx_graph = nx.Graph(graph)  # Convert the graph to a networkx graph object

    connected_components = list(nx.connected_components(nx_graph))

    if len(connected_components) <= 1:
        # No disconnected components found
        return nx_graph

    for component in connected_components[1:]:
        # Connect component to the largest connected component
        largest_component = max(connected_components[0], key=len)
        nearest_node = min(largest_component, key=lambda node: min(
            nx_graph.nodes.get(node, {}).get('weight', float('inf')) for node in component))

        # Check if the nearest_node exists in the graph
        if nearest_node not in nx_graph.nodes:
            continue

        # Connect each node in the component to the nearest node in the largest component
        for node in component:
            nearest_node_distance = min(nx_graph.nodes.get(nearest_node, {}).get('weight', float('inf')), float('inf'))
            nx_graph.add_edge(node, nearest_node, weight=nearest_node_distance)

    return nx_graph


# Function to extract lines from GeoJSON data
def extract_lines(lines_data):
    lines = []
    for feature in lines_data['features']:
        geometry = feature['geometry']
        if geometry['type'] == 'LineString':
            switched_coordinates = [(coord[1], coord[0]) for coord in geometry['coordinates']]
            lines.append(switched_coordinates)
    return lines

# Function to create a graph from lines
def create_graph(lines):
    graph = {}
    for line in lines:
        for i in range(len(line) - 1):
            start = line[i]
            end = line[i + 1]
            if start not in graph:
                graph[start] = []
            if end not in graph:
                graph[end] = []
            graph[start].append(end)
            graph[end].append(start)  # Since it's an undirected graph, add both directions
    return graph

# A* algorithm to find the shortest path between two points in a graph
def astar(graph, start, goal):

    open_set = [(0, start)]
    came_from = {}
    g_score = {node: float('inf') for node in graph}
    g_score[start] = 0

    while open_set:
        current_cost, current_node = heappop(open_set)

        if current_node == goal:
            return reconstruct_path(came_from, goal)

        for neighbor in graph[current_node]:
            tentative_g_score = g_score[current_node] + calculate_distance(current_node, neighbor)
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current_node
                g_score[neighbor] = tentative_g_score
                f_score = tentative_g_score + heuristic(neighbor, goal)
                heappush(open_set, (f_score, neighbor))

    return None  # No path found

# Function to calculate Euclidean distance between two coordinates
def calculate_distance(coord1, coord2):
    return math.sqrt((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2)

# Heuristic function for A* algorithm
def heuristic(node, goal):
    return calculate_distance(node, goal)

# Function to reconstruct the path from the start node to the current node
def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return path[::-1]

# Function to switch coordinates (lat, lon) to (lon, lat) for LineString features
def switch_coordinates(geojson):
    for feature in geojson['features']:
        geometry = feature['geometry']
        if geometry['type'] == 'LineString':
            for i, coord in enumerate(geometry['coordinates']):
                geometry['coordinates'][i] = (coord[1], coord[0])
    return geojson

def main():
    # Read GeoJSON data
    current_directory = os.path.dirname(__file__) + "/jsons/"
    lines_data = read_geojson(os.path.join(current_directory,'UT_Area_Roads.geojson'))

    # Extract coordinates and lines
    lines = extract_lines(lines_data)

    # Select start and goal points
    start = (52.2368057, 6.854245)
    goal = (52.2412227, 6.847291)

    # Round coordinates to match precision
    start = tuple(map(lambda x: round(x, 7), start))
    goal = tuple(map(lambda x: round(x, 7), goal))

    print("Start:", start)
    print("Goal:", goal)

    # Create graph
    graph = create_graph(lines)

    print("Graph created with", len(graph), "nodes.")

    # Ensure start and goal are in the graph
    if start not in graph:
        start = find_closest_node(graph, start)
        print("Adjusted start coordinate to:", start)
    if goal not in graph:
        goal = find_closest_node(graph, goal)
        print("Adjusted goal coordinate to:", goal)

    if start not in graph or goal not in graph:
        print("Invalid start or goal coordinates.")
        return

    # Connect disconnected components
    graph = connect_disconnected_components(graph)

    # Find the shortest path using A*
    path = astar(graph, start, goal)

    if path:
        print("Shortest path found:", path)

        # Create a folium map
        map_osm = folium.Map(location=start, zoom_start=15)

        # Add lines to the map
        for line in lines:
            folium.PolyLine(line, color="red").add_to(map_osm)

        # Add the path to the map
        folium.PolyLine(path, color="green").add_to(map_osm)

        # Display the map
        map_osm.save('map.html')
    else:
        print("No path found")

if __name__ == "__main__":
    main()
