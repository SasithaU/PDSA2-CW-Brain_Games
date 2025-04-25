# import mysql.connector

# def test_db_connection():
#     try:
#         conn = mysql.connector.connect(
#             host="localhost",
#             user="root",
#             password="badagediya",
#             database="knights_tour_game"
#         )
#         cursor = conn.cursor()
#         cursor.execute("SELECT DATABASE();")
#         print("Connected to:", cursor.fetchone())
#         cursor.close()
#         conn.close()
#     except Exception as e:
#         print("Connection failed:", e)

# test_db_connection()





import unittest
import mysql.connector

class TestDatabaseConnection(unittest.TestCase):

    def test_connection_to_database(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="badagediya",
                database="knights_tour_game"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT DATABASE();")
            current_db = cursor.fetchone()[0]

            self.assertEqual(current_db, "knights_tour_game", "Connected to the wrong database")

        except mysql.connector.Error as err:
            self.fail(f"MySQL connection failed with error: {err}")

        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

if __name__ == '__main__':
    unittest.main()

