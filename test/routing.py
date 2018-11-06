#!/usr/bin/env python3

import googlemaps
import pprint
import ortools

from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2


addresses = [
    "vasagatan 13, gothenburg",
    "kungsportsavenyen 10, gothenburg",
    "haga nygata 16, gothenburg",
    "majorsgatan 1, gothenburg",
    "viktoriagatan 19, gothenburg",
    "terrassgatan 3, gothenburg",
    "fredsgatan 14, gothenburg",
    "kyrkogatan 13, gothenburg",
    "herkulesgatan 13, gothenburg",
    "västra keillersgatan 9, gothenburg",
]

api_key = 'AIzaSyCUbOT9j-li5pxGSJYIFnjC_lnjxQdjxCI'

gm = googlemaps.Client(key=api_key)

distance_matrix = gm.distance_matrix(origins=addresses, destinations=addresses)

optimise = 'distance'
matrix = []

for element_obj in distance_matrix['rows']:
    row = []
    elements = element_obj['elements']
    for item in elements:
        row.append(item[optimise]['value'])
    matrix.append(row)

tsp_size = len(addresses)
num_routes = 1
# start and end address index
depot = 0


def create_distance_callback(dist_matrix):
    # Create a callback to calculate distances between cities.
    def distance_callback(from_node, to_node):
        return int(dist_matrix[from_node][to_node])
    return distance_callback


if tsp_size > 1:
    route = pywrapcp.RoutingModel(tsp_size, num_routes, depot)
    search_parameters = pywrapcp.RoutingModel.DefaultSearchParameters()
    dist_callback = create_distance_callback(matrix)
    route.SetArcCostEvaluatorOfAllVehicles(dist_callback)

    assignment = route.SolveWithParameters(search_parameters)

    if assignment:
        print('Total distance: ' + str(assignment.ObjectiveValue()))
        route_number = 0
        index = route.Start(route_number)
        path = ''
        while not route.IsEnd(index):
            path += str(addresses[route.IndexToNode(index)]) + ' -> '
            index = assignment.Value(route.NextVar(index))
        path += str(addresses[route.IndexToNode(index)])
        print(path)
