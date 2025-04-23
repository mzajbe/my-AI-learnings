import random
import math

# Calculate the Euclidean distance between two points
def euclidean_distance(p1, p2):
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

# Calculate total distance for a given route
def calculate_total_distance(route):
    distance = 0
    for i in range(len(route) - 1):
        distance += euclidean_distance(route[i], route[i + 1])
    distance += euclidean_distance(route[-1], route[0])  # Return to the start (warehouse)
    return distance

# Format the route to match the required output (1-based index)
def format_route(route):
    route_indices = [locations.index(loc) + 1 for loc in route]  # Convert coordinates to indices
    return " -> ".join(map(str, route_indices))

# Hill Climbing Algorithm with multiple restarts
def hill_climbing(locations, restarts=10):
    best_route = None
    best_distance = float('inf')
    
    for _ in range(restarts):
        current_route = random.sample(locations[1:], len(locations) - 1)  # Random initial route excluding warehouse
        current_route = [locations[0]] + current_route + [locations[0]]  # Add warehouse at start and end
        current_distance = calculate_total_distance(current_route)

        while True:
            neighbors = generate_neighbors(current_route)
            best_neighbor = min(neighbors, key=lambda route: calculate_total_distance(route))
            best_distance_neighbor = calculate_total_distance(best_neighbor)

            if best_distance_neighbor < current_distance:
                current_route = best_neighbor
                current_distance = best_distance_neighbor
            else:
                break
        
        # Keep track of the best found route
        if current_distance < best_distance:
            best_route = current_route
            best_distance = current_distance
    
    formatted_route = format_route(best_route)
    return formatted_route, best_distance

# Simulated Annealing Algorithm with multiple restarts
def simulated_annealing(locations, temperature=1000, cooling_rate=0.98, restarts=10):
    best_route = None
    best_distance = float('inf')
    
    for _ in range(restarts):
        current_route = random.sample(locations[1:], len(locations) - 1)  # Initial random route excluding warehouse
        current_route = [locations[0]] + current_route + [locations[0]]  # Add warehouse at start and end
        current_distance = calculate_total_distance(current_route)

        best_route_local = current_route
        best_distance_local = current_distance
        
        while temperature > 1:
            new_route = generate_new_solution(current_route)
            new_distance = calculate_total_distance(new_route)
            
            # Accept new route based on the acceptance probability
            if new_distance < current_distance or random.random() < acceptance_probability(current_distance, new_distance, temperature):
                current_route = new_route
                current_distance = new_distance
            
            # Update the best local route if needed
            if current_distance < best_distance_local:
                best_route_local = current_route
                best_distance_local = current_distance

            temperature *= cooling_rate
        
        # Track best solution found across all restarts
        if best_distance_local < best_distance:
            best_route = best_route_local
            best_distance = best_distance_local
    
    formatted_route = format_route(best_route)
    return formatted_route, best_distance

# Generate neighboring solutions by swapping two locations
def generate_neighbors(route):
    neighbors = []
    for i in range(1, len(route) - 2):  # Exclude warehouse (start and end points)
        for j in range(i + 1, len(route) - 1):
            new_route = route[:]
            new_route[i], new_route[j] = new_route[j], new_route[i]  # Swap two locations
            neighbors.append(new_route)
    return neighbors

# Acceptance probability function for Simulated Annealing
def acceptance_probability(old_cost, new_cost, temperature):
    if new_cost < old_cost:
        return 1.0
    return math.exp((old_cost - new_cost) / temperature)

# Generate a new solution by swapping two random locations
def generate_new_solution(route):
    new_route = route[:]
    i = random.randint(1, len(route) - 2)  # Exclude warehouse
    j = random.randint(1, len(route) - 2)  # Exclude warehouse
    new_route[i], new_route[j] = new_route[j], new_route[i]  # Swap two locations
    return new_route

# Input data: Locations with warehouse at index 0
locations = [(0.0, 0.0), (2.0, 3.0), (4.0, 0.0), (4.0, 3.0), (6.0, 1.0)]

# Hill Climbing result with multiple restarts
hill_route, hill_distance = hill_climbing(locations)
print("=== Hill Climbing Result ===")
print(f"Route: {hill_route}")
print(f"Total Distance: {hill_distance:.2f}")

# Simulated Annealing result with multiple restarts
sa_route, sa_distance = simulated_annealing(locations)
print("=== Simulated Annealing Result ===")
print(f"Route: {sa_route}")
print(f"Total Distance: {sa_distance:.2f}")
