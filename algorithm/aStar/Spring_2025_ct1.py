# Test the A* implementation with a fixed example
import heapq

def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return path[::-1]

def a_star(n, obstacles, start, goal):
    obstacle_set = set(obstacles)
    if start in obstacle_set or goal in obstacle_set:
        return None

    directions = [(-1,0), (1,0), (0,-1), (0,1)]
    g_score = {start: 0}
    f_score = {start: manhattan(start, goal)}
    came_from = {}
    open_set = [(f_score[start], start)]
    visited = set()

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            return reconstruct_path(came_from, current)

        visited.add(current)

        for dr, dc in directions:
            neighbor = (current[0] + dr, current[1] + dc)
            if (0 <= neighbor[0] < n and 0 <= neighbor[1] < n
                and neighbor not in obstacle_set):
                tentative_g = g_score[current] + 1
                if tentative_g < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + manhattan(neighbor, goal)
                    if neighbor not in visited:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))
    return None

# ---- Static Test Case ----
n = 5
obstacles = [(1, 2), (2, 2), (3, 2)]
start = (0, 0)
goal = (4, 4)

path = a_star(n, obstacles, start, goal)
if path:
    print(" ".join(f"({r}, {c})" for r, c in path))
else:
    print("No path found")
