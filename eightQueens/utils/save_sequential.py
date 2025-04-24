# utils/save_sequential.py

import time
from src.algorithm.backtracking_sequential import solve_n_queens_sequential
from db.connection import get_connection

def save_sequential_results():
    start = time.time()
    solutions = solve_n_queens_sequential()
    end = time.time()
    total_duration_ms = (end - start) * 1000

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("TRUNCATE TABLE sequential_solutions")
        conn.commit()

        new_count = 0
        for sol in solutions:
            pos_str = str([(row, col) for row, col in enumerate(sol)])

            cursor.execute(
                "INSERT INTO sequential_solutions (positions, time_taken_ms) VALUES (%s, %s)",
                (pos_str, total_duration_ms)
            )
            new_count += 1

        # Insert timing for this run
        cursor.execute(
            "INSERT INTO timings (algorithm_type, time_taken_ms) VALUES (%s, %s)",
            ("sequential", total_duration_ms)
        )

        conn.commit()
        print(f"🕒 Total Time for Sequential: {new_count} in {total_duration_ms:.2f} ms")

    except ModuleNotFoundError as e:
        print("Sequential error - Module not found:", e)

    except ConnectionError as e:
        print("Sequential error - DB connection failed:", e)
        
    except RuntimeError as e:
        print("Sequential error - Runtime issue:", e)

    except Exception as e:
        print("Sequential error:", e)
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
    return total_duration_ms

if __name__ == "__main__":
    save_sequential_results()

