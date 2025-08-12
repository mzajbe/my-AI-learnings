import heapq

def a_star(graph, start, goal, heuristic_function):
    # Priority queue stores (f_cost, node)
    pq = [(0, start)]
    g_costs = {node: float('inf') for node in graph}
    g_costs[start] = 0
    f_costs = {node: float('inf') for node in graph}
    f_costs[start] = heuristic_function(start, goal)
    came_from = {}

    while pq:
        _, current = heapq.heappop(pq)

        if current == goal:
            path = reconstruct_path_from_came_from(came_from, start, goal)
            return path, g_costs[goal]

        for neighbor, weight in graph[current].items():
            tentative_g = g_costs[current] + weight
            if tentative_g < g_costs[neighbor]:
                came_from[neighbor] = current
                g_costs[neighbor] = tentative_g
                f_costs[neighbor] = tentative_g + heuristic_function(neighbor, goal)
                heapq.heappush(pq, (f_costs[neighbor], neighbor))

    return None, float('inf')

def reconstruct_path_from_came_from(came_from, start, goal):
    path = [goal]
    current = goal
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    if path[0] != start:
        return None
    return path

def heuristic_function(node, goal):
    # Example heuristic (domain-specific). For this tiny graph it's arbitrary.
    heuristic_map = {
        'A': {'D': 7},
        'B': {'D': 6},
        'C': {'D': 2},
        'D': {'D': 0}
    }
    return heuristic_map.get(node, {}).get(goal, 0)

# Example usage
graph = {
    'A': {'B': 1, 'C': 4},
    'B': {'A': 1, 'C': 2, 'D': 6},
    'C': {'A': 4, 'B': 2, 'D': 3},
    'D': {'B': 6, 'C': 3}
}

start_node = 'A'
goal_node = 'D'
path, cost = a_star(graph, start_node, goal_node, heuristic_function)

print("A* path A -> D:", path)
print("A* path cost:", cost)