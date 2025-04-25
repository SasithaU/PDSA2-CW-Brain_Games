import unittest
import json
from db_utils import save_winner_to_db
import mysql.connector


class TestSaveWinnerToDB(unittest.TestCase):
    def setUp(self):
        # Setup test data
        self.player_name = "TestPlayer"
        self.move_count = 64
        self.path = [(0, 0), (2, 1), (4, 2), (6, 3)]  # example path, keep it short for testing

    def test_save_winner_to_db(self):
        # Save data
        save_winner_to_db(self.player_name, self.move_count, self.path)

        # Verify data was inserted
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="badagediya",
            database="knights_tour_game"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT name, move_count, path FROM winners WHERE name = %s ORDER BY id DESC LIMIT 1", (self.player_name,))
        result = cursor.fetchone()

        self.assertIsNotNone(result)
        self.assertEqual(result[0], self.player_name)
        self.assertEqual(result[1], self.move_count)
        # self.assertEqual(json.loads(result[2]), self.path)  # check if path was correctly stored as JSON
        self.assertEqual(json.loads(result[2]), [list(pos) for pos in self.path])

        cursor.close()
        conn.close()

    def tearDown(self):
        # Clean up inserted test record
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="badagediya",
            database="knights_tour_game"
        )
        cursor = conn.cursor()
        cursor.execute("DELETE FROM winners WHERE name = %s", (self.player_name,))
        conn.commit()
        cursor.close()
        conn.close()


if __name__ == "__main__":
    unittest.main()
