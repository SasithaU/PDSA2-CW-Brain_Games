# ui/game_ui.py
import tkinter as tk
from tkinter import ttk
from ui.message_ui import show_error
from src.validation.validator import *
from utils.save_sequential import save_sequential_results
from utils.save_threaded import save_threaded_results
from ui.message_ui import show_info
import time


class ChessGame:
    def __init__(self, root, main_root=None):
        
        self.root = root
        self.start_time = None
        self.main_root = main_root

        self.root.title("Eight Queens Puzzle")
        self.root.configure(bg="#F4E1D2") 

        self.tile_size = 75
        canvas_size = self.tile_size * 8
        self.queens = set()
        self.name_var = tk.StringVar()

        # Center the window on the screen
        window_width = self.tile_size * 8 + 85
        window_height = self.tile_size * 8 + 85

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)-18

        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # === Top bar with Back on left and controls in center ===
        top_bar = tk.Frame(root,bg="#F4E1D2")
        top_bar.pack(fill=tk.X, pady=10, padx=10)

        button_width = 5
        button_height = 1

        # Back Button on the far left
        tk.Button(top_bar, text="Back", command=self.go_back, bg="#4169E1", fg="white",width=button_width,height=button_height,activebackground="#314db3", activeforeground="white",font=("Arial", 10, "bold")).pack(side=tk.LEFT,padx=(0, 5))

        # Reset button (clears board only)
        self.reset_button = tk.Button(top_bar, text="Reset", command=self.reset_board,bg="#FF8C00", fg="white",width=button_width, height=button_height, font=("Arial", 10, "bold"),activebackground="#cc7000", activeforeground="white")
        self.reset_button.pack(side=tk.LEFT, padx=(0, 30))

        # Replay button
        self.replay_button = tk.Button(top_bar, text="Replay", command=self.replay_game,bg="#8B0000", fg="white", width=button_width, height=button_height, font=("Arial", 10, "bold"),activebackground="#a30000", activeforeground="white")
        self.replay_button.pack(side=tk.TOP, pady=10) 
        self.replay_button.pack_forget()  # Hide initially

        # Dropdown menu for mode selection
        self.mode_var = tk.StringVar(value="Select Mode")
        self.mode_dropdown = ttk.Combobox(top_bar, textvariable=self.mode_var, state="readonly", width=15,values=["Select Mode", "Sequential", "Threaded"])
        self.mode_dropdown.pack(side=tk.LEFT, padx=(0, 20))
        self.mode_dropdown.bind("<<ComboboxSelected>>", self.on_mode_selected)
        
        # Center frame for the other controls
        center_frame = tk.Frame(top_bar,bg="#F4E1D2")
        center_frame.pack(side=tk.TOP)

        # Controls in the center
        tk.Label(center_frame, text="Player Name:", bg="#F4E1D2",font=("Times New Roman", 11,"bold"),).pack(side=tk.LEFT, padx=5)
        tk.Entry(center_frame, textvariable=self.name_var, width=15, font=("Times New Roman", 12)).pack(side=tk.LEFT)
        tk.Button(center_frame, text="Submit", command=self.submit_solution, bg="#006400", fg="white",width=button_width, height=button_height,activebackground="#004d00", activeforeground="white",font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=10)

        # Label to show number of queens remaining
        self.queens_remaining_label = tk.Label(center_frame,text=f"♕", bg="#F4E1D2", font=("Arial", 24, "bold"))
        self.queens_remaining_label.pack(side=tk.LEFT)

        # Label to show number of queens remaining (number next to ♕)
        self.queens_number_label = tk.Label(center_frame, text=f"{8 - len(self.queens)}", bg="#F4E1D2", font=("Times New Roman", 14, "bold"))
        self.queens_number_label.pack(side=tk.LEFT, padx=(2, 0))

        # Canvas
        self.canvas = tk.Canvas(root, width=canvas_size, height=canvas_size)
        self.canvas.pack(pady=10)

        self.draw_board()
        self.canvas.bind("<Button-1>", self.place_queen)

    def draw_board(self):
        self.canvas.delete("all")
        tile_size = self.tile_size
        for row in range(8):
            for col in range(8):
                color = "white" if (row + col) % 2 == 0 else "black"
                self.canvas.create_rectangle(
                    col * tile_size, row * tile_size,
                    (col + 1) * tile_size, (row + 1) * tile_size,
                    fill=color
                )
        for (r, c) in self.queens:
           self.canvas.create_text(
                c * tile_size + tile_size // 2,
                r * tile_size + tile_size // 2,
                text="♕",
                font=("Arial", 40),
                fill="#B8860B"
            )

    def place_queen(self, event):
        try:
            row, col = event.y // self.tile_size, event.x // self.tile_size
            if (row, col) in self.queens:
                self.queens.remove((row, col))
            else:
                if not validate_queen_limit(self.queens):
                    self.update_queens_remaining()
                    return 
                self.queens.add((row, col))
                
            if self.start_time is None:  
                self.start_time = time.time()

            self.draw_board()
            self.update_queens_remaining()
        except Exception as e:
            show_error("Error", f"An error occurred while placing the queen:\n{e}")

    def submit_solution(self):
        try:
            name = self.name_var.get().strip()

            if not validate_submission(self.queens, name):
                return

            positions = [-1] * 8
            for (r, c) in self.queens:
                positions[r] = c

            validate_and_save(name, tuple(positions), self.start_time)
            self.replay_button.pack()
            self.canvas.unbind("<Button-1>") 
        except Exception as e:
            show_error("Submission Error", f"Failed to submit solution:\n{e}")

    def on_mode_selected(self, event):
        selected_mode = self.mode_var.get()
        try:
            if selected_mode == "Sequential":
                duration = save_sequential_results()
                show_info("Sequential Results", f"Sequential Program - 92 solutions found in {duration:.2f} ms.")
            elif selected_mode == "Threaded":
                duration = save_threaded_results()
                show_info("Threaded Results", f"Threaded Program - 92 solutions found in {duration:.2f} ms.")
        except Exception as e:
            show_error("Execution Error", f"An error occurred while running the {selected_mode.lower()} algorithm:\n{e}")

    def replay_game(self):
        self.queens.clear()
        self.draw_board()
        self.name_var.set("")
        self.update_queens_remaining()
        self.canvas.bind("<Button-1>", self.place_queen) 
        self.replay_button.pack_forget()  

    def reset_board(self):
        self.queens.clear()
        self.draw_board()
        self.update_queens_remaining()

    def go_back(self):
        self.root.destroy()
        if self.main_root:
            self.main_root.deiconify()

    def on_close(self):
        self.root.destroy()
        if self.main_root:
            self.main_root.destroy()

    def update_queens_remaining(self):
        queens_left = 8 - len(self.queens)
        if queens_left <= 1:
            self.queens_remaining_label.config(fg="red")
            self.queens_number_label.config(fg="red") 
        else:
            self.queens_remaining_label.config(fg="black")
            self.queens_number_label.config(fg="black")
        self.queens_number_label.config(text=f"{queens_left}")