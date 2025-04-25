import tkinter as tk
from tkinter import ttk, messagebox

class TSPGameUI:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.root.title("TSP Game")

        # Center and slightly move the TSP Game window upward
        window_width = 600
        window_height = 690

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2) - 18  # Move up by 18px

        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.root.resizable(True, True)
        self.frame = tk.Frame(root, bg="#C3B3E4") 
        label = tk.Label(self.frame, text="Welcome to TSP Game", bg=self.frame["bg"], font=("Helvetica", 18))
        label.pack(pady=20)    
        self.frame.pack(fill="both", expand=True)
        

    def clear(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def show_welcome_screen(self):
        self.clear()
        
        tk.Label(self.frame, text="Travelling Salesman Game!", font=("Helvetica", 24, "bold"),bg=self.frame["bg"]).pack(pady=30)
        tk.Label(self.frame, text="Enter your name:", font=("Helvetica", 14),bg=self.frame["bg"]).pack(pady=10)
        name_entry = tk.Entry(self.frame, font=("Helvetica", 14),  bd=2, relief="groove", highlightthickness=1, highlightbackground="#ccc" )
        name_entry.pack(pady=10, ipady=1, ipadx=1)
        tk.Button(self.frame, text="OK", font=("Helvetica", 12), activebackground="#C3B3E4", padx=50,pady=1,  bg="#6A5ACD",
                         command=lambda: self.app.set_player(name_entry.get())).pack(pady=10)  
                       
                        
                          
                       
               

    def show_main_menu(self):
        self.clear()
        tk.Label(self.frame, text=f"Welcome, {self.app.player}!", font=("Helvetica", 20),bg=self.frame["bg"]).pack(pady=20)
        tk.Button(self.frame, text="🎮 Start Game", font=("Helvetica", 14), width=20,
                  command=self.app.on_start_game).pack(pady=10)
        tk.Button(self.frame, text="❌ Exit Game", font=("Helvetica", 14), width=20,
              command=self.app.exit_game).pack(pady=10)
      

    def show_city_selection(self, home, city_list):
        self.clear()
        tk.Label(self.frame, text=f"🏠 Home City: {home}", font=("Helvetica", 16, "bold"), bg=self.frame["bg"]).pack(pady=10)
        tk.Label(self.frame, text="Select cities to visit:", font=("Helvetica", 14), bg=self.frame["bg"]).pack()

        selected_vars = {}
        checkbox_frame = tk.Frame(self.frame, bg=self.frame["bg"])
        checkbox_frame.pack(pady=20)

        # Configurable values
        checkboxes_per_row = 3
        row = 0
        col = 0

        for idx, city in enumerate(city_list):
            var = tk.BooleanVar()
            chk = tk.Checkbutton(
                checkbox_frame,
                text=f"City {city}",
                variable=var,
                font=("Helvetica", 14),  # bigger font
                bg=self.frame["bg"],
                padx=10,
                pady=5
            )
            # Zig-zag alignment: even row left, odd row right
            anchor = "w" if row % 2 == 0 else "e"
            chk.grid(row=row, column=col, sticky=anchor, padx=20, pady=10)
            selected_vars[city] = var

            col += 1
            if col >= checkboxes_per_row:
                col = 0
                row += 1

        tk.Button(
            self.frame,
            text="Submit",
            font=("Helvetica", 13, "bold"),
            activebackground="#C3B3E4",
            padx=50,
            pady=5,
            bg="#6A5ACD",
            fg="white",
            command=lambda: self.app.on_city_selected([c for c in selected_vars if selected_vars[c].get()])
        ).pack(pady=20)


    def show_distance_matrix(self, matrix, home, cities, callback):
        self.clear()
        tk.Label(self.frame, text="🗺️ Distance Travelled", font=("Helvetica", 16),bg=self.frame["bg"]).pack(pady=10)

        style = ttk.Style()
        style.configure("Bold.Treeview.Heading", font=("Helvetica", 10, "bold"),foreground="#6A0DAD")
        style.configure("Bold.Treeview", font=("Helvetica", 10), rowheight=25, borderwidth=1, relief="solid") 

        style.layout("Bold.Treeview", [
            ('Treeview.field', {'sticky': 'nswe', 'border': '1', 'children': [
                ('Treeview.padding', {'sticky': 'nswe', 'children': [
                    ('Treeview.treearea', {'sticky': 'nswe'})
                ]})
            ]})
        ])

        tree = ttk.Treeview(self.frame,style="Bold.Treeview")
        city_list = list(matrix.keys())
        tree["columns"] = city_list
        tree.column("#0", width=80, anchor="w")
        tree.heading("#0", text="From/To", anchor="w")

        for city in city_list:
            tree.column(city, width=70, anchor="center")
            tree.heading(city, text=city, anchor="center")

        for city in city_list:
            values = [matrix[city][dest] for dest in city_list]
            tree.insert("", "end", text=city, values=values)

        tree.tag_configure("purple_bold", foreground="#6A0DAD", font=("Helvetica", 10, "bold"))

        for child in tree.get_children():
            tree.item(child, tags=("purple_bold",))

        tree.pack(pady=10)
        self.show_route_input(matrix, home, cities, callback)

    def show_route_input(self, matrix, home, cities, callback):
        tk.Label(self.frame, text=f"🔔 Your home city is: {home}", font=("Arial", 14), fg="#322b59",bg=self.frame["bg"]).pack(pady=10)
        tk.Label(self.frame, text="Click on cities to select your travel path.", font=("Arial", 12),bg=self.frame["bg"]).pack()

        route = [home]
        route_var = tk.StringVar()
        route_var.set(" -> ".join(route))

        def add_city(city):
            if city not in route:
                route.append(city)
                route_var.set(" -> ".join(route))

        def submit_route():
            if route[-1] != home:
                route.append(home)
            callback(route)

        frame = tk.Frame(self.frame,bg=self.frame["bg"])
        frame.pack(pady=10)

        for city in cities:
            btn = tk.Button(frame, text=city, width=10,bg="#f7b66a", command=lambda c=city: add_city(c))
            btn.pack(side=tk.LEFT, padx=10)

        tk.Label(self.frame, textvariable=route_var, font=("Arial", 12,"bold"), fg="#6A0DAD",bg=self.frame["bg"]).pack(pady=10)
        tk.Button(self.frame, text="✅ Submit Route", command=submit_route,font=("Helvetica", 13, "bold"),activebackground="#C3B3E4",padx=50,pady=5,
            bg="#6A5ACD",fg="white",).pack(pady=10)

    def show_result_screen(self, user_route, user_cost, correct,
                           bf, greedy, dp, play_again_callback, quit_callback):
        self.clear()
        title = "✅ Correct!" if correct else "❌ Incorrect"
        tk.Label(self.frame, text=title, font=("Helvetica", 20, "bold"), bg=self.frame["bg"]).pack(pady=10)

        # Player's route
        tk.Label(self.frame, text=f"🧍 Your Route: {' -> '.join(user_route)}", font=("Arial", 12), bg=self.frame["bg"]).pack(pady=5)
        tk.Label(self.frame, text=f"🛣️ Your Distance: {user_cost} km", font=("Arial", 12), bg=self.frame["bg"]).pack(pady=5)

        # Algorithm results
        def algo_result(label, data):
            route, cost, time = data
            tk.Label(self.frame, text=f"🔍 {label}:", font=("Arial", 13, "bold"), bg=self.frame["bg"]).pack(pady=5)
            tk.Label(self.frame, text=f"Route: {' -> '.join(route)}", font=("Arial", 11), bg=self.frame["bg"]).pack()
            tk.Label(self.frame, text=f"Distance: {cost} km | Time: {time} ms", font=("Arial", 11), bg=self.frame["bg"]).pack()

        algo_result("Brute Force", bf)
        algo_result("Greedy", greedy)
        algo_result("Dynamic Programming", dp)


      
        tk.Label(self.frame, text="🎮 Round Complete!", font=("Helvetica", 20), bg=self.frame["bg"]).pack(pady=30)
        # Buttons
        tk.Button(self.frame, text="🔁 Play Again", font=("Helvetica", 13), width=20,
                  bg="#6A5ACD", fg="white", command=play_again_callback).pack(pady=10)

        tk.Button(self.frame, text="❌ Quit", font=("Helvetica", 13), width=20,
                  bg="#D9534F", fg="white", command=quit_callback).pack(pady=5)
        

   
