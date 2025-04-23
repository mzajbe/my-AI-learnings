import sys
import math
import random

def parse_input():
    """Parse the input file to get the locations."""
    try:
        n = int(input())
        locations = []
        for _ in range(n):
            x, y = map(float, input().split())
            locations.append((x, y))
        return locations
    except Exception as e:
        print(f"Error parsing input: {e}")
        sys.exit(1)

def calculate_distance(point1, point2):
    """Calculate Euclidean distance between two points."""
    return math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)

def calculate_total_distance(route, locations):
    """Calculate the total distance of a route."""
    total_dist = 0
    for i in range(len(route) - 1):
        total_dist += calculate_distance(locations[route[i]], locations[route[i+1]])
    return total_dist

def generate_initial_route(n):
    """Generate a random initial route, ensuring warehouse is first and last."""
    route = [0]  # Start with warehouse (index 0)
    route.extend(random.sample(range(1, n), n-1))  # Add all other locations in random order
    route.append(0)  # End with warehouse
    return route

def get_neighbors(route):
    """Generate neighbors by swapping two non-warehouse locations."""
    neighbors = []
    # We exclude first and last elements (warehouse) from swapping
    for i in range(1, len(route) - 2):
        for j in range(i + 1, len(route) - 1):
            neighbor = route.copy()
            neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
            neighbors.append(neighbor)
    return neighbors

def hill_climbing(locations):
    """Implement hill climbing algorithm for TSP."""
    n = len(locations)
    current_route = generate_initial_route(n)
    current_distance = calculate_total_distance(current_route, locations)
    
    improvement = True
    while improvement:
        improvement = False
        neighbors = get_neighbors(current_route)
        
        for neighbor in neighbors:
            neighbor_distance = calculate_total_distance(neighbor, locations)
            if neighbor_distance < current_distance:
                current_route = neighbor
                current_distance = neighbor_distance
                improvement = True
                break  # Move to the first better neighbor found
    
    return current_route, current_distance

def main():
    locations = parse_input()
    best_route, best_distance = hill_climbing(locations)
    
    # Convert to 1-indexed for output as specified
    route_str = " -> ".join(str(i + 1) for i in best_route)
    
    print("=== Hill Climbing Result ===")
    print(f"Route: {route_str}")
    print(f"Total Distance: {best_distance:.2f}")

if __name__ == "__main__":
    main()