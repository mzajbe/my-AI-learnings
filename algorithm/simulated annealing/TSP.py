import sys
import math
import random

def parse_input():
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
    return math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)

def calculate_total_distance(route, locations):
    total_dist = 0
    for i in range(len(route) - 1):
        total_dist += calculate_distance(locations[route[i]], locations[route[i+1]])
    return total_dist

def generate_initial_route(n):
    
    route = [0] 
    route.extend(random.sample(range(1, n), n-1))  
    route.append(0)  
    return route

def get_random_neighbor(route):
    
    
    i, j = random.sample(range(1, len(route) - 1), 2)
    neighbor = route.copy()
    neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
    return neighbor

def simulated_annealing(locations, initial_temp=1000, cooling_rate=0.995, min_temp=0.01, max_iterations=10000):
    
    n = len(locations)
    current_route = generate_initial_route(n)
    current_distance = calculate_total_distance(current_route, locations)
    
    best_route = current_route.copy()
    best_distance = current_distance
    
    temp = initial_temp
    iteration = 0
    
    while temp > min_temp and iteration < max_iterations:
        neighbor_route = get_random_neighbor(current_route)
        neighbor_distance = calculate_total_distance(neighbor_route, locations)
        
        
        delta = neighbor_distance - current_distance
        acceptance_probability = math.exp(-delta / temp) if delta > 0 else 1.0
        
        
        if random.random() < acceptance_probability:
            current_route = neighbor_route
            current_distance = neighbor_distance
            
            
            if current_distance < best_distance:
                best_route = current_route.copy()
                best_distance = current_distance
        
        
        temp *= cooling_rate
        iteration += 1
    
    return best_route, best_distance

def main():
    locations = parse_input()
    best_route, best_distance = simulated_annealing(locations)
    
    
    route_str = " -> ".join(str(i + 1) for i in best_route)
    
    
    print(f"Route: {route_str}")
    print(f"Total Distance: {best_distance:.2f}")

if __name__ == "__main__":
    main()