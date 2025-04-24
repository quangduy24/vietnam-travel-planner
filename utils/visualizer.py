import matplotlib.pyplot as plt
import networkx as nx

def visualize_graph(graph):

    G = nx.DiGraph()
    
    # Add nodes
    for location_name, location in graph.vertices.items():
        if location.coordinates:
            G.add_node(location_name, pos=location.coordinates)
        else:
            G.add_node(location_name)
    
    # Add edges
    for from_location, neighbors in graph.edges.items():
        for to_location, distance in neighbors:
            G.add_edge(from_location, to_location, weight=distance)
    
    # Draw the graph
    pos = nx.get_node_attributes(G, 'pos')
    plt.figure(figsize=(15, 10))
    nx.draw(G, pos, with_labels=True, node_size=500, node_color='skyblue', font_size=8)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title("Vietnam Travel Routes")
    plt.show()

def visualize_path(graph, path, title="Travel Path"):

    if not path:
        print("No path to visualize")
        return
        
    G = nx.DiGraph()
    
    # Add nodes
    for location_name, location in graph.vertices.items():
        if location.coordinates:
            G.add_node(location_name, pos=location.coordinates)
        else:
            G.add_node(location_name)
    
    # Add all edges
    for from_location, neighbors in graph.edges.items():
        for to_location, distance in neighbors:
            G.add_edge(from_location, to_location, weight=distance)
    
    # Create path edges
    path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
    
    # Draw the graph
    pos = nx.get_node_attributes(G, 'pos')
    plt.figure(figsize=(15, 10))
    
    # Draw all nodes
    nx.draw_networkx_nodes(G, pos, node_size=300, node_color='skyblue')
    
    # Draw path nodes with different color
    path_nodes = set(path)
    nx.draw_networkx_nodes(G, pos, nodelist=path_nodes, node_size=500, node_color='red')
    
    # Draw all edges
    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.3)
    
    # Draw path edges with different color and width
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, width=2.5, alpha=1.0, edge_color='red')
    
    # Draw labels
    nx.draw_networkx_labels(G, pos, font_size=8)
    
    plt.title(title)
    plt.axis('off')
    plt.show()
