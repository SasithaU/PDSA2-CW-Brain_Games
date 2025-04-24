# utils/save_threaded.py

import time
from src.algorithm.backtracking_threaded import solve_n_queens_threaded
from db.connection import get_connection

def save_threaded_results():
    start = time.time()
    solutions = solve_n_queens_threaded()
    end = time.time()
    total_duration_ms = (end - start) * 1000  

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("TRUNCATE TABLE threaded_solutions")
        conn.commit()

        new_count = 0
        for sol in solutions:
            pos_str = str([(row, col) for row, col in enumerate(sol)])

            cursor.execute(
                "INSERT INTO threaded_solutions (positions, time_taken_ms) VALUES (%s, %s)",
                (pos_str, total_duration_ms)  # Store total time for the threaded process
            )
            new_count += 1

        # Insert overall timing for the threaded algorithm into the 'timings' table
        cursor.execute(
            "INSERT INTO timings (algorithm_type, time_taken_ms) VALUES (%s, %s)",
            ("threaded", total_duration_ms)
        )

        conn.commit()
        print(f"🕒 Total Time for Threaded: {new_count} in {total_duration_ms:.2f} ms")
    
    except ModuleNotFoundError as e:
        print("Threaded error - Module not found:", e)

    except ConnectionError as e:
        print("Threaded error - Could not connect to DB:", e)

    except TypeError as e:
        print("Threaded error - Type mismatch:", e)

    except ValueError as e:
        print("Threaded error - Value error:", e)

    except Exception as e:
        print("Threaded error:", e)
        
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
    return total_duration_ms 

if __name__ == "__main__":
    save_threaded_results()
