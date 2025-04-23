import tkinter as tk
from game.ui import TSPGameUI
from game.utils import generate_distance_matrix
from game.logic import brute_force_tsp, greedy_tsp, dp_tsp
from db.models import save_result, get_leaderboard
import random
from tkinter import messagebox

cities = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]

class TSPGameApp:
    def __init__(self, root):
        self.root = root
        self.ui = TSPGameUI(root, self)
        self.round_number = 1
        self.total_score = 0
        self.player = ""
        self.home = ""
        self.selected_cities = []
        self.matrix = {}
        self.user_route = []
        self.ui.show_welcome_screen()

    def set_player(self, name):
        if name.strip():
            self.player = name.strip()
            self.ui.show_main_menu()

    def on_start_game(self):
        self.home = random.choice(cities)
        self.ui.show_city_selection(self.home, [c for c in cities if c != self.home])

    def on_city_selected(self, selected):
        if not selected:
            messagebox.showerror("Error", "❌ Please select at least one city.")
            return
        self.selected_cities = selected
        self.matrix = generate_distance_matrix([self.home] + self.selected_cities)
        self.ui.show_distance_matrix(self.matrix, self.home, self.selected_cities, self.on_route_entered)

    def on_route_entered(self, route):
        if not route or route[0] != self.home or route[-1] != self.home:
            messagebox.showerror("Error", "❌ Route must start and end at home city.")
            return
        self.user_route = route
        self.ui.show_algorithm_choice()

    def on_algorithm_chosen(self, algo_choice):
        if algo_choice == "1":
            correct_route, correct_distance, time_taken = brute_force_tsp(self.matrix, self.home, self.selected_cities)
            algo_name = "Brute Force"
        elif algo_choice == "2":
            correct_route, correct_distance, time_taken = greedy_tsp(self.matrix, self.home, self.selected_cities)
            algo_name = "Greedy"
        elif algo_choice == "3":
            correct_route, correct_distance, time_taken = dp_tsp(self.matrix, self.home, self.selected_cities)
            algo_name = "Dynamic Programming"
        else:
            messagebox.showerror("Error", "❌ Invalid algorithm choice.")
            return

        try:
            user_distance = sum(
                self.matrix[self.user_route[i]][self.user_route[i + 1]] for i in range(len(self.user_route) - 1)
            )
        except (KeyError, IndexError):
            messagebox.showerror("Error", "❌ Invalid route entered.")
            return

        is_correct = self.user_route == correct_route
        score = 1 if is_correct else 0

        save_result(
            self.player,
            self.home,
            self.selected_cities,
            correct_route,
            algo_name,
            time_taken,
            score,
            self.round_number
        )

        self.total_score += score
        self.round_number += 1
        self.ui.show_result_screen(correct_route, correct_distance, time_taken, self.user_route, is_correct)

    def play_again(self):
        self.on_start_game()

    def end_game(self):
        self.ui.show_final_score(self.player, self.total_score, self.round_number - 1)

    def show_leaderboard(self):
        data = get_leaderboard()
        self.ui.show_leaderboard(data)


if __name__ == "__main__":
    root = tk.Tk()
    app = TSPGameApp(root)
    root.mainloop()
