import unittest
from database import connect, initialize_database, save_player_name, save_game_result

class TestDatabaseReal(unittest.TestCase):

    def setUp(self):
        self.conn = connect()
        self.cursor = self.conn.cursor()
        self.test_player = "TestPlayer"
        self.test_result_data = {
            "player_name": self.test_player,
            "player_type": "X",
            "algorithm_used": "minimax",
            "move_time": 1.23,
            "result": "win"
        }

        #Make sure database and tables exist
        initialize_database()

        #Before test, clean the data from the tables
        self.cursor.execute("DELETE FROM players WHERE player_name = %s", (self.test_player,))
        self.cursor.execute("DELETE FROM game_results WHERE player_name = %s", (self.test_player,))
        self.conn.commit()

    #Test the player name save correctly in the database
    def test_save_player_name(self):
        save_player_name(self.test_player)
        self.cursor.execute("SELECT * FROM players WHERE player_name = %s", (self.test_player,))
        result = self.cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[1], self.test_player)

    #Test the game results save correctly in the database
    def test_save_game_result(self):
        save_game_result(**self.test_result_data)
        self.cursor.execute("SELECT * FROM game_results WHERE player_name = %s", (self.test_player,))
        result = self.cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[1], self.test_player)
        self.assertEqual(result[2], self.test_result_data["player_type"])
        self.assertEqual(result[3], self.test_result_data["algorithm_used"])
        self.assertAlmostEqual(result[4], self.test_result_data["move_time"], places=2)
        self.assertEqual(result[5], self.test_result_data["result"])

    #After test, clean the data from the tables
    def tearDown(self):
        self.cursor.execute("DELETE FROM players WHERE player_name = %s", (self.test_player,))
        self.cursor.execute("DELETE FROM game_results WHERE player_name = %s", (self.test_player,))
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

if __name__ == '__main__':
    unittest.main()
