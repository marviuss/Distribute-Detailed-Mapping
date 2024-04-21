import sys
import heapq
from math import radians, sin, cos, sqrt, atan2

class Graph:
    def __init__(self):
        # Dictionary to store vertices and their edges
        self.vertices = {}

    def add_vertex(self, name, edges):
        # Add a new vertex to the graph with its edges
        self.vertices[name] = edges

    def safest_path(self, start, finish, dangerous_junctions):
        # Dijkstra's algorithm for finding the safest path between two points
        distances = {}
        previous = {}
        nodes = []

        # Initialize distances to all vertices to infinity, except start vertex to 0
        for vertex in self.vertices:
            if vertex == start:
                distances[vertex] = 0
                heapq.heappush(nodes, [0, vertex])
            else:
                distances[vertex] = sys.maxsize
                heapq.heappush(nodes, [sys.maxsize, vertex])
            previous[vertex] = None

        # Iterate until all vertices are visited
        while nodes:
            smallest = heapq.heappop(nodes)[1]
            if smallest == finish:
                # Reconstruct the path from finish to start
                path = []
                total_dangerous_junctions = distances[smallest]
                while previous[smallest]:
                    path.append(smallest)
                    smallest = previous[smallest]
                path.append(start)
                path.reverse()  # Reverse the path to get the correct order
                return path, total_dangerous_junctions
            if distances[smallest] == sys.maxsize:
                break

            # Update distances to neighbors if a safer path is found
            for neighbor, weight, oneway in self.vertices[smallest]:
                alt = distances[smallest] + weight
                if neighbor in dangerous_junctions:
                    alt += 10  # Increase distance if the neighbor is a dangerous junction
                if oneway == "yes":
                    alt += 1  # Penalize one-way streets
                if alt < distances[neighbor]:
                    distances[neighbor] = alt
                    previous[neighbor] = smallest
                    heapq.heappush(nodes, [alt, neighbor])

        # If no path is found, return an empty path and distance 0
        return [], 0

    def add_line_string(self, line_string):
        # Add edges from a GeoJSON LineString feature
        coordinates = line_string["geometry"]["coordinates"]
        oneway = line_string["properties"].get("oneway", "no")
        for i in range(len(coordinates) - 1):
            start = tuple(coordinates[i])
            end = tuple(coordinates[i + 1])
            distance = self.calculate_distance(start, end)
            self.add_edge(start, end, distance, oneway)

    def add_edge(self, start, end, weight, oneway):
        # Add an edge between two vertices with the given weight
        if start not in self.vertices:
            self.add_vertex(start, [])
        if end not in self.vertices:
            self.add_vertex(end, [])
        self.vertices[start].append((end, weight, oneway))
        self.vertices[end].append((start, weight, oneway))

    @staticmethod
    def calculate_distance(coord1, coord2):
        # Calculate distance between two coordinates using Haversine formula
        lat1, lon1 = radians(coord1[1]), radians(coord1[0])
        lat2, lon2 = radians(coord2[1]), radians(coord2[0])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        radius = 6371.0  # Earth radius in kilometers
        distance = radius * c
        return distance

    def find_closest_point(self, point):
        # Find the closest vertex to a given point
        min_distance = sys.maxsize
        closest_point = None
        for vertex in self.vertices:
            distance = self.calculate_distance(point, vertex)
            if distance < min_distance:
                min_distance = distance
                closest_point = vertex
        return closest_point
