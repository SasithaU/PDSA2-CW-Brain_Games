import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import time
from algorithms import get_computer_move_minimax, get_computer_move_alphabeta
from database import save_game_result, save_player_name
import game_validation
import uiValidation_messages

TILE_SIZE = 140
BOARD_SIZE = 5
WIDTH = TILE_SIZE * BOARD_SIZE
HEIGHT = TILE_SIZE * BOARD_SIZE + 180

player_name = "Player"
selected_difficulty = "Easy"

def start_classic_ui(): #Function to handle the main game UI
    global player_name, selected_difficulty
    root = tk.Tk()
    root.title("Classic Tic Tac Toe")
    root.resizable(False, False)

    x_img = Image.open("tic_tac_toe_game/assets/X.png").resize((100, 100))
    o_img = Image.open("tic_tac_toe_game/assets/O.png").resize((100, 100))
    x_photo = ImageTk.PhotoImage(x_img)
    o_photo = ImageTk.PhotoImage(o_img)

    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
    canvas.pack()

    board = [[" " for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    last_computer_time = [0]
    algorithm_used = ["minimax"]
    
    def draw_board():  #UI design for the tic-tac-toe board
     for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            canvas.create_rectangle(
                j * TILE_SIZE, i * TILE_SIZE + 100,
                (j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE + 100,
                fill="#945034" ,
                outline="black",
                width=2
            )
            symbol = board[i][j]
            if symbol != " ":
                canvas.create_text(
                    j * TILE_SIZE + TILE_SIZE // 2,
                    i * TILE_SIZE + 100 + TILE_SIZE // 2,
                    text=symbol,
                    font=("Helvetica", 28, "bold"),
                    fill="red" if symbol == "X" else "blue"
                )

    def place_symbol(i, j, symbol):
        x = j * TILE_SIZE + TILE_SIZE // 2
        y = i * TILE_SIZE + TILE_SIZE // 2 + 100
        img = x_photo if symbol == "X" else o_photo
        canvas.create_image(x, y, image=img)
        canvas.image = img

    def check_winner(move_time=0): #Function to check the winner of the game
        from main import show_main_menu
        winner = game_validation.get_winner(board)

        if winner:
            print(">>> Winner found:", winner)
            uiValidation_messages.show_game_over(winner)
            end_game(winner, move_time)
            root.destroy()
            show_main_menu()

        elif game_validation.is_board_full(board):
            print(">>> No winner, but board is full. Game is a draw.")
            uiValidation_messages.show_game_over("Draw")
            end_game("Draw", move_time)
            root.destroy()
            show_main_menu()
        else:
            print(">>> Game not finished yet.")

    def end_game(winner, move_time): 
        print(f"Ending game. Winner: {winner}, Move time: {move_time}")
        algo = algorithm_used[0] if algorithm_used else "N/A" # Fallback for algorithm_used

        if winner == "Draw":
            save_game_result(player_name, "-", algo, 0, "Draw")
        else:
            result = "Win" if winner == "X" else "Lose"
            save_game_result(player_name, winner, algo, move_time if winner == "O" else 0, result)
        reset_game()
    
    def reset_game(): #Function to reset UI and board state
        canvas.delete("all")
        draw_board()
        canvas.create_text(WIDTH // 2, 40, text=f"Welcome, {player_name} ({selected_difficulty})!", font=("Georgia", 18), fill="black")
        for i in range(BOARD_SIZE): #Clear board data
            for j in range(BOARD_SIZE):
                board[i][j] = " "

    def handle_click(event):
        col = event.x // TILE_SIZE #Get the grid position from the mouse click
        row = (event.y - 100) // TILE_SIZE
        if not game_validation.is_valid_move(board, row, col):
            uiValidation_messages.show_invalid_move()
            return
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and board[row][col] == " ":
            board[row][col] = "X"
            place_symbol(row, col, "X")
            winner = game_validation.get_winner(board)
        if winner or game_validation.is_board_full(board):
            check_winner(0)  # Human wins, so move_time is 0
            return

        # Computer's move using selected algorithm and its timing
        start = time.time()
        if selected_difficulty == "Hard":
            move = get_computer_move_minimax(board)
            algorithm_used[0] = "minimax"
        else:
            move = get_computer_move_alphabeta(board)
            algorithm_used[0] = "alpha-beta"
        end = time.time()

        move_time = round((end - start) * 1000, 3)
        last_computer_time[0] = move_time

        if move:
            r, c = move
            if board[r][c] == " ":
                board[r][c] = "O"
                place_symbol(r, c, "O")
                winner = game_validation.get_winner(board)
                if winner or game_validation.is_board_full(board):
                    check_winner(move_time)
    
    canvas.bind("<Button-1>", handle_click)
    draw_board()
    canvas.create_text(WIDTH // 2, 40, text=f"Welcome, {player_name} ({selected_difficulty})!", font=("Georgia", 18), fill="black")

    back_btn = tk.Button(root, text="Back", font=("Georgia", 12), command=lambda: [root.destroy(), show_main_menu()])
    canvas.create_window(WIDTH - 70, 40, window=back_btn)

    root.mainloop()

def show_rules():
    rules_text = (
        "Welcome to 5x5 Tic Tac Toe!\n\n"
        "- You are 'X'. The computer is 'O'.\n"
        "- First to align 5 in a row, column, or diagonal wins.\n"
        "- If the board fills with no winner, it's a draw.\n\n"


        "- Can you beat the board and win?\n\n"
        "- Good luck, Player!\n"
    )
    messagebox.showinfo("Game Rules", rules_text)

def show_main_menu():
    def start_game():
        name = name_entry.get().strip()
        difficulty = difficulty_var.get()

        # Validate the inputs using uiValidation_messages
        if not uiValidation_messages.validate_inputs(name, difficulty):
            return

        global player_name, selected_difficulty
        player_name = name
        selected_difficulty = difficulty
        save_player_name(player_name)
        root.destroy()
        start_classic_ui()

    def exit_game():
        root.destroy()

    #Welcome Screen UI Design
    root = tk.Tk()
    root.title("Welcome to Tic Tac Toe")
    root.geometry("700x800")
    root.resizable(False, False)

    bg_img = Image.open("tic_tac_toe_game/assets/tictactoe.jpg").resize((700, 800))
    bg_photo = ImageTk.PhotoImage(bg_img)

    canvas = tk.Canvas(root, width=700, height=800)
    canvas.pack()
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")

    input_frame = tk.Frame(root, bg="#854836")
 
    name_label = tk.Label(input_frame, text="Enter Your Name", font=("Georgia", 18), bg="#854836",fg="white")
    name_label.pack(pady=(10, 5))

    name_entry = tk.Entry(input_frame, font=("Georgia", 14), justify="center", width=25)
    name_entry.pack(pady=(0, 15))

    difficulty_label = tk.Label(input_frame, text="Select Difficulty", font=("Georgia", 16), bg="#D29F80")
    difficulty_label.pack(pady=(0, 5))

    difficulty_var = tk.StringVar(value="Easy")
    easy_radio = tk.Radiobutton(input_frame, text="Easy", variable=difficulty_var, value="Easy", font=("Georgia", 12), bg="#854836",fg="white")
    hard_radio = tk.Radiobutton(input_frame, text="Hard", variable=difficulty_var, value="Hard", font=("Georgia", 12), bg="#854836",fg="white")
    easy_radio.pack()
    hard_radio.pack()

    canvas.create_window(350, 250, window=input_frame)
    start_btn = tk.Button(root, text="Start", font=("Georgia", 16), width=25, bg="green",fg="white",activebackground="#228B22", command=start_game)
    rules_btn = tk.Button(root, text="Rules", font=("Georgia", 16), width=25, bg="saddlebrown",fg="white",activebackground="#8B4513", command=show_rules)
    exit_btn = tk.Button(root, text="Exit", font=("Georgia", 16), width=25,bg="red",fg="white",activebackground="#8B0000", command=exit_game)

    canvas.create_window(350, 550, window=start_btn)
    canvas.create_window(350, 620, window=rules_btn)
    canvas.create_window(350, 690, window=exit_btn)

    root.mainloop()
