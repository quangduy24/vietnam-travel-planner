from collections import deque

def bfs(graph, start_location, end_location=None):

    if start_location not in graph.vertices:
        raise ValueError(f"Start location {start_location} not in graph")
    if end_location and end_location not in graph.vertices:
        raise ValueError(f"End location {end_location} not in graph")
        
    visited = set()
    queue = deque([start_location])
    parent = {start_location: None}
    
    while queue:
        current = queue.popleft()
        
        if current == end_location:
            break
            
        if current in visited:
            continue
            
        visited.add(current)
        
        for neighbor, _ in graph.get_neighbors(current):
            if neighbor not in visited:
                queue.append(neighbor)
                if neighbor not in parent:
                    parent[neighbor] = current
    
    return parent

def reconstruct_path(parent, start_location, end_location):

    if end_location not in parent:
        return None
        
    path = []
    current = end_location
    
    while current != start_location:
        path.append(current)
        current = parent[current]
        
    path.append(start_location)
    path.reverse()
    
    return path
