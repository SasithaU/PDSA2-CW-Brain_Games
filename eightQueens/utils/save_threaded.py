# utils/save_threaded.py

import time
from src.algorithm.backtracking_threaded import solve_n_queens_threaded
from db.connection import get_connection

def save_threaded_results():
    start = time.time()
    solutions = solve_n_queens_threaded()
    end = time.time()
    total_duration_ms = (end - start) * 1000  # Total time for all solutions

    try:
        conn = get_connection()
        cursor = conn.cursor()

        new_count = 0
        for sol in solutions:
            pos_str = ",".join(map(str, sol))

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
        print(f"✅ {new_count} threaded solutions inserted.")
        print(f"🕒 Total Time for Threaded: {total_duration_ms:.2f} ms")

    except Exception as e:
        print("Threaded error:", e)
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
    return total_duration_ms 

if __name__ == "__main__":
    save_threaded_results()
