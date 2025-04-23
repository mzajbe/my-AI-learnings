import random
import math

# Calculate the number of attacking pairs of queens
def calculate_conflicts(state):
    conflicts = 0
    n = len(state)
    for i in range(n):
        for j in range(i + 1, n):
            # Check if two queens are on the same diagonal or in the same row
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                conflicts += 1
    return conflicts

# Hill Climbing Algorithm with multiple restarts
def steepest_ascent_hill_climbing(queen_loc, chess_board):
    n = len(chess_board)
    current_conflicts = calculate_conflicts(queen_loc)
    col = -1
    while current_conflicts > 0:
        best_loc = queen_loc
        best_conflicts = current_conflicts
        for col in range(n):
            new_loc = get_neighbor(queen_loc, chess_board, col)
            new_conflicts = calculate_conflicts(new_loc)
            if new_conflicts < best_conflicts:
                best_conflicts = new_conflicts
                best_loc = new_loc
        if best_conflicts >= current_conflicts:
            break
        queen_loc = best_loc
        current_conflicts = best_conflicts
    return queen_loc

# Simulated Annealing Algorithm with multiple restarts
def simulated_annealing(queen_loc, chess_board, initial_temp, cooling_rate):
    temp = initial_temp
    current_loc = list(queen_loc)
    current_cost = calculate_conflicts(current_loc)

    while temp > 0.1:
        col = random.randint(0, len(chess_board) - 1)
        neighbor_loc = get_neighbor(current_loc, chess_board, col)
        neighbor_cost = calculate_conflicts(neighbor_loc)

        if neighbor_cost < current_cost or random.uniform(0, 1) < math.exp((current_cost - neighbor_cost) / temp):
            current_loc = neighbor_loc
            current_cost = neighbor_cost

        temp *= cooling_rate

    return current_loc

# Get the neighbor state by moving a queen to a new row
def get_neighbor(queen_loc, chess_board, col):
    n = len(chess_board)
    best_cost = float('inf')
    best_loc = list(queen_loc)
    for new_row in range(n):
        if new_row != queen_loc[col]:
            new_loc = list(queen_loc)
            new_loc[col] = new_row
            cost = calculate_conflicts(new_loc)
            if cost < best_cost:
                best_cost = cost
                best_loc = new_loc
    return best_loc

# Function to print the board in a readable format
def print_board(queen_loc, n):
    board = [['.' for _ in range(n)] for _ in range(n)]
    for col, row in enumerate(queen_loc):
        board[row][col] = 'Q'
    
    for row in board:
        print(' '.join(row))

# Input data: Number of queens (n=8)
n = 8
initial_queen_loc = [0, 3, 0, 2, 7, 5, 4, 6]  # You can start with a random configuration

# Create a chessboard of size 8x8 for Hill Climbing
chess_board = [[0] * n for _ in range(n)]

# Run Hill Climbing
final_queen_loc = steepest_ascent_hill_climbing(initial_queen_loc, chess_board)
print("=== Hill Climbing Result ===")
print_board(final_queen_loc, n)

# Run Simulated Annealing
final_queen_loc_sa = simulated_annealing(initial_queen_loc, chess_board, initial_temp=30, cooling_rate=0.95)
print("=== Simulated Annealing Result ===")
print_board(final_queen_loc_sa, n)
