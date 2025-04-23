# src/algorithm/backtracking_threaded.py

import threading

solutions = []
lock = threading.Lock()

def is_safe(board, row, col):
    for i in range(row):
        if board[i] == col or abs(board[i] - col) == abs(i - row):
            return False
    return True

def thread_solve(start_col):
    def backtrack(row, board):
        if row == 8:
            with lock:
                solutions.append(tuple(board))  # Protect the shared list
            return
        for col in range(8):
            if is_safe(board, row, col):
                board[row] = col
                backtrack(row + 1, board)

    board = [-1] * 8
    board[0] = start_col
    try:
        backtrack(1, board)
    except Exception as e:
        print(f"Error occurred in backtracking thread for column {start_col}: {e}")

def solve_n_queens_threaded():
    threads = []
    try:
        for col in range(8):
            t = threading.Thread(target=thread_solve, args=(col,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()
    except Exception as e:
        print(f"An error occurred while managing threads: {e}")
    return solutions
