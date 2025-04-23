import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import unittest
from game.logic import brute_force_tsp, greedy_tsp, dp_tsp
from game.utils import generate_distance_matrix, format_route
from db.models import save_result, get_leaderboard
from db.connect import get_connection


class TestTSPGame(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cities = ["A", "B", "C", "D"]
        cls.home = "A"
        cls.matrix = {
            'A': {'A': 0, 'B': 60, 'C': 70, 'D': 80},
            'B': {'A': 60, 'B': 0, 'C': 65, 'D': 75},
            'C': {'A': 70, 'B': 65, 'C': 0, 'D': 85},
            'D': {'A': 80, 'B': 75, 'C': 85, 'D': 0}
        }

    def test_TC_001_brute_force_tsp(self):
        """Test Brute Force TSP algorithm"""
        route, dist, t = brute_force_tsp(self.matrix, self.home, ["B", "C", "D"])
        self.assertIsInstance(route, list)
        self.assertGreater(dist, 0)

    def test_TC_002_greedy_tsp(self):
        """Test Greedy TSP algorithm"""
        route, dist, t = greedy_tsp(self.matrix, self.home, ["B", "C", "D"])
        self.assertIsInstance(route, list)
        self.assertGreater(dist, 0)

    def test_TC_003_dp_tsp(self):
        """Test DP TSP algorithm"""
        route, dist, t = dp_tsp(self.matrix, self.home, ["B", "C", "D"])
        self.assertIsInstance(route, list)
        self.assertGreater(dist, 0)

    def test_TC_004_generate_distance_matrix(self):
        """Test Generate Distance Matrix utility"""
        matrix = generate_distance_matrix(["A", "B", "C"])
        self.assertIn("A", matrix)
        self.assertIn("B", matrix["A"])

    def test_TC_005_format_route(self):
        """Test Format Route utility"""
        route_str = format_route(["A", "B", "C"])
        self.assertEqual(route_str, "A -> B -> C")

    def test_TC_006_database_connection(self):
        """Test Database Connection"""
        conn = get_connection()
        self.assertIsNotNone(conn)
        conn.close()

    def test_TC_007_save_and_get_leaderboard(self):
        """Test Save and Retrieve Leaderboard"""
        save_result("UnitTester", "A", ["B", "C", "D"],
                    ["A", "B", "C", "D", "A"],
                    "Greedy", 1.23, 1, 1)
        leaderboard = get_leaderboard()
        self.assertGreaterEqual(len(leaderboard), 1)


# Custom Test Result class to print structured results
class CustomTestResult(unittest.TextTestResult):
    def addSuccess(self, test):
        super().addSuccess(test)
        print(f"{test._testMethodName} | {test.shortDescription()} | Pass | Pass | -")

    def addFailure(self, test, err):
        super().addFailure(test, err)
        print(f"{test._testMethodName} | {test.shortDescription()} | Fail | Fail | {err}")

    def addError(self, test, err):
        super().addError(test, err)
        print(f"{test._testMethodName} | {test.shortDescription()} | Error | Error | {err}")


# Custom Test Runner using the above result class
class CustomTestRunner(unittest.TextTestRunner):
    def _makeResult(self):
        return CustomTestResult(self.stream, self.descriptions, self.verbosity)


if __name__ == "__main__":
    print("Test Case ID | Test Description | Expected Result | Actual Result | Status | Remarks")
    print("-" * 110)
    unittest.main(testRunner=CustomTestRunner(), verbosity=2)
