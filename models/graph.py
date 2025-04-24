class Graph:

    def __init__(self):

        self.vertices = {}  # Dictionary of location name to Location object
        self.edges = {}     # Dictionary of location name to list of (neighbor, distance) tuples
        
    def add_vertex(self, location):

        if location.name not in self.vertices:
            self.vertices[location.name] = location
            self.edges[location.name] = []
            
    def add_edge(self, from_location, to_location, distance):

        if from_location not in self.edges:
            raise ValueError(f"Location {from_location} not in graph")
        if to_location not in self.vertices:
            raise ValueError(f"Location {to_location} not in graph")
            
        # Add the edge
        self.edges[from_location].append((to_location, distance))
        
    def get_neighbors(self, location_name):

        if location_name not in self.edges:
            return []
        return self.edges[location_name]
    
    def get_all_vertices(self):

        return list(self.vertices.keys())
