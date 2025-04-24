# db/connection.py

import mysql.connector
from mysql.connector import Error
from ui.message_ui import show_error

def get_connection(is_test=False):
    connection = None
    try:
        if is_test:
            # For testing, connect to MySQL server and create a temporary test database
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="admin123"
            )
            
            cursor = connection.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS temp_test_db;")
            connection.database = "temp_test_db"  # Switch to the temp database

            # Set up tables here for testing
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS solutions (
                sol_id INT AUTO_INCREMENT PRIMARY KEY,
                positions TEXT,
                is_found BOOLEAN
            );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS players (
                    player_id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(50) NOT NULL,
                    positions TEXT,
                    solution_id INT,
                    FOREIGN KEY (solution_id) REFERENCES solutions(sol_id)
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sequential_solutions (
                    sol_id INT AUTO_INCREMENT PRIMARY KEY,
                    positions TEXT,
                    is_found BOOLEAN
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS threaded_solutions (
                    sol_id INT AUTO_INCREMENT PRIMARY KEY,
                    positions TEXT,
                    is_found BOOLEAN
                );
            """)

        else:
            # For production, connect to the actual database
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="admin123",
                database="eight_queens_game"
            )
        return connection
    
    except DatabaseError as e:
        show_error("Database Error", f"A database-level error occurred:\n{e}")
        print(f"📂 DatabaseError: {e}")
    
    except Exception as e:
        show_error("Unexpected Error", f"An unexpected error occurred:\n{e}")
        print(f"🚨 Unexpected error: {e}")

    except Error as e:
        show_error("Database Connection Error", f"Unable to connect to database:\n{e}")
        print(f"Failed to connect to the database: {e}")
        return None
