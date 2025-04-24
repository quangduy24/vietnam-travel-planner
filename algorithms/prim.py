from models.priority_queue import PriorityQueue

def prim(graph, start_location):

    if start_location not in graph.vertices:
        raise ValueError(f"Start location {start_location} not in graph")
        
    # Initialize
    mst = {}  # Minimum spanning tree
    visited = set([start_location])
    edges = []
    
    # Add all edges from start location
    for neighbor, distance in graph.get_neighbors(start_location):
        edges.append((start_location, neighbor, distance))
    
    # Sort edges by distance
    edges.sort(key=lambda x: x[2])
    
    # While we haven't visited all vertices
    while len(visited) < len(graph.vertices) and edges:
        # Get the edge with the smallest distance
        from_loc, to_loc, distance = edges.pop(0)
        
        # If we've already visited the destination, skip
        if to_loc in visited:
            continue
            
        # Add to MST and mark as visited
        mst[to_loc] = from_loc
        visited.add(to_loc)
        
        # Add all edges from the new vertex
        for neighbor, dist in graph.get_neighbors(to_loc):
            if neighbor not in visited:
                edges.append((to_loc, neighbor, dist))
                
        # Re-sort edges
        edges.sort(key=lambda x: x[2])
    
    return mst
