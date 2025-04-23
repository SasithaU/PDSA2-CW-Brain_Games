import unittest
from hanoi_algorithm import solve_hanoi_recursive, solve_hanoi_iterative
from unittest.mock import patch, MagicMock
import database

class TestHanoAlgorithms(unittest.TestCase):
    def test_recursive_3_disks(self):
        result = solve_hanoi_recursive(3, 'A', 'C', 'B')
        print("Recursive result:", result)
        expected_moves = [('A', 'C'), ('A', 'B'), ('C', 'B'), ('A', 'C'), ('B', 'A'), ('B', 'C'), ('A', 'C')]
        self.assertEqual(result, expected_moves)

    def test_iterative_3_disks(self):
        result = solve_hanoi_iterative(3, 'A', 'C', 'B')
        print("Iterative result:", result)
        expected_moves = [('A', 'C'), ('A', 'B'), ('C', 'B'), ('A', 'C'), ('B', 'A'), ('B', 'C'), ('A', 'C')]
        self.assertEqual(result, expected_moves)

    def test_recursive_4_disks(self):
        result = solve_hanoi_recursive(4, 'A', 'C', 'B')
        print("Recursive result:", result)
        expected_moves = [('A', 'B'), ('A', 'C'), ('B', 'C'), ('A', 'B'), ('C', 'A'), ('C', 'B'), ('A', 'B'), ('A', 'C'), 
                          ('B', 'C'), ('B', 'A'), ('C', 'A'), ('B', 'C'), ('A', 'B'), ('A', 'C'), ('B', 'C')]
        self.assertEqual(result, expected_moves)

class TestDatabaseFunctions(unittest.TestCase):

    @patch('database.mysql.connector.connect')
    def test_connect_db_success(self, mock_connect):
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection

        database.connect_db()
        self.assertIsNotNone(database.mydb)
        mock_connect.assert_called_once()

    

if __name__ == '__main__':
    unittest.main(exit=False)

if __name__ == '__main__':
    unittest.main(exit=False)
