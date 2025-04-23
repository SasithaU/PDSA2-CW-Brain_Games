import mysql.connector
from mysql.connector import Error

#DB Connection
def connect():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="Sandu@20020409",
            database="tictactoe_game"
        )
    except Error as e:
        print(f"Database connection failed: {e}")
        return None

#Initialize the tables in the database
def initialize_database():
    conn = connect()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS players (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    player_name VARCHAR(50),
                    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS game_results (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    player_name VARCHAR(50),
                    player_type CHAR(1),
                    algorithm_used VARCHAR(50),
                    time_taken DOUBLE,
                    result VARCHAR(10),
                    played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
        except Error as e:
            print(f"Error creating tables: {e}")
        finally:
            cursor.close()
            conn.close()

#Save the data into the game_results table
def save_game_result(player_name, player_type, algorithm_used, move_time, result):
    try:
        conn = connect()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO game_results (player_name, player_type, algorithm_used, time_taken, result)
                VALUES (%s, %s, %s, %s, %s)
            """, (player_name, player_type, algorithm_used, move_time, result))
            conn.commit()
            cursor.close()
            conn.close()
    except Error as e:
        print(f"Error saving game result: {e}")

#Save the data into the players table
def save_player_name(player_name):
    try:
        conn = connect()
        if conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO players (player_name) VALUES (%s)", (player_name,))
            conn.commit()
            cursor.close()
            conn.close()
    except Error as e:
        print(f"Error saving player name: {e}")
