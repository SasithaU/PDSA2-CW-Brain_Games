



import unittest
from unittest.mock import patch, MagicMock
from knights_tour import (
    get_valid_moves,
    solve_knights_tour_no_ui,
    # backtracking_knights_tour,
    save_winner_to_db,
    ROWS, COLS
)

class TestKnightTour(unittest.TestCase):

    def test_get_valid_moves_center(self):
        visited = [(3, 3)]
        moves = get_valid_moves((3, 3), visited)
        expected_count = 8
        self.assertEqual(len(moves), expected_count)

    def test_get_valid_moves_corner(self):
        visited = [(0, 0)]
        moves = get_valid_moves((0, 0), visited)
        expected = [(2, 1), (1, 2)]
        self.assertEqual(set(moves), set(expected))

    def test_knights_tour_solution_exists(self):
        board = [[-1 for _ in range(8)] for _ in range(8)]
        board[0][0] = 0
        result = solve_knights_tour_no_ui(board, 0, 0, 1)
        self.assertTrue(result)

    def test_knights_tour_incomplete_board(self):
        board = [[-1 for _ in range(8)] for _ in range(8)]
        board[0][0] = 0
        board[1][2] = 99
        board[2][1] = 99
        result = solve_knights_tour_no_ui(board, 0, 0, 1)
        self.assertFalse(result)

# class TestBacktrackingKnightTour(unittest.TestCase):

#     def test_backtracking_solution_exists(self):
#         board = [[-1 for _ in range(COLS)] for _ in range(ROWS)]
#         x, y = 0, 0
#         board[y][x] = 0
#         result = backtracking_knights_tour(board, x, y, 1)
#         self.assertTrue(result)
#         self.assertTrue(all(all(cell != -1 for cell in row) for row in board))

#     def test_invalid_start_position(self):
#         board = [[-1 for _ in range(COLS)] for _ in range(ROWS)]
#         x, y = -1, -1
#         with self.assertRaises(IndexError):
#             board[y][x] = 0
#             backtracking_knights_tour(board, x, y, 1)

# class TestDatabase(unittest.TestCase):

#     @patch("knights_tour.mysql.connector.connect")
#     def test_save_winner_to_db_success(self, mock_connect):
#         mock_conn = MagicMock()
#         mock_cursor = MagicMock()
#         mock_connect.return_value = mock_conn
#         mock_conn.cursor.return_value = mock_cursor

#         save_winner_to_db("TestUser", 64)

#         mock_cursor.execute.assert_called_once()
#         mock_conn.commit.assert_called_once()
#         mock_cursor.close.assert_called_once()
#         mock_conn.close.assert_called_once()

#     @patch("knights_tour.mysql.connector.connect", side_effect=Exception("DB error"))
#     def test_save_winner_to_db_error_handling(self, mock_connect):
#         try:
#             save_winner_to_db("TestUser", 64)
#         except Exception:
#             self.fail("save_winner_to_db raised an exception unexpectedly!")

if __name__ == '__main__':
    unittest.main()
