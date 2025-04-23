# src/solution_controller.py
from db.connection import get_connection
from ui.message_ui import show_error

def insert_player_solution(name, positions, solution_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO players (name, positions, solution_id) VALUES (%s, %s, %s)",
            (name, str(positions), solution_id)
        )
        cursor.execute("UPDATE solutions SET is_found = TRUE WHERE id = %s", (solution_id,))
        conn.commit()
    except Exception as e:
        show_error("Database Error", f"Failed to save solution: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

def get_all_solutions():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, positions, is_found FROM solutions")
        results = cursor.fetchall()
        return results
    except Exception as e:
        show_error("Database Error", f"Failed to retrieve solutions: {e}")
        return []
    finally:
        if 'conn' in locals():
            conn.close()

def reset_all_solution_flags():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE solutions SET is_found = FALSE")
        conn.commit()
    except Exception as e:
        show_error("Database Error", f"Failed to reset solution flags: {e}")
    finally:
        if 'conn' in locals():
            conn.close()