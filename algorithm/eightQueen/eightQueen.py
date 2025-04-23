import random
import math

# Calculate the number of attacking pairs of queens
def calculate_conflicts(state):
    conflicts = 0
    n = len(state)
    for i in range(n):
        for j in range(i + 1, n):
            # Check if two queens are on the same diagonal or in the same row
            if state[i] == state[j] or abs(state[i] - state[j]) == j - i:
                conflicts += 1
    return conflicts

# Hill Climbing Algorithm with multiple restarts
def hill_climbing(n, restarts=10):
    best_state = None
    best_conflicts = float('inf')
    
    for _ in range(restarts):
        current_state = random.sample(range(n), n)  # Random initial configuration of queens
        current_conflicts = calculate_conflicts(current_state)

        while True:
            neighbors = generate_neighbors(current_state)
            best_neighbor = min(neighbors, key=calculate_conflicts)
            best_conflict_neighbor = calculate_conflicts(best_neighbor)

            if best_conflict_neighbor < current_conflicts:
                current_state = best_neighbor
                current_conflicts = best_conflict_neighbor
            else:
                break

        if current_conflicts < best_conflicts:
            best_state = current_state
            best_conflicts = current_conflicts

    return best_state, best_conflicts

# Simulated Annealing Algorithm with multiple restarts
def simulated_annealing(n, temperature=1000, cooling_rate=0.98, restarts=10):
    best_state = None
    best_conflicts = float('inf')
    
    for _ in range(restarts):
        current_state = random.sample(range(n), n)  # Initial random configuration of queens
        current_conflicts = calculate_conflicts(current_state)

        best_state_local = current_state
        best_conflicts_local = current_conflicts
        
        while temperature > 1:
            new_state = generate_new_solution(current_state)
            new_conflicts = calculate_conflicts(new_state)

            if new_conflicts < current_conflicts or random.random() < acceptance_probability(current_conflicts, new_conflicts, temperature):
                current_state = new_state
                current_conflicts = new_conflicts

            if current_conflicts < best_conflicts_local:
                best_state_local = current_state
                best_conflicts_local = current_conflicts

            temperature *= cooling_rate
        
        if best_conflicts_local < best_conflicts:
            best_state = best_state_local
            best_conflicts = best_conflicts_local
    
    return best_state, best_conflicts

# Generate neighboring solutions by moving a queen to a different row in its column
def generate_neighbors(state):
    neighbors = []
    n = len(state)
    for i in range(n):
        for j in range(n):
            if j != state[i]:  # Avoid moving the queen to its current position
                new_state = state[:]
                new_state[i] = j  # Move the queen in column i to row j
                neighbors.append(new_state)
    return neighbors

# Acceptance probability function for Simulated Annealing
def acceptance_probability(old_conflicts, new_conflicts, temperature):
    if new_conflicts < old_conflicts:
        return 1.0
    return math.exp((old_conflicts - new_conflicts) / temperature)

# Generate a new solution by moving a queen to a random row
def generate_new_solution(state):
    new_state = state[:]
    i = random.randint(0, len(state) - 1)  # Pick a random queen
    j = random.randint(0, len(state) - 1)  # Pick a new row for the queen
    new_state[i] = j  # Move the queen in column i to row j
    return new_state

# Input data: Number of queens (n=8)
n = 8

# Hill Climbing result with multiple restarts
hill_state, hill_conflicts = hill_climbing(n)
print("=== Hill Climbing Result ===")
print(f"State: {hill_state}")
print(f"Conflicts: {hill_conflicts}")

# Simulated Annealing result with multiple restarts
sa_state, sa_conflicts = simulated_annealing(n)
print("=== Simulated Annealing Result ===")
print(f"State: {sa_state}")
print(f"Conflicts: {sa_conflicts}")
