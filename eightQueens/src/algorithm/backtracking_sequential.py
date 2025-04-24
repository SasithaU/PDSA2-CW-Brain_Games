# # src/algorithm/backtracking_sequential.py

def is_safe(board, row, col):
    for i in range(row):
        if board[i] == col or abs(board[i] - col) == abs(i - row):
            return False
    return True

def solve_n_queens_sequential():
    solutions = []

    def backtrack(row, board):
        try:
            if row == 8:
                solutions.append(tuple(board))
                return
            for col in range(8):
                if is_safe(board, row, col):
                    board[row] = col
                    backtrack(row + 1, board)
        
        except RecursionError as e:
            print(f"Backtrack error - Max recursion depth exceeded: {e}")
            
        except Exception as e:
            print(f"An error occurred while backtracking: {e}")
            raise
    try:
        board = [-1] * 8
        backtrack(0, board)
    except Exception as e:
        print(f"An error occurred in the solve_n_queens_sequential function: {e}")
    return solutions

