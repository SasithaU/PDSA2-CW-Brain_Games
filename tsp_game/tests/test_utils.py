
import pytest


from game.utils import generate_distance_matrix, format_route

def test_generate_distance_matrix_valid():
    cities = ["A", "B", "C"]
    matrix = generate_distance_matrix(cities)
    assert isinstance(matrix, dict)
    assert all(city in matrix for city in cities)
    for i in cities:
        for j in cities:
            if i == j:
                assert matrix[i][j] == 0
            else:
                assert 50 <= matrix[i][j] <= 100

def test_generate_distance_matrix_empty():
    with pytest.raises(ValueError, match="Cities list cannot be empty."):
        generate_distance_matrix([])

def test_format_route():
    route = ["A", "B", "C", "A"]
    formatted = format_route(route)
    assert formatted == "A -> B -> C -> A"
