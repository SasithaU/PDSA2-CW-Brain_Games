# ui/main_menu.py
import tkinter as tk
from ui.message_ui import show_error
from PIL import Image, ImageTk
from ui.game_ui import ChessGame

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Eight Queens Puzzle")

        try:
            # Match the ChessGame window size (600x600 for 75px tiles and board + controls)
            window_width = 600
            window_height = 670

            # Set up the background image
            bg_image = Image.open("eightQueens\images\chessboard.jpg")  # Replace with your image path
            bg_image = bg_image.resize((window_width, window_height), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(bg_image)

            bg_label = tk.Label(self.root, image=self.bg_photo)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        except FileNotFoundError:
            show_error("Error", "Background image file not found. Please check the path.")
            self.root.quit()
            return
        except Exception as e:
            show_error("Error", f"An unexpected error occurred while loading the background image: {e}")
            self.root.quit()
            return

        try:
            # Get screen width and height
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()

            # Calculate x and y to center the window
            x = (screen_width // 2) - (window_width // 2)
            y = (screen_height // 2) - (window_height // 2) - 15 

            self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
            self.root.resizable(False, False)

            # Create a central frame to hold the buttons vertically
            center_frame = tk.Frame(root, bg="#f5f0e1", width=350, height=250)
            center_frame.place(relx=0.5, rely=0.42, anchor=tk.CENTER)
            center_frame.pack_propagate(False)

            # Title Label
            title_label = tk.Label(center_frame, text="Eight Queens Puzzle", font=("Old English Text MT", 24), bg="#f5f0e1")
            title_label.pack(pady=(0, 30))  # Less padding below title

            # Start Button
            start_button = tk.Button(center_frame, text="Start", width=20, font=("Times New Roman", 14, "bold"), command=self.start_game, bg="#808000", fg="white", activebackground="#666600", activeforeground="white")
            start_button.pack(pady=10)

            # Rules Button
            rules_button = tk.Button(center_frame, text="Rules", width=20, font=("Times New Roman", 14, "bold"), command=self.show_rules, bg="#8B5E3C", fg="white", activebackground="#6E4A2F", activeforeground="white")
            rules_button.pack(pady=10)

            # Exit Button
            exit_button = tk.Button(center_frame, text="Exit", width=20, font=("Times New Roman", 14, "bold"), command=root.quit, bg="#800000", fg="white", activebackground="#660000", activeforeground="white")
            exit_button.pack(pady=10)

        except Exception as e:
            show_error("Error", f"An unexpected error occurred during UI setup: {e}")
            self.root.quit()

    def start_game(self):
        try:
            self.root.withdraw()  # Hide main menu
            game_window = tk.Toplevel(self.root)
            ChessGame(game_window, main_root=self.root)

        except Exception as e:
            show_error("Error", f"An error occurred while starting the game: {e}")

    def show_rules(self):
        try:
            rules_window = tk.Toplevel(self.root)
            rules_window.title("Game Rules")
            rules_window.configure(bg="#f5f0e1")

            # Set the same size and center it like the main window
            window_width = 490
            window_height = 300
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            x = (screen_width // 2) - (window_width // 2)
            y = (screen_height // 2) - (window_height // 2) - 15

            rules_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
            rules_window.resizable(False, False)

            rules_text = (
                "🧩 Welcome to the Eight Queens Puzzle! 🎩\n\n"
                "This is a chess challenge where you need to think carefully.\n"
                "Your goal is to place 8 queens on a chessboard so that:—\n"
                "No two queens can attack each other.\n"
                "That means:\n"
                "No two queens in the same row.\n"
                "No two queens in the same column.\n"
                "No two queens in the same diagonal.👑\n\n"
                "Can you beat the board and win?\n\n"
                "Good luck, Player!"
            )
            rules_label = tk.Message(rules_window, text=rules_text, font=("Times New Roman", 12), bg="#f5f0e1", width=500)
            rules_label.pack(padx=20, pady=20)

            close_button = tk.Button(rules_window, text="Close", command=rules_window.destroy, font=("Times New Roman", 12, "bold"), bg="#8B5E3C", fg="white")
            close_button.pack(pady=(0, 20))

        except Exception as e:
            show_error("Error", f"An error occurred while displaying the rules: {e}")

def run_main_menu():
    try:
        root = tk.Tk()
        MainMenu(root)
        root.mainloop()

    except Exception as e:
        show_error("Error", f"An error occurred while running the main menu: {e}")
