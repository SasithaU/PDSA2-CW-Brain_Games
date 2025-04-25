import time
import itertools
import functools
import sys

def brute_force_tsp(matrix, home, selected):
    if not matrix or not selected:
        raise ValueError("Matrix and selected cities cannot be empty.")

    start = time.time()
    cities = selected.copy()
    shortest_distance = float('inf')
    best_route = []

    for perm in itertools.permutations(cities):
        route = [home] + list(perm) + [home]
        try:
            distance = sum(matrix[route[i]][route[i+1]] for i in range(len(route)-1))
        except KeyError:
            raise ValueError("Invalid city name in route.")
        if distance < shortest_distance:
            shortest_distance = distance
            best_route = route

    end = time.time()
    return best_route, shortest_distance, round((end - start) * 1000, 2) 

def greedy_tsp(matrix, home, selected):
    if not matrix or not selected:
        raise ValueError("Matrix and selected cities cannot be empty.")

    start = time.time()
    unvisited = set(selected)
    route = [home]
    current = home
    total_distance = 0

    while unvisited:
        try:
            next_city = min(unvisited, key=lambda city: matrix[current][city])
        except KeyError:
            raise ValueError("Invalid city in matrix.")
        total_distance += matrix[current][next_city]
        route.append(next_city)
        current = next_city
        unvisited.remove(next_city)

    total_distance += matrix[current][home]
    route.append(home)
    end = time.time()
    return route, total_distance, round((end - start) * 1000, 2) 


def dp_tsp(matrix, home, selected):
    if not matrix or not selected:
        raise ValueError("Matrix and selected cities cannot be empty.")

    start = time.time()
    all_cities = [home] + selected
    city_index = {city: i for i, city in enumerate(all_cities)}
    n = len(all_cities)

    # Memoization for cost and path
    @functools.lru_cache(None)
    def visit(city, visited):
        if visited == (1 << n) - 1:
            return matrix[all_cities[city]][home], [home]  # Return cost and path back to home
        
        min_cost = sys.maxsize
        best_path = []
        for next_city in range(n):
            if not visited & (1 << next_city):
                cost_to_next = matrix[all_cities[city]][all_cities[next_city]]
                temp_cost, temp_path = visit(next_city, visited | (1 << next_city))
                total_cost = cost_to_next + temp_cost
                if total_cost < min_cost:
                    min_cost = total_cost
                    best_path = [all_cities[next_city]] + temp_path
        return min_cost, best_path

    total_cost, path = visit(0, 1)
    path = [home] + path  # Add home at the beginning
    end = time.time()

    return path, total_cost, round((end - start) * 1000, 2)