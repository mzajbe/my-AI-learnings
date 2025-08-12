
import heapq

def dijkstra(graph,start):
    #priority queue:(distance,node)
    pq = [(0,start)]
    distances = {node:float('inf') for node in graph}
    distances[start] = 0
    predecessor = {start: None}
    visited = set()
    
    
    while pq:
        current_distance,current_node = heapq.heappop(pq)
        
        if current_node in visited:
            continue
        visited.add(current_node)
        
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor]=distance
                predecessor[neighbor]=current_node
                heapq.heappush(pq,(distance,neighbor))
    return distance,predecessor

def reconstruct_path(predecessor,start,goal):
    path=[]
    node=goal
    while node is not None:
        path.append(node)
        node = predecessor.get(node)
    path.reverse()
    if path[0] != start:
        #no path
        return None
    return path




# Example usage
graph = {
    'A': {'B': 1, 'C': 4},
    'B': {'A': 1, 'C': 2, 'D': 6},
    'C': {'A': 4, 'B': 2, 'D': 3},
    'D': {'B': 6, 'C': 3}
}

start_node = 'A'
distances,preds = dijkstra(graph,start_node)

goal = 'D'
path = reconstruct_path(preds,start_node,goal)

print("Distance:",distances)
print("path:",path)
