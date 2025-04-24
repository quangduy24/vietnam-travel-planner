import sys
from models.priority_queue import PriorityQueue

def dijkstra(graph, start_location, end_location=None):

    if start_location not in graph.vertices:
        raise ValueError(f"Start location {start_location} not in graph")
    if end_location and end_location not in graph.vertices:
        raise ValueError(f"End location {end_location} not in graph")
        
    # Initialize distances and parents
    distances = {vertex: float('infinity') for vertex in graph.vertices}
    distances[start_location] = 0
    parents = {vertex: None for vertex in graph.vertices}
    
    # Priority queue
    pq = PriorityQueue()
    pq.put(start_location, 0)
    
    while not pq.empty():
        current = pq.get()
        
        # If we've reached the destination, we can stop
        if current == end_location:
            break
            
        # Check all neighbors
        for neighbor, distance in graph.get_neighbors(current):
            # Calculate potential new distance
            new_distance = distances[current] + distance
            
            # If we found a better path, update it
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                parents[neighbor] = current
                pq.put(neighbor, new_distance)
    
    return distances, parents

def get_shortest_path(parents, start_location, end_location):
    """
    Get the shortest path from start to end using the parent dictionary
    
    Args:
        parents (dict): Dictionary of location to its parent in the shortest path
        start_location (str): Name of the starting location
        end_location (str): Name of the destination location
        
    Returns:
        list: List of locations in the shortest path from start to end
    """
    if parents[end_location] is None and start_location != end_location:
        return None
        
    path = []
    current = end_location
    
    while current != start_location:
        path.append(current)
        current = parents[current]
        
    path.append(start_location)
    path.reverse()
    
    return path
