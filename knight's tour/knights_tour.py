

######################




import pygame
import sys
import ctypes
import mysql.connector
from tkinter import simpledialog
import tkinter as tk
from db_utils import save_winner_to_db


# Constants
WIDTH, HEIGHT = 640, 690
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Colors
WHITE = (245, 245, 245)
GRAY = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER_COLOR = (100, 160, 210)
BUTTON_TEXT_COLOR = WHITE

# Button dimensions
BUTTON_WIDTH, BUTTON_HEIGHT = 120, 40
SOLVE_BUTTON_X = 100
RESET_BUTTON_X = 420
BUTTON_Y = HEIGHT - BUTTON_HEIGHT - 10

# Knight moves
KNIGHT_MOVES = [
    (2, 1), (1, 2), (-1, 2), (-2, 1),
    (-2, -1), (-1, -2), (1, -2), (2, -1)
]

# Pygame setup
pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Knight's Tour")

ctypes.windll.user32.MoveWindow(pygame.display.get_wm_info()['window'], 320, 3, WIDTH, HEIGHT, True)

# Load knight image and scale it
knight_img = pygame.image.load("knight's tour/knight.png")
knight_img = pygame.transform.scale(knight_img, (SQUARE_SIZE - 10, SQUARE_SIZE - 10))

button_font = pygame.font.SysFont(None, 24)

def draw_board(win, board, knight_pos=None):
    font = pygame.font.SysFont(None, 24)
    for row in range(ROWS):
        for col in range(COLS):
             # Determine the color based on whether the cell has been visited
            if board[row][col] != -1:  # If the cell has been visited
                color = GREEN  # Mark visited cells in green
            else:
                color = WHITE if (row + col) % 2 == 0 else GRAY  # Default checkerboard pattern

            # color = WHITE if (row + col) % 2 == 0 else GRAY
            rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(win, color, rect)

            if board[row][col] != -1:
                text = font.render(str(board[row][col]), True, RED)
                text_rect = text.get_rect(center=rect.center)
                win.blit(text, text_rect)

    if knight_pos:
        row, col = knight_pos[1], knight_pos[0]
        top_left = (col * SQUARE_SIZE + 5, row * SQUARE_SIZE + 5)
        win.blit(knight_img, top_left)

    draw_buttons(win)
    pygame.display.update()

def draw_buttons(win):
    mouse_pos = pygame.mouse.get_pos()
    solve_rect = pygame.Rect(SOLVE_BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT)
    solve_color = BUTTON_HOVER_COLOR if solve_rect.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(win, solve_color, solve_rect, border_radius=8)
    solve_text = button_font.render("Solve", True, BUTTON_TEXT_COLOR)
    win.blit(solve_text, solve_text.get_rect(center=solve_rect.center))

    reset_rect = pygame.Rect(RESET_BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT)
    reset_color = (255, 0, 0) if reset_rect.collidepoint(mouse_pos) else (200, 0, 0)
    pygame.draw.rect(win, reset_color, reset_rect, border_radius=8)
    reset_text = button_font.render("Reset", True, BUTTON_TEXT_COLOR)
    win.blit(reset_text, reset_text.get_rect(center=reset_rect.center))



def get_valid_moves(pos, visited):
    if not pos or not isinstance(pos, tuple) or len(pos) != 2:
        return []
    moves = []
    x, y = pos
    for dx, dy in KNIGHT_MOVES:
        nx, ny = x + dx, y + dy
        if 0 <= nx < ROWS and 0 <= ny < COLS and (nx, ny) not in visited:
            moves.append((nx, ny))
    return moves


def display_message(win, message, color=RED):
    font = pygame.font.SysFont("arial", 36, bold=True)
    text = font.render(message, True, color)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    win.blit(text, text_rect)
    pygame.display.update()
    pygame.time.wait(2000)
    
    
def get_algorithm_selection():
    selected_algo = []

    def submit():
        choice = combo.get()
        if choice:
            selected_algo.append(choice)
            top.destroy()

    top = tk.Tk()
    top.title("Select Algorithm")
    top.geometry("300x120")
    tk.Label(top, text="Choose an algorithm:").pack(pady=10)

    from tkinter import ttk
    combo = ttk.Combobox(top, values=["warnsdorff", "backtracking"], state="readonly")
    combo.pack(pady=5)
    combo.set("warnsdorff")  # default selection

    submit_btn = tk.Button(top, text="Submit", command=submit)
    submit_btn.pack(pady=10)

    top.mainloop()

    return selected_algo[0] if selected_algo else None




def solve_knights_tour(win, board, x, y, move_num):
    try:
        if move_num == ROWS * COLS:
            return True

        moves = []
        for dx, dy in KNIGHT_MOVES:
            nx, ny = x + dx, y + dy
            if 0 <= nx < COLS and 0 <= ny < ROWS and board[ny][nx] == -1:
                count = 0
                for ddx, ddy in KNIGHT_MOVES:
                    nnx, nny = nx + ddx, ny + ddy
                    if 0 <= nnx < COLS and 0 <= nny < ROWS and board[nny][nnx] == -1:
                        count += 1
                moves.append(((nx, ny), count))

        moves.sort(key=lambda move: move[1])

        for (nx, ny), _ in moves:
            board[ny][nx] = move_num
            draw_board(win, board, (nx, ny))
            pygame.time.delay(600)

            if solve_knights_tour(win, board, nx, ny, move_num + 1):
                return True

            board[ny][nx] = -1
            draw_board(win, board, (x, y))
            pygame.time.delay(100)

    except Exception as e:
        print(f"Error during solving: {e}")
    return False




def backtracking_knights_tour(board, x, y, move_num):
    if move_num == ROWS * COLS:
        return True

    for dx, dy in KNIGHT_MOVES:
        nx, ny = x + dx, y + dy
        if 0 <= nx < COLS and 0 <= ny < ROWS and board[ny][nx] == -1:
            board[ny][nx] = move_num
            draw_board(win, board, (nx, ny))
            pygame.time.delay(100)

            if backtracking_knights_tour(board, nx, ny, move_num + 1):
                return True

            board[ny][nx] = -1
            draw_board(win, board, (x, y))
            pygame.time.delay(100)

    return False



################ Non-UI version of the solver




def solve_knights_tour_no_ui(board, x, y, move_num):
    try:
        if move_num == ROWS * COLS:
            return True

        moves = []
        for dx, dy in KNIGHT_MOVES:
            nx, ny = x + dx, y + dy
            if 0 <= nx < COLS and 0 <= ny < ROWS and board[ny][nx] == -1:
                count = sum(
                    1 for ddx, ddy in KNIGHT_MOVES
                    if 0 <= nx + ddx < COLS and 0 <= ny + ddy < ROWS and board[ny + ddy][nx + ddx] == -1
                )
                moves.append(((nx, ny), count))

        moves.sort(key=lambda move: move[1])

        for (nx, ny), _ in moves:
            board[ny][nx] = move_num
            if solve_knights_tour_no_ui(board, nx, ny, move_num + 1):
                return True
            board[ny][nx] = -1
    except Exception as e:
        print(f"Error in non-UI solver: {e}")
    return False




# def save_winner_to_db(name, move_count):
#     if not name or not isinstance(name, str) or move_count <= 0:
#         print("Invalid data for database save.")
#         return
#     try:
#         conn = mysql.connector.connect(
#             host='localhost',
#             user='root',
#             password='badagediya',
#             database='knights_tour_game'
#         )
#         cursor = conn.cursor()
#         query = "INSERT INTO winners (name, move_count) VALUES (%s, %s)"
#         cursor.execute(query, (name.strip(), move_count))
#         conn.commit()
#     except mysql.connector.Error as err:
#         print(f"Database Error: {err}")
#     finally:
#         if conn.is_connected():
#             cursor.close()
#             conn.close()




def main():
    visited = []
    knight_pos = None
    running = True
    game_over = False
    
    
    # Ask for player's name at the beginning (compulsory)
    # root = tk.Tk()
    # root.withdraw()
    # player_name = None
    # while not player_name:
    #     player_name = simpledialog.askstring("Welcome!", "Enter your name to start:")
    # root.destroy()
    

    while running:
        board = [[-1 for _ in range(COLS)] for _ in range(ROWS)]
        for i, pos in enumerate(visited):
            board[pos[1]][pos[0]] = i
        draw_board(win, board, knight_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()


                
                # if SOLVE_BUTTON_X <= mx <= SOLVE_BUTTON_X + BUTTON_WIDTH and BUTTON_Y <= my <= BUTTON_Y + BUTTON_HEIGHT:
                #     if knight_pos and not game_over:
                #         # Show dropdown to choose algorithm
                #         try:
                #             root = tk.Tk()
                #             root.withdraw()
                #             algorithm = simpledialog.askstring("Select Algorithm", "Choose algorithm:\n- warnsdorff\n- backtracking")
                #             root.destroy()
                #         except Exception as e:
                #             print(f"Error during algorithm selection: {e}")
                #             algorithm = "warnsdorff"  # default fallback

                #         if algorithm:
                #             algorithm = algorithm.lower()
                #             visited = [knight_pos]
                #             board = [[-1 for _ in range(COLS)] for _ in range(ROWS)]
                #             x, y = knight_pos
                #             board[y][x] = 0

                #             solved = False
                #             if algorithm == "warnsdorff":
                #                 solved = solve_knights_tour(win, board, x, y, 1)
                #             elif algorithm == "backtracking":
                #                 solved = backtracking_knights_tour(board, x, y, 1)

                #             if not solved:
                #                 display_message(win, "No solution found!", RED)
                
                
                
                if SOLVE_BUTTON_X <= mx <= SOLVE_BUTTON_X + BUTTON_WIDTH and BUTTON_Y <= my <= BUTTON_Y + BUTTON_HEIGHT:
                    if not knight_pos:
                        display_message(win, "Place the knight first!", RED)
                        continue

                    if not game_over:
                        # Show dropdown to choose algorithm
                        # try:
                        #     root = tk.Tk()
                        #     root.withdraw()
                        #     algorithm = simpledialog.askstring("Select Algorithm", "Choose algorithm:\n- warnsdorff\n- backtracking")
                        #     root.destroy()
                        # except Exception as e:
                        #     print(f"Error during algorithm selection: {e}")
                        #     algorithm = "warnsdorff"  # default fallback
                        
                        
                        algorithm = get_algorithm_selection()

                        

                        if algorithm:
                            algorithm = algorithm.lower()
                            visited = [knight_pos]
                            board = [[-1 for _ in range(COLS)] for _ in range(ROWS)]
                            x, y = knight_pos
                            board[y][x] = 0

                            solved = False
                            if algorithm == "warnsdorff":
                                solved = solve_knights_tour(win, board, x, y, 1)
                            elif algorithm == "backtracking":
                                solved = backtracking_knights_tour(board, x, y, 1)

                            if not solved:
                                display_message(win, "No solution found!", RED)


                

                if RESET_BUTTON_X <= mx <= RESET_BUTTON_X + BUTTON_WIDTH and BUTTON_Y <= my <= BUTTON_Y + BUTTON_HEIGHT:
                    knight_pos = None
                    visited = []
                    game_over = False
                    continue

                if my <= HEIGHT - BUTTON_HEIGHT - 20 and not game_over:
                    row = my // SQUARE_SIZE
                    col = mx // SQUARE_SIZE
                    clicked_pos = (col, row)

                    if not knight_pos:
                        knight_pos = clicked_pos
                        visited.append(knight_pos)
                    else:
                        valid_moves = get_valid_moves(knight_pos, visited)
                        if clicked_pos in valid_moves:
                            knight_pos = clicked_pos
                            visited.append(knight_pos)

                            if len(get_valid_moves(knight_pos, visited)) == 0 and len(visited) < ROWS * COLS:
                                display_message(win, "No more valid moves. You lost!", RED)
                                # save_winner_to_db(player_name, len(visited))
                                # save_winner_to_db(player_name, len(visited), visited)  # <-- include the path here

                                game_over = True
                        else:
                            display_message(win, "Invalid move!", RED)

        if knight_pos and len(visited) == ROWS * COLS and not game_over:
            display_message(win, "You won!", GREEN)
            try:
                root = tk.Tk()
                root.withdraw()
                player_name = simpledialog.askstring("Victory!", "Enter your name:")
                root.destroy()

                if player_name:
                    # save_winner_to_db(player_name, len(visited))
                    save_winner_to_db(player_name, len(visited), visited)  # <-- include the path here

                # save_winner_to_db(player_name, len(visited))

            except Exception as e:
                print(f"Error collecting player name: {e}")
            game_over = True

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()