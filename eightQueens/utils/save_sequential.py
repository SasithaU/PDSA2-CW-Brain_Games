# utils/save_sequential.py

import time
from src.algorithm.backtracking_sequential import solve_n_queens_sequential
from db.connection import get_connection

def save_sequential_results():
    start = time.time()
    solutions = solve_n_queens_sequential()
    end = time.time()
    total_duration_ms = (end - start) * 1000  # Total time taken for all solutions

    try:
        conn = get_connection()
        cursor = conn.cursor()

        new_count = 0
        for sol in solutions:
            pos_str = ",".join(map(str, sol))  # Convert solution to a comma-separated string

            cursor.execute(
                "INSERT INTO sequential_solutions (positions, time_taken_ms) VALUES (%s, %s)",
                (pos_str, total_duration_ms)  # Store total time for the process, or you can modify this based on your needs
            )
            new_count += 1

        # Insert overall timing for the sequential algorithm into the 'timings' table
        cursor.execute(
            "INSERT INTO timings (algorithm_type, time_taken_ms) VALUES (%s, %s)",
            ("sequential", total_duration_ms)
        )

        conn.commit()
        print(f"✅ {new_count} sequential solutions inserted.")
        print(f"🕒 Total Time for Sequential: {total_duration_ms:.2f} ms")

    except Exception as e:
        print("Sequential error:", e)
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
    return total_duration_ms 

if __name__ == "__main__":
    save_sequential_results()



# Solves the 8-Queens puzzle using a sequential backtracking algorithm.
# Measures how long it takes to find all solutions.
# Saves each solution (as a comma-separated string) into the sequential_solutions table in the database.
# Also saves the total time taken into the timings table for performance tracking.
# Prints how many solutions were inserted and how long the process took.