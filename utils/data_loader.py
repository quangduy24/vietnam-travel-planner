from models.graph import Graph
from models.location import Location

def load_graph_data(graph_data, coordinates_data):
 
    graph = Graph()
    
    # First, add all locations
    for location_name, coords in coordinates_data.items():
        location = Location(location_name, coords)
        graph.add_vertex(location)
    
    # Then, add all edges
    for from_location, neighbors in graph_data.items():
        for neighbor_data in neighbors:
            to_location, distance = neighbor_data
            graph.add_edge(from_location, to_location, distance)
    
    return graph
