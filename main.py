import tkinter as tk
from PIL import Image, ImageTk
import subprocess
import os

class BrainGamesMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Brain Games")

        window_width = 600
        window_height = 670

        try:
            bg_image = Image.open("assets\mainUI.png")  
            bg_image = bg_image.resize((window_width, window_height), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            bg_label = tk.Label(self.root, image=self.bg_photo)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except:
            self.root.configure(bg="#f7f7eb")  # Fallback background

        # Centering the window
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2) - 20
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.resizable(False, False)

        # Frame for buttons
        center_frame = tk.Frame(root, bg="#f7f7eb", width=300, height=400)
        center_frame.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
        center_frame.pack_propagate(False)

        # Title
        # title_label = tk.Label(center_frame, text=" Brain Games", font=("Old English Text MT", 24), bg="#f7f7eb")
        # title_label.pack(pady=(10, 30))

        # Buttons for games
        self.create_game_button(center_frame, "Tic Tac Toe", "tic_tac_toe_game/main.py", "#39bda9")
        self.create_game_button(center_frame, "Tower of Hanoi", "TowerOfHanoi/main.py", "#b3d138")
        self.create_game_button(center_frame, "8 Queens", "eightQueens/main.py", "#e6653d")
        self.create_game_button(center_frame, "Traveling Salesman", "tsp_game/main.py", "#bd45b1")
        self.create_game_button(center_frame, "Knight's Tour", "knight's tour/knights_tour.py", "#6098c6")

        # Exit button
        exit_button = tk.Button(center_frame, text="Exit", width=20,height=1, font=("Fixedsys", 14, "bold"),
                                command=self.root.quit, bg="#c61e1e", fg="white",
                                activebackground="#660000", activeforeground="white",padx=4,pady=6)
        exit_button.pack(pady=(40, 0))

    def create_game_button(self, parent, label, script_path, bg_color):
        button = tk.Button(parent, text=label, width=20, height=1, font=("Fixedsys", 14, "bold"),
                           bg=bg_color, fg="white", activebackground="black", activeforeground="white",padx=4,pady=6,
                           command=lambda: self.show_loading_screen(script_path))
        button.pack(pady=10)

    def show_loading_screen(self, path):
        # Show a small loading window
        loading_window = tk.Toplevel(self.root)
        loading_window.title("Loading...")
        loading_window.geometry("300x100")
        loading_window.configure(bg="#f5f0e1")
        loading_window.resizable(False, False)

        # Center the loading window
        screen_width = loading_window.winfo_screenwidth()
        screen_height = loading_window.winfo_screenheight()
        x = (screen_width // 2) - (300 // 2)
        y = (screen_height // 2) - (100 // 2) - 60
        loading_window.geometry(f"+{x}+{y}")

        # Label for loading
        loading_label = tk.Label(loading_window, text="Loading, please wait...", font=("Fixedsys", 12), bg="#f5f0e1")
        loading_label.pack(expand=True)

        # Force UI update
        self.root.update()
        loading_window.update()

        # Wait a short moment and launch the game
        self.root.after(500, lambda: self.run_game(path, loading_window))

    def run_game(self, path, loading_window):
        loading_window.destroy()
        self.root.destroy()
        subprocess.call(["python", path])  # Wait for the game to finish
        run_brain_games_menu()  # Relaunch the main menu


def run_brain_games_menu():
    root = tk.Tk()
    BrainGamesMenu(root)
    root.mainloop()

if __name__ == "__main__":
    run_brain_games_menu()
