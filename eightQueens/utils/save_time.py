# utils/save_time.py

import time
from db.connection import get_connection
from src.algorithm.backtracking_sequential import solve_n_queens_sequential
from src.algorithm.backtracking_threaded import solve_n_queens_threaded

def record_timing(algo_name, func):
    try:
        start = time.time()
        func()
        end = time.time()
        time_taken = (end - start) * 1000  # in ms

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO timings (algorithm_type, time_taken_ms) VALUES (%s, %s)",
            (algo_name, time_taken)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"An error occurred while recording timing: {e}")