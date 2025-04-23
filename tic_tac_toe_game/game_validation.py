def validate_board(board): #Function to validate if it is a valid 5*5 board
    if not isinstance(board, list) or len(board) != 5:
        raise ValueError("Board must be a 5x5 list.")
    for row in board:
        if not isinstance(row, list) or len(row) != 5:
            raise ValueError("Each row in the board must be a list of length 5.")
        for cell in row:
            if cell not in ["X", "O", " "]:
                raise ValueError("Invalid cell value. Allowed values are 'X', 'O', or ' '.")

def is_valid_name(name): #Function to validate if it is a valid name
    try:
        return name.strip().isalpha()
    except AttributeError:
        print("Error: Invalid input for player name. Expected a string.")
        return False

def is_valid_difficulty(level): #Function to validate if it is a valid difficulty type
    return level in ["Easy", "Hard"]

def is_valid_move(board, row, col): #Function to validate if it is a valid move or not
    try:
        return 0 <= row < len(board) and 0 <= col < len(board[0]) and board[row][col] == " "
    except (IndexError, TypeError):
        print("Error: Invalid row or column index.")
        return False

def is_board_full(board): #Function to validate if the board is full
    try:
        return all(cell != " " for row in board for cell in row)
    except Exception as e:
        print(f"Error checking if board is full: {e}")
        return False

def get_winner(board): #Function to validate the winner behavior
    size = len(board)
    win_length = 5 

    def check_sequence(seq):
        count = 1
        for i in range(1, len(seq)):
            if seq[i] != " " and seq[i] == seq[i - 1]:
                count += 1
                if count == win_length:
                    return seq[i]
            else:
                count = 1
        return None

    # Check rows
    for row in board:
        winner = check_sequence(row)
        if winner:
            return winner

    # Check columns
    for col in range(size):
        column = [board[row][col] for row in range(size)]
        winner = check_sequence(column)
        if winner:
            return winner

    # Check diagonals
    for r in range(size - win_length + 1):
        for c in range(size - win_length + 1):
            # Top-left to bottom-right
            diag1 = [board[r + i][c + i] for i in range(win_length)]
            winner = check_sequence(diag1)
            if winner:
                return winner

            # Top-right to bottom-left
            diag2 = [board[r + i][c + win_length - 1 - i] for i in range(win_length)]
            winner = check_sequence(diag2)
            if winner:
                return winner
    return None

def is_game_over(board): #Function to validate if the game is over
    return get_winner(board) is not None or is_board_full(board)