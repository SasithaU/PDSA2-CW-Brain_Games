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
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS computer_moves (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    game_id INT,
                    move_number INT,
                    time_taken DOUBLE,
                    algorithm_used VARCHAR(50),
                    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (game_id) REFERENCES game_results(id)
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
            game_id = cursor.lastrowid
            cursor.close()
            conn.close()
            return game_id
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

#Save the data into the computer_move table
def save_computer_move(game_id, move_number, time_taken, algorithm_used):
    try:
        conn = connect()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO computer_moves (game_id, move_number, time_taken, algorithm_used)
                VALUES (%s, %s, %s, %s)
            """, (game_id, move_number, time_taken, algorithm_used))
            conn.commit()
            cursor.close()
            conn.close()
    except Error as e:
        print(f"Error saving computer move: {e}")

# Update the final result of a game
def update_game_result(game_id, winner, time_taken, result):
    try:
        conn = connect()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE game_results
                SET player_type = %s, time_taken = %s, result = %s
                WHERE id = %s
            """, (winner, time_taken, result, game_id))
            conn.commit()
            cursor.close()
            conn.close()
    except Error as e:
        print(f"Error updating game result: {e}")



