import sys
from algorithms.bfs import bfs, reconstruct_path
from algorithms.dfs import dfs
from algorithms.dijkstra import dijkstra, get_shortest_path
from algorithms.prim import prim
from utils.visualizer import visualize_graph, visualize_path

class CLI:

    def __init__(self, graph):

        self.graph = graph
        
    def run(self):
     
        print("=== Vietnam Travel Planner ===")
        
        while True:
            print("\nOptions:")
            print("1. Tìm đường đi ngắn nhất giữa 2 địa điểm")
            print("2. Tìm tất cả các vị trí có thể di chuyển từ điểm xuất phát")
            print("3. Tìm cây khung tối thiểu từ một vị trí")
            print("4. Hiển thị toàn bộ đồ thị")
            print("5. Exit")
            
            choice = input("\nEnter your choice (1-5): ")
            
            if choice == '1':
                self.find_shortest_path()
            elif choice == '2':
                self.find_reachable_locations()
            elif choice == '3':
                self.find_minimum_spanning_tree()
            elif choice == '4':
                self.visualize_graph()
            elif choice == '5':
                print("Exiting...")
                sys.exit(0)
            else:
                print("Invalid choice. Please try again.")
    
    def find_shortest_path(self):
        
        print("\n=== Find Shortest Path ===")
        
        # Get all locations
        locations = sorted(self.graph.get_all_vertices())
        
        # Print all locations
        print("\nAvailable locations:")
        for i, location in enumerate(locations):
            print(f"{i+1}. {location}")
        
        # Get start and end locations
        try:
            start_idx = int(input("\nEnter the number of the starting location: ")) - 1
            end_idx = int(input("Enter the number of the destination location: ")) - 1
            
            if start_idx < 0 or start_idx >= len(locations) or end_idx < 0 or end_idx >= len(locations):
                print("Invalid location number.")
                return
                
            start_location = locations[start_idx]
            end_location = locations[end_idx]
            
            # Find shortest path using Dijkstra's algorithm
            distances, parents = dijkstra(self.graph, start_location, end_location)
            path = get_shortest_path(parents, start_location, end_location)
            
            if path:
                print(f"\nShortest path from {start_location} to {end_location}:")
                
                # Calculate total distance
                total_distance = 0
                for i in range(len(path) - 1):
                    for neighbor, distance in self.graph.get_neighbors(path[i]):
                        if neighbor == path[i + 1]:
                            total_distance += distance
                            break
                
                # Print path
                print(" -> ".join(path))
                print(f"Total distance: {total_distance} km")
                
                # Visualize path
                visualize_path(self.graph, path, f"Shortest Path: {start_location} to {end_location}")
            else:
                print(f"No path found from {start_location} to {end_location}")
                
        except ValueError:
            print("Please enter valid numbers.")
            
    def find_reachable_locations(self):
      
        print("\n=== Find Reachable Locations ===")
        
        # Get all locations
        locations = sorted(self.graph.get_all_vertices())
        
        # Print all locations
        print("\nAvailable locations:")
        for i, location in enumerate(locations):
            print(f"{i+1}. {location}")
        
        # Get start location
        try:
            start_idx = int(input("\nEnter the number of the starting location: ")) - 1
            
            if start_idx < 0 or start_idx >= len(locations):
                print("Invalid location number.")
                return
                
            start_location = locations[start_idx]
            
            # Find all reachable locations using BFS
            parents = bfs(self.graph, start_location)
            
            # Get all reachable locations
            reachable = [loc for loc in parents.keys() if loc != start_location]
            
            if reachable:
                print(f"\nReachable locations from {start_location}:")
                for i, location in enumerate(sorted(reachable)):
                    path = reconstruct_path(parents, start_location, location)
                    print(f"{i+1}. {location} via: {' -> '.join(path)}")
            else:
                print(f"No locations are reachable from {start_location}")
                
        except ValueError:
            print("Please enter a valid number.")
            
    def find_minimum_spanning_tree(self):
       
        print("\n=== Find Minimum Spanning Tree ===")
        
        # Get all locations
        locations = sorted(self.graph.get_all_vertices())
        
        # Print all locations
        print("\nAvailable locations:")
        for i, location in enumerate(locations):
            print(f"{i+1}. {location}")
        
        # Get start location
        try:
            start_idx = int(input("\nEnter the number of the starting location: ")) - 1
            
            if start_idx < 0 or start_idx >= len(locations):
                print("Invalid location number.")
                return
                
            start_location = locations[start_idx]
            
            # Find minimum spanning tree using Prim's algorithm
            mst = prim(self.graph, start_location)
            
            if mst:
                print(f"\nMinimum Spanning Tree from {start_location}:")
                
                # Calculate total distance
                total_distance = 0
                for to_loc, from_loc in mst.items():
                    for neighbor, distance in self.graph.get_neighbors(from_loc):
                        if neighbor == to_loc:
                            total_distance += distance
                            print(f"{from_loc} -> {to_loc} ({distance} km)")
                            break
                
                print(f"Total distance: {total_distance} km")
            else:
                print(f"No minimum spanning tree found from {start_location}")
                
        except ValueError:
            print("Please enter a valid number.")
            
    def visualize_graph(self):
      
        print("\nVisualizing the entire graph...")
        visualize_graph(self.graph)
