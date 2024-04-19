import heapq
import sys
import json
import geojson
from math import radians, sin, cos, sqrt, atan2


class Graph:
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, name, edges):
        self.vertices[name] = edges
    

    def safest_path(self, start, finish, dangerous_junctions):
        distances = {}
        previous = {}
        nodes = []

        for vertex in self.vertices:
            if vertex == start:
                distances[vertex] = 0
                heapq.heappush(nodes, [0, vertex])
            else:
                distances[vertex] = sys.maxsize
                heapq.heappush(nodes, [sys.maxsize, vertex])
            previous[vertex] = None

        while nodes:
            smallest = heapq.heappop(nodes)[1]
            if smallest == finish:
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

            for neighbor, weight, oneway in self.vertices[smallest]:
                alt = distances[smallest] + weight
                if neighbor in dangerous_junctions:
                    alt += 10
                if oneway == "yes":
                    alt += 1  
                if alt < distances[neighbor]:
                    distances[neighbor] = alt
                    previous[neighbor] = smallest
                    heapq.heappush(nodes, [alt, neighbor])

        return [], 0
    

    # def safest_path(self, start, finish, dangerous_junctions):
    #     distances = {}
    #     previous = {}
    #     nodes = []

    #     for vertex in self.vertices:
    #         if vertex == start:
    #             distances[vertex] = 0
    #             heapq.heappush(nodes, [0, vertex])
    #         else:
    #             distances[vertex] = sys.maxsize
    #             heapq.heappush(nodes, [sys.maxsize, vertex])
    #         previous[vertex] = None

    #     while nodes:
    #         smallest = heapq.heappop(nodes)[1]
    #         if smallest == finish:
    #             path = []
    #             total_dangerous_junctions = distances[smallest]
    #             while previous[smallest]:
    #                 path.append(smallest)
    #                 smallest = previous[smallest]
    #             path.append(start)
    #             path.reverse()  # Reverse the path to get the correct order
    #             return path, total_dangerous_junctions
    #         if distances[smallest] == sys.maxsize:
    #             break

    #         for neighbor, weight, oneway in self.vertices[smallest]:
    #             alt = distances[smallest] + weight
    #             if neighbor in dangerous_junctions:
    #                 alt += 1  # Increase weight if neighbor is a dangerous junction
    #             if oneway == "yes":
    #                 # If the road is one-way, ensure the direction of traversal matches the one-way direction
    #                 alt += 1  # Increase weight to discourage going against one-way direction
    #             if alt < distances[neighbor]:
    #                 distances[neighbor] = alt
    #                 previous[neighbor] = smallest
    #                 heapq.heappush(nodes, [alt, neighbor])

    #     return [], 0

    def add_line_string(self, line_string):
        coordinates = line_string["geometry"]["coordinates"]
        oneway = line_string["properties"].get("oneway", "no")  
        for i in range(len(coordinates) - 1):
            start = tuple(coordinates[i])
            end = tuple(coordinates[i + 1])
            distance = self.calculate_distance(start, end)
            self.add_edge(start, end, distance, oneway)

    def add_edge(self, start, end, weight, oneway):
        if start not in self.vertices:
            self.add_vertex(start, [])
        if end not in self.vertices:
            self.add_vertex(end, [])
        self.vertices[start].append((end, weight, oneway))
        self.vertices[end].append((start, weight, oneway))

    @staticmethod
    def calculate_distance(coord1, coord2):
        lat1, lon1 = radians(coord1[1]), radians(coord1[0])
        lat2, lon2 = radians(coord2[1]), radians(coord2[0])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        radius = 6371.0
        distance = radius * c
        return distance

    def find_closest_point(self, point):
        min_distance = sys.maxsize
        closest_point = None
        for vertex in self.vertices:
            distance = self.calculate_distance(point, vertex)
            if distance < min_distance:
                min_distance = distance
                closest_point = vertex
        return closest_point