import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import random

# Visual Constants
peg_color = "gray"
disk_colors = [
    "lightblue", "lightcoral", "lightgreen", "lightsalmon", "lightskyblue",
    "lightgoldenrodyellow", "lightpink", "lightseagreen", "lightcyan", "lavender"
]
peg_width = 20
disk_height = 10
base_width = 150  # Reduced base width for better separation
base_height = 30
offset_x_start = 100  # Starting x-offset for the first peg
offset_x =50
offset_y = 10
peg_spacing = 200  # Increased spacing between pegs
canvas_width = 700  # Increased canvas width
canvas_height = 400

# Create Home Page 
def home_page():
    home = tk.Tk()
    home.title("Play Tower of Hanoi")
    home.geometry("600x400")
    home.configure(bg="#A9A9A9")

    def start_game():
        home.destroy()  # Ends the mainloop, continuing to main()

    def show_rules_local():
        show_rules()  # Avoids scope conflict

    tk.Label(
        home, text="Tower of Hanoi", font=("Algerian", 28, "bold"),
        fg="#333", bg="#A9A9A9"
    ).pack(pady=40)

    tk.Button(
        home, text="Start Game", font=("Helvetica", 16), bg="#4caf50",
        fg="white", padx=20, pady=10, relief="raised", command=start_game
    ).pack(pady=30)

    tk.Button(
        home, text="Game Rules", font=("Helvetica", 12),
        bg="#2196f3", fg="white", padx=15, pady=5, command=show_rules_local
    ).pack()

    home.mainloop()  # Keeps the home window running


    # Peg Functions
def draw_peg(canvas, x, y, height):
    canvas.create_rectangle(x - peg_width // 2, y - height, x + peg_width // 2, y, fill=peg_color)
    canvas.create_rectangle(x - base_width // 2, y, x + base_width // 2, y + base_height, fill=peg_color)

def draw_disk(canvas, peg_x, y, width, color, tag):
    disk_id = canvas.create_rectangle(
        peg_x - width // 2, y,
        peg_x + width // 2, y + disk_height,
        fill=color, outline="black", width=1, tags=tag
    )
    return disk_id

def draw_initial_state(canvas, num_of_disks):
    canvas.delete("all")
    y_start = 350 - base_height - disk_height // 2
    canvas.disks = []  # Store disk IDs for drag logic
    canvas.peg_locations = {
        "A": offset_x_start,
        "B": offset_x_start + peg_spacing,
        "C": offset_x_start + 2 * peg_spacing
    }
    canvas.stacks = {"A": [], "B": [], "C": []} # Keep track of disks on each peg

    # Draw pegs
    draw_peg(canvas, canvas.peg_locations["A"], 350, 150 + base_height // 2)  # Peg A
    draw_peg(canvas, canvas.peg_locations["B"], 350, 150 + base_height // 2)  # Peg B
    draw_peg(canvas, canvas.peg_locations["C"], 350, 150 + base_height // 2)  # Peg C

    for i in range(num_of_disks):
        width = 40 + (num_of_disks - 1 - i) * 15  # Slightly reduced disk width increment
        color = disk_colors[i % len(disk_colors)]
        tag = f"disk_{i}"
        y = y_start - i * disk_height
        disk_id = draw_disk(canvas, canvas.peg_locations["A"], y, width, color, tag)
        canvas.disks.append(disk_id)
        canvas.stacks["A"].append(disk_id)

    # Add drag-and-drop
    setup_drag_and_drop(canvas)

    # Add drag-and-drop
    setup_drag_and_drop(canvas)


def setup_drag_and_drop(canvas):
    canvas.drag_data = {"item": None, "x": 0, "y": 0}

    def on_disk_press(event):
        item = canvas.find_closest(event.x, event.y)[0]
        if item in canvas.disks:
            canvas.drag_data["item"] = item
            canvas.drag_data["x"] = event.x
            canvas.drag_data["y"] = event.y

    def on_disk_motion(event):
        item = canvas.drag_data["item"]
        if item:
            dx = event.x - canvas.drag_data["x"]
            dy = event.y - canvas.drag_data["y"]
            canvas.move(item, dx, dy)
            canvas.drag_data["x"] = event.x
            canvas.drag_data["y"] = event.y

    def on_disk_release(event):
        canvas.drag_data["item"] = None

    canvas.bind("<ButtonPress-1>", on_disk_press)
    canvas.bind("<B1-Motion>", on_disk_motion)
    canvas.bind("<ButtonRelease-1>", on_disk_release)

# Game Functions     
def show_rules():
    rules_text = (
        "Game Rules:\n\n"
        "1. Only one disk can be moved at a time.\n"
        "2. A larger disk cannot be placed on a smaller disk.\n"
        "3. You can use the auxiliary peg to help move the disks."
    )
    messagebox.showinfo("Tower of Hanoi Rules", rules_text)
def get_user_input(num_of_disks):
    root = tk.Tk()
    root.title("Tower of Hanoi Game")

    canvas = tk.Canvas(root, width=600, height=400, bg="white")
    canvas.pack(pady=10)
    draw_initial_state(canvas, num_of_disks)

        # Draw labels A, B, C under each peg
    canvas.create_text(offset_x, 370, text="A", font=("Helvetica", 14, "bold"))
    canvas.create_text(offset_x + peg_spacing, 370, text="B", font=("Helvetica", 14, "bold"))
    canvas.create_text(offset_x + 2 * peg_spacing, 370, text="C", font=("Helvetica", 14, "bold"))

    algorithm_var = tk.StringVar(root, "recursive")
    moves_entry_var = tk.StringVar(root)
    name_entry_var = tk.StringVar(root)
    result = {"algorithm": None, "moves": None, "submitted": False}

    ttk.Label(root, text=f"Move {num_of_disks} disks from A to C").pack(pady=5)

    algo_frame = ttk.Frame(root)
    algo_frame.pack(pady=5)
    ttk.Label(algo_frame, text="Select Algorithm:").pack(side=tk.LEFT)
    algo_combo = ttk.Combobox(algo_frame, textvariable=algorithm_var, values=["recursive", "iterative"], state="readonly")
    algo_combo.pack(side=tk.LEFT)

    ttk.Label(root, text="Enter Your Name:").pack(pady=5)
    name_entry = ttk.Entry(root, textvariable=name_entry_var, width=40)
    name_entry.pack(pady=5)

    ttk.Label(root, text="Enter moves (e.g., A->C, B->A, ...):").pack(pady=5)
    moves_entry = ttk.Entry(root, textvariable=moves_entry_var, width=60)
    moves_entry.pack(pady=5)

    rules_button = ttk.Button(root, text="Game Rules", command=show_rules)
    rules_button.pack(pady=5)

    def submit_input():
        result["algorithm"] = algorithm_var.get()
        result["moves"] = moves_entry_var.get()
        result["submitted"] = True
        root.destroy()

    submit_button = ttk.Button(root, text="Submit", command=submit_input)
    submit_button.pack(pady=10)

    root.mainloop()
    return result["algorithm"], result["moves"]

def parse_user_moves(moves_str):
    moves_list = []
    if moves_str:
        for move_str in moves_str.split(','):
            move = move_str.strip().replace('->', '').upper()
            if len(move) == 2 and all(peg in ['A', 'B', 'C'] for peg in move) and move[0] != move[1]:
                moves_list.append((move[0], move[1]))
            elif move_str.strip():
                messagebox.showerror("Input Error", f"Invalid move format: {move_str}")
                return []
    return moves_list

def display_result(is_correct, correct_moves):
    if is_correct:
        messagebox.showinfo("Result", "Correct sequence of moves!")
    else:
        messagebox.showerror("Result", f"Incorrect. Expected: {', '.join([f'{m[0]}->{m[1]}' for m in correct_moves])}")

def get_player_name():
    return simpledialog.askstring("Save Score", "Enter your name:")

def play_again():
    return messagebox.askyesno("Play Again", "Do you want to play another round?")

# Main Program Entry
if __name__ == '__main__':
    home_page()
    n = random.randint(5, 10)
    algorithm, moves_str = get_user_input(n)
    print(f"Selected Algorithm: {algorithm}")
    print(f"Entered Moves: {moves_str}")
    moves_list = parse_user_moves(moves_str)
    print(f"Parsed Moves: {moves_list}")


