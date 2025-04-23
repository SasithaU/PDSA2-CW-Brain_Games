import mysql.connector

def test_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="badagediya",
            database="knights_tour_game"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT DATABASE();")
        print("Connected to:", cursor.fetchone())
        cursor.close()
        conn.close()
    except Exception as e:
        print("Connection failed:", e)

test_db_connection()
