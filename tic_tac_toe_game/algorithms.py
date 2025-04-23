import random
from game_validation import validate_board

def evaluate(board, player): #Function to evaluate the current board state
    opponent = "X" if player == "O" else "O"
    def score_line(line):
        if line.count(player) == 5:
            return 100
        elif line.count(player) == 4 and line.count(" ") == 1:
            return 10
        elif line.count(player) == 3 and line.count(" ") == 2:
            return 5
        elif line.count(opponent) == 5:
            return -100
        return 0

    score = 0
    for i in range(5):
        score += score_line(board[i])  # row
        score += score_line([board[j][i] for j in range(5)])  # col

    score += score_line([board[i][i] for i in range(5)])
    score += score_line([board[i][4 - i] for i in range(5)])

    return score

def check_winner(b, p): #Function to check whether the specified player ('X' or 'O') has won the game
    try:
        validate_board(b)
        if p not in ["X", "O"]:
            raise ValueError("Player must be 'X' or 'O'.")
        for i in range(5):
            if all(b[i][j] == p for j in range(5)) or all(b[j][i] == p for j in range(5)):
                return True
        if all(b[i][i] == p for i in range(5)) or all(b[i][4 - i] == p for i in range(5)):
                return True
        return False
    except Exception as e:
        print(f"Error in check_winner: {e}")
        return False

def is_draw(board): #Function to check whether the game is a draw or not
    try:
        validate_board(board)
        return all(cell != " " for row in board for cell in row)
    except Exception as e:
        print(f"Error in is_draw: {e}")
        return False

def get_available_moves(board): #Function to return the all available positions on the board
    try:
        validate_board(board)
        return [(i, j) for i in range(5) for j in range(5) if board[i][j] == " "]
    except Exception as e:
        print(f"Error in get_available_moves: {e}")
        return []

#Minimax Algo
def minimax(board, depth, is_maximizing, player):
    try:
        validate_board(board)
        if player not in ["X", "O"]:
            raise ValueError("Player must be 'X' or 'O'.")
        if not isinstance(depth, int) or depth < 0:
            raise ValueError("Depth must be a non-negative integer.")
        
        opponent = "X" if player == "O" else "O"
        last_player = opponent if is_maximizing else player

        if check_winner(board, last_player):
            return 100 if last_player == player else -100
        if is_draw(board):
            return 0
        if depth == 0:
            return evaluate(board, player)

        best_score = float('-inf') if is_maximizing else float('inf')

        for i in range(5):
            for j in range(5):
                if board[i][j] == " ":
                    board[i][j] = player if is_maximizing else opponent
                    score = minimax(board, depth - 1, not is_maximizing, player)
                    board[i][j] = " "

                    if is_maximizing:
                        best_score = max(best_score, score)
                    else:
                        best_score = min(best_score, score)

        return best_score
    except Exception as e:
        print(f"Error in minimax: {e}")
        return 0

def get_computer_move_minimax(board): #Function to determine the best move for the computer using minimax algo
    best_score = float('-inf')
    best_move = None

    for i in range(5):
        for j in range(5):
            if board[i][j] == " ":
                board[i][j] = "O"
                score = minimax(board, 2, False, "O")
                board[i][j] = " "
                if score > best_score:
                    best_score = score
                    best_move = (i, j)

    return best_move

#Alpha beta pruning algorithm
def alphabeta(board, depth, alpha, beta, is_maximizing, player):
    try:
        validate_board(board)
        if player not in ["X", "O"]:
            raise ValueError("Player must be 'X' or 'O'.")
        if not isinstance(depth, int) or depth < 0:
            raise ValueError("Depth must be a non-negative integer.")
        opponent = "X" if player == "O" else "O"

        if check_winner(board, player):
            return 100
        if check_winner(board, opponent):
            return -100
        if is_draw(board):
            return 0
        if depth == 0:
            return evaluate(board, player)

        if is_maximizing:
            max_eval = float('-inf')
            for i in range(5):
                for j in range(5):
                    if board[i][j] == " ":
                        board[i][j] = player
                        eval = alphabeta(board, depth - 1, alpha, beta, False, player)
                        board[i][j] = " "
                        max_eval = max(max_eval, eval)
                        alpha = max(alpha, eval)
                        if beta <= alpha:
                            break
            return max_eval
        else:
            min_eval = float('inf')
            for i in range(5):
                for j in range(5):
                    if board[i][j] == " ":
                        board[i][j] = opponent
                        eval = alphabeta(board, depth - 1, alpha, beta, True, player)
                        board[i][j] = " "
                        min_eval = min(min_eval, eval)
                        beta = min(beta, eval)
                        if beta <= alpha:
                            break
        return min_eval
    except Exception as e:
        print(f"Error in alphabeta: {e}")
        return 0

def get_computer_move_alphabeta(board): #Function to determine the best move for the computer using alphabeta algo
    best_score = float('-inf')
    best_move = None

    for i in range(5):
        for j in range(5):
            if board[i][j] == " ":
                board[i][j] = "O"
                score = alphabeta(board, 2, float('-inf'), float('inf'), False, "O")
                board[i][j] = " "
                if score > best_score:
                    best_score = score
                    best_move = (i, j)

    return best_move
