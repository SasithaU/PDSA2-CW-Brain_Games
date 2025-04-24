# ui/message_ui.py

import tkinter as tk

class MessageWindow:
    def __init__(self, title, message, message_type="info"):
        self.root = tk.Toplevel()
        self.root.overrideredirect(True)  # Remove default window decorations
        self.root.resizable(False, False)

        # Calculate dynamic width based on message length
        message_length = len(message)
        width = max(370, message_length * 10 + 50)  
        height = 150
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

        # Icon and Color Configurations
        icon_map = {
            "info":    ("ℹ️", "dodgerblue", "#4a90e2"),
            "success": ("✅", "green", "#808000"),
            "warning": ("⚠️", "orange", "#dea03c"),
            "error":   ("❌", "red", "#b22222")  
        }

        icon, icon_color, accent_color = icon_map.get(message_type, ("ℹ️", "dodgerblue", "#4a90e2"))
        background_color = "#f5f0e1"

        # Outer Frame with Accent Border
        outer_frame = tk.Frame(self.root, bg=accent_color, bd=2)
        outer_frame.pack(fill="both", expand=True)

        # Custom Title Bar
        title_bar = tk.Frame(outer_frame, bg=accent_color, relief="flat", height=24)
        title_bar.pack(fill="x")
        title_label = tk.Label(title_bar, text=title, bg=accent_color, fg="white", font=("Times New Roman", 10, "bold"))
        title_label.pack(side="left", padx=10)

        close_btn = tk.Button(title_bar, text="✕", bg=accent_color, fg="white", borderwidth=0,
                              command=self.root.destroy, font=("Arial", 10, "bold"))
        close_btn.pack(side="right", padx=8)

        # Title Bar Dragging
        def start_move(event):
            self.x = event.x
            self.y = event.y

        def on_motion(event):
            deltax = event.x - self.x
            deltay = event.y - self.y
            new_x = self.root.winfo_x() + deltax
            new_y = self.root.winfo_y() + deltay
            self.root.geometry(f"+{new_x}+{new_y}")

        title_bar.bind("<Button-1>", start_move)
        title_bar.bind("<B1-Motion>", on_motion)

        # Main Content Frame
        content_frame = tk.Frame(outer_frame, bg=background_color)
        content_frame.pack(fill="both", expand=True)

        icon_label = tk.Label(content_frame, text=icon, font=("Times New Roman", 22), fg=icon_color, bg=background_color)
        icon_label.grid(row=0, column=0, padx=(20, 10), pady=(30, 10))

        msg_label = tk.Label(content_frame, text=message, font=("Times New Roman", 12, "bold"),
                             bg=background_color, fg="black")
        msg_label.grid(row=0, column=1, sticky="w", pady=(30, 10))

        # Center the OK button horizontally without covering the entire width
        ok_button = tk.Button(content_frame, text="OK", font=("Times New Roman", 12, "bold"),
                              bg="#8B5E3C", fg="#f5f0e1", command=self.root.destroy)

        ok_button.grid(row=1, column=0, columnspan=2, pady=(0, 15), padx=10)

        # Adjust the row and column weights to ensure the button is centered without spanning the entire width
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)

    def get_window(self):
        return self.root       

# Test functions
def show_error(title, message):
    MessageWindow(title, message, message_type="error").get_window()

def show_warning(title, message):
    MessageWindow(title, message, message_type="warning").get_window()

def show_success(title, message):
    win = MessageWindow(title, message, message_type="success").get_window()
    return win

def show_info(title, message):
    MessageWindow(title, message, message_type="info").get_window()
