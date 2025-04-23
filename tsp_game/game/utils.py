import random

def generate_distance_matrix(cities):
    if not cities:
        raise ValueError("Cities list cannot be empty.")
    matrix = {}
    for i in cities:
        matrix[i] = {}
        for j in cities:
            matrix[i][j] = 0 if i == j else random.randint(50, 100)
    return matrix


def format_route(route):
    return " -> ".join(route)
