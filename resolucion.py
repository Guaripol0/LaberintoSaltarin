from queue import PriorityQueue
import numpy as np


def busqueda_dfs(matrix, current_point, ending_point, visited_nodes=None, path=None):
    if visited_nodes is None:
        visited_nodes = set()
    if path is None:
        path = []

    path.append(current_point)
    visited_nodes.add(current_point)

    if current_point == ending_point:
        return path 

    for neighbor in vecinos(matrix, current_point):
        if neighbor not in visited_nodes:
            result = busqueda_dfs(matrix, neighbor, ending_point, visited_nodes, path)
            if result:
                return result
    path.pop()
    return None

def vecinos(matrix, point):
    x, y = point
    jumps = matrix[x][y]
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    neighbors = [(x + jumps * dx, y + jumps * dy) for dx, dy in directions 
                 if 0 <= x + jumps * dx < len(matrix) and 0 <= y + jumps * dy < len(matrix[0])]
    return neighbors

def busqueda_ucs(matrix, start, goal):
    frontier = PriorityQueue()
    frontier.put((0, start, [start]))
    visited = set()

    while not frontier.empty():
        current_cost, current_point, path = frontier.get()

        if current_point == goal:
            return path

        if current_point not in visited:
            visited.add(current_point)

            for neighbor in vecinos(matrix, current_point):
                if neighbor not in visited:
                    jump_cost = matrix[current_point[0]][current_point[1]]
                    new_cost = current_cost + jump_cost
                    frontier.put((new_cost, neighbor, path + [neighbor]))

    return None

def resolver_juego_completo(mazes, starts, goals):
    solutions = []
    for i in range(len(mazes)):
        solution = resolver_juego(mazes[i], starts[i], goals[i])
        solutions.append(solution)
    return solutions

def resolver_juego(matrix, start, goal):
    path = busqueda_dfs(matrix, start, goal)
    if path is not None:
        path = busqueda_ucs(matrix, start, goal)
        jumps = len(path) - 1
        return {'path': path, 'jumps': jumps}
    return None

def resolver_juego_dfs(matrix, start, goal):
    path = busqueda_dfs(matrix, start, goal)
    if path is not None:
        jumps = len(path) - 1
        return {'path': path, 'jumps': jumps}
    return None

def resolver_juego_ucs(matrix, start, goal):
    path = busqueda_ucs(matrix, start, goal)
    if path is not None:
        jumps = len(path) - 1
        return {'path': path, 'jumps': jumps}
    return None

def verificar_matriz(m, n):
    while True:
        # Generate random matrix directly in the loop
        matrix = np.random.randint(1, 11, size=(m, n)).tolist()
        start_point = (0, 0)
        ending_point = (len(matrix) - 1, len(matrix[0]) - 1)
        visited_nodes = set()
        path = []
        if busqueda_dfs(matrix, start_point, ending_point, visited_nodes, path):
            for row in matrix:
                print(row)
            return matrix