# import folium

# my_map = folium.Map(location=[28.6139, 77.2090], zoom_start=12)
# my_map.save("my_map.html")


import folium                    #map drawing tool
import pandas as pd              #data handling tool
import heapq                     #or dijikstra algorithm

my_map = folium.Map(location=[28.6139, 77.2090], zoom_start=12)

try:
    # Load POI data from the CSV file:
    poi_data = pd.read_csv("poi.csv")
    connections = pd.read_csv("connections.csv")  #connections between POIs
except FileNotFoundError:
    print("Error: poi.csv or connections.csv not found. Make sure they are in the same directory.")
    exit()  # Stop the script if the files are missing
    
# Add markers for each POI:
for index, row in poi_data.iterrows():
    folium.Marker([row['Latitude'], row['Longitude']], popup=row['Name']).add_to(my_map)
    
    graph = {}  # Start with an empty dictionary
for index, row in connections.iterrows():  # Go through each row in the connections DataFrame
    poi1 = row['POI1'].strip()  # Get the name of the first POI      
    poi2 = row['POI2'].strip()  # Get the name of the second POI
    distance = row['Distance']  # Get the distance between them

    if poi1 not in graph:
        graph[poi1] = {}  # If poi1 isn't in the graph yet, add it
    if poi2 not in graph:
        graph[poi2] = {}  # If poi2 isn't in the graph yet, add it
# if poi2 not in graph[poi1]:   #check if poi1-> poi2 connection exists
    graph[poi1][poi2] = distance  # Add the connection (poi1 to poi2) and its distance
#  if poi1 not in graph[poi2]:   #check if poi2-> poi1 connection exists
    graph[poi2][poi1] = distance  # Add the connection (poi2 to poi1) - assuming connections are two-way(bidirectional)
    
print(graph)

def dijikstra(graph,start_poi,end_poi):
    
    distances = {node: float('inf') for node in graph}  # Initialize distances to infinity
    distances[start_poi] = 0  # Distance from start_poi to itself is 0
    priority_queue = [(0, start_poi)]  # Priority queue to keep track of nodes to visit

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_distance > distances[current_node]:
            continue  # We've already found a shorter path to this node

        if current_node == end_poi:  # We've reached the end_poi node
            break

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight  # Calculate distance to neighbor

            if distance < distances[neighbor]:  # If we found a shorter path to neighbor
                distances[neighbor] = distance  # Update the distance
                heapq.heappush(priority_queue, (distance, neighbor))  # Add neighbor to queue

    # Reconstruct the shortest path
    path = []
    current = end_poi
    while current != start_poi:
        for neighbor, weight in graph[current].items():
            if distances[current] == distances[neighbor] + weight:
                path.insert(0, current)
                current = neighbor
                break
    path.insert(0, start_poi)  # Add the start_poi node to the beginning of the path
    return path, distances[end_poi]  # Return the path and the total distance
    
start_poi = "Restaurant A"  # Replace with your starting POI
end_poi = "Hospital C"  # Replace with your destination POI

shortest_path, shortest_distance = dijikstra(graph,start_poi,end_poi)

if shortest_path:
    points = []
    for poi_name in shortest_path:
        poi = poi_data[poi_data["Name"] == poi_name].iloc[0]
        points.append([poi["Latitude"], poi["Longitude"]])

    folium.PolyLine(points, color="red", weight=2.5, opacity=1).add_to(my_map)

    print(f"Shortest path: {shortest_path}")
    print(f"Shortest distance: {shortest_distance}")
else:
    print(f"No path found between {start_poi} and {end_poi}")
    
my_map.save("my_map.html")