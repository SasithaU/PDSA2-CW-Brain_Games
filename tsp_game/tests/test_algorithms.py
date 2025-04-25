import pytest
from game.logic import brute_force_tsp, greedy_tsp, dp_tsp

# Sample distance matrix (50–100 km range)
matrix = {
    'A': {'A': 0, 'B': 80, 'C': 60, 'D': 70},
    'B': {'A': 80, 'B': 0, 'C': 90, 'D': 65},
    'C': {'A': 60, 'B': 90, 'C': 0, 'D': 75},
    'D': {'A': 70, 'B': 65, 'C': 75, 'D': 0},
}

home = 'A'
selected = ['B', 'C', 'D']


def test_brute_force():
    route, cost, time_ms = brute_force_tsp(matrix, home, selected)
    assert route[0] == home and route[-1] == home
    assert isinstance(cost, (int, float))
    print(f"\033[92m[PASS] Brute Force TSP: {route} | Cost: {cost} | Time: {time_ms} ms\033[0m")


def test_greedy():
    route, cost, time_ms = greedy_tsp(matrix, home, selected)
    assert route[0] == home and route[-1] == home
    assert isinstance(cost, (int, float))
    print(f"\033[92m[PASS] Greedy TSP: {route} | Cost: {cost} | Time: {time_ms} ms\033[0m")


def test_dynamic_programming():
    route, cost, time_ms = dp_tsp(matrix, home, selected)
    assert route[0] == home and route[-1] == home
    assert isinstance(cost, (int, float))
    print(f"\033[92m[PASS] Dynamic Programming TSP: {route} | Cost: {cost} | Time: {time_ms} ms\033[0m")
