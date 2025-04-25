import tkinter as tk
from game.ui import TSPGameUI
from game.utils import generate_distance_matrix
from game.logic import brute_force_tsp, greedy_tsp, dp_tsp
from db.models import save_result, log_algorithm_times  # ✅ Import both
import random
from tkinter import messagebox
from game.utils import format_route

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
        if not selected or len(selected) < 2:
            messagebox.showerror("Error", "❌ Please select at least *two* cities.")
            return
        self.selected_cities = selected
        self.matrix = generate_distance_matrix([self.home] + self.selected_cities)
        self.ui.show_distance_matrix(self.matrix, self.home, self.selected_cities, self.on_route_entered)


    def on_route_entered(self, route):
        if not route or route[0] != self.home or route[-1] != self.home:
            messagebox.showerror("Error", "❌ Route must start and end at home city.")
            return

        self.user_route = route

        try:
            # Run all algorithms
            bf_route, bf_cost, bf_time = brute_force_tsp(self.matrix, self.home, self.selected_cities)
            greedy_route, greedy_cost, greedy_time = greedy_tsp(self.matrix, self.home, self.selected_cities)
            dp_route, dp_cost, dp_time = dp_tsp(self.matrix, self.home, self.selected_cities)

            # ✅ Log algorithm times to new table
            log_algorithm_times(
                player_name=self.player,
                round_number=self.round_number,
                brute_force_time=bf_time,
                greedy_time=greedy_time,
                dp_time=dp_time
            )
            self.round_number += 1  # ✅ Increment round number

            # Calculate user cost
            user_cost = 0
            for i in range(len(route)-1):
                user_cost += self.matrix[route[i]][route[i+1]]

            # Check if user is correct
            if user_cost == bf_cost:
                correct = True
                self.total_score += 1
                save_result(
                    self.player, self.home, self.selected_cities,
                    route, bf_cost, bf_time, greedy_time, dp_time
                )
                messagebox.showinfo("Correct!", f"✅ You found the shortest route!\nYour Score: {self.total_score}")
            else:
                correct = False
                messagebox.showinfo("Incorrect", f"❌ Not the shortest route.\nYour distance: {user_cost} km\nBest: {bf_cost} km")

            # Show result
            self.ui.show_result_screen(
                user_route=route,
                user_cost=user_cost,
                correct=correct,
                bf=(bf_route, bf_cost, bf_time),
                greedy=(greedy_route, greedy_cost, greedy_time),
                dp=(dp_route, dp_cost, dp_time),
                play_again_callback=self.on_start_game,
                quit_callback=self.show_final_result
            )

        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong: {e}")

    def show_final_result(self):
        messagebox.showinfo("Game Over", f"🎯 Final Score: {self.total_score}")
        self.ui.show_main_menu()
            
    def exit_game(self):
        self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = TSPGameApp(root)
    root.mainloop()
