def dfs(graph, start_location, end_location=None):

    if start_location not in graph.vertices:
        raise ValueError(f"Start location {start_location} not in graph")
    if end_location and end_location not in graph.vertices:
        raise ValueError(f"End location {end_location} not in graph")
        
    visited = set()
    parent = {start_location: None}
    
    def dfs_recursive(current):
        if current == end_location:
            return True
            
        visited.add(current)
        
        for neighbor, _ in graph.get_neighbors(current):
            if neighbor not in visited:
                parent[neighbor] = current
                if dfs_recursive(neighbor):
                    return True
                    
        return False
    
    dfs_recursive(start_location)
    return parent
