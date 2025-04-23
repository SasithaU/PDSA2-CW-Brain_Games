import tkinter as tk
from tkinter import ttk, messagebox

class TSPGameUI:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.root.title("TSP Game")
        self.root.geometry("800x600")
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
        tk.Label(self.frame, text="Traveling Salesman Problem!", font=("Helvetica", 24, "bold"),bg=self.frame["bg"]).pack(pady=30)
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
        tk.Button(self.frame, text="📊 Leaderboard", font=("Helvetica", 14), width=20,
                  command=self.app.show_leaderboard).pack(pady=10)
        tk.Button(self.frame, text="❌ Quit Game", font=("Helvetica", 14), width=20,
                  command=self.root.quit).pack(pady=10)

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
        tk.Label(self.frame, text="🗺️ Distance Matrix", font=("Helvetica", 16),bg=self.frame["bg"]).pack(pady=10)

        tree = ttk.Treeview(self.frame)
        city_list = list(matrix.keys())
        tree["columns"] = city_list
        tree.column("#0", width=80, anchor="w")
        tree.heading("#0", text="From/To")

        for city in city_list:
            tree.column(city, width=70, anchor="center")
            tree.heading(city, text=city)

        for city in city_list:
            values = [matrix[city][dest] for dest in city_list]
            tree.insert("", "end", text=city, values=values)

        tree.pack(pady=10)
        self.show_route_input(matrix, home, cities, callback)

    def show_route_input(self, matrix, home, cities, callback):
        tk.Label(self.frame, text=f"🔔 Your home city is: {home}", font=("Arial", 14), fg="blue",bg=self.frame["bg"]).pack(pady=10)
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

        frame = tk.Frame(self.frame)
        frame.pack(pady=10)

        for city in cities:
            btn = tk.Button(frame, text=city, width=10, command=lambda c=city: add_city(c))
            btn.pack(side=tk.LEFT, padx=10)

        tk.Label(self.frame, textvariable=route_var, font=("Arial", 12), fg="green",bg=self.frame["bg"]).pack(pady=10)
        tk.Button(self.frame, text="✅ Submit Route", command=submit_route,font=("Helvetica", 13, "bold"),activebackground="#C3B3E4",padx=50,pady=5,
            bg="#6A5ACD",fg="white",).pack(pady=10)

    def show_algorithm_choice(self):
        self.clear()
        tk.Label(self.frame, text="🧠 Choose Algorithm", font=("Helvetica", 16),bg=self.frame["bg"]).pack(pady=20)
        for val, name in [("1", "Brute Force"), ("2", "Greedy"), ("3", "Dynamic Programming")]:
            tk.Button(self.frame, text=name, font=("Helvetica", 14), width=25,
                      command=lambda v=val: self.app.on_algorithm_chosen(v)).pack(pady=5)

    def show_result_screen(self, correct_route, correct_distance, time_taken, user_route, is_correct):
        self.clear()
        result_text = (
            f"✅ Correct Route: {' → '.join(correct_route)}\n"
            f"🧭 Distance: {correct_distance} km\n"
            f"⏱️ Time: {time_taken:.2f} milliseconds\n"
            f"📌 Your Route: {' → '.join(user_route)}\n"
            f"{'🎉 Correct! You found the shortest path!' if is_correct else '❌ Not the shortest path.'}"
        )
        tk.Label(self.frame, text=result_text, font=("Helvetica", 12),bg="#FFEF73", justify="left").pack(pady=20)
        tk.Button(self.frame, text="🔁 Play Again", font=("Helvetica", 13, "bold"),activebackground="#C3B3E4",padx=50,pady=5,
            bg="#6A5ACD",fg="white", command=self.app.play_again).pack(pady=5)
        tk.Button(self.frame, text="❌ Quit", font=("Helvetica", 13, "bold"),activebackground="#C3B3E4",padx=50,pady=5,
            bg="#FF0303",fg="white", command=self.app.end_game).pack(pady=5)

    def show_final_score(self, player, score, rounds):
        self.clear()
        summary = f"🏁 Game Over {player}!\n⭐ Rounds Played: {rounds}\n🏆 Total Score: {score}"
        tk.Label(self.frame, text=summary, font=("Helvetica", 14),bg="#FFEF73").pack(pady=30)
        tk.Button(self.frame, text="📊 View Leaderboard", font=("Helvetica", 13, "bold"),activebackground="#C3B3E4",padx=50,pady=5,
            bg="#6A5ACD",fg="white",command=self.app.show_leaderboard).pack(pady=10)
        tk.Button(self.frame, text="❌ Exit", font=("Helvetica", 13, "bold"),activebackground="#C3B3E4",padx=50,pady=5,bg="#FF0303",fg="white", command=self.root.quit).pack(pady=5)

    def show_leaderboard(self, data):
        self.clear()
        tk.Label(self.frame, text="🏆 Leaderboard", font=("Helvetica", 16),bg=self.frame["bg"]).pack(pady=10)

        cols = ("Rank", "Player", "Algorithm", "Score", "Round", "Time Taken")
        tree = ttk.Treeview(self.frame, columns=cols, show="headings", height=10)

        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")

        for i, row in enumerate(data, 1):
            player, algo, score, round_num, time = row
            tree.insert("", "end", values=(i, player, algo, score, round_num, f"{time:.2f}"))

        tree.pack(expand=True, fill="both", pady=10)
        tk.Button(self.frame, text="🔙 Back to Menu", font=("Helvetica", 13, "bold"),activebackground="#C3B3E4",padx=50,pady=5,
            bg="#6A5ACD",fg="white", command=self.show_main_menu).pack(pady=10)


