import unittest
from knights_tour import (backtracking_knights_tour
                          , ROWS, COLS)



class TestBacktrackingKnightTour(unittest.TestCase):

    def test_backtracking_solution_exists(self):
        board = [[-1 for _ in range(COLS)] for _ in range(ROWS)]
        x, y = 0, 0
        board[y][x] = 0
        result = backtracking_knights_tour(board, x, y, 1)
        self.assertTrue(result)
        self.assertTrue(all(all(cell != -1 for cell in row) for row in board))

    def test_invalid_start_position(self):
        board = [[-1 for _ in range(COLS)] for _ in range(ROWS)]
        x, y = -1, -1
        with self.assertRaises(IndexError):
            board[y][x] = 0
            backtracking_knights_tour(board, x, y, 1)
            
            
if __name__ == '__main__':
    unittest.main()
