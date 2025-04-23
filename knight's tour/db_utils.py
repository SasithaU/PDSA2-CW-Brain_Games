import mysql.connector

def save_winner_to_db(name, move_count):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="badagediya",
            database="knights_tour_game"
        )
        cursor = conn.cursor()
        cursor.execute("INSERT INTO winners (name, move_count) VALUES (%s, %s)", (name, move_count))
        conn.commit()
        cursor.close()
        conn.close()
        print("Data inserted successfully.")
    except Exception as e:
        print("Error saving to DB:", e)
