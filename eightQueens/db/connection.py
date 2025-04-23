# db/connection.py
import mysql.connector
from mysql.connector import Error
from ui.message_ui import show_error

def get_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="admin123",
            database="eight_queens_game"
        )
        return connection
    except Error as e:
        show_error("Database Connection Error", f"Unable to connect to database:\n{e}")
        
        # For CLI or logs
        print(f"Failed to connect to the database: {e}")
        return None
