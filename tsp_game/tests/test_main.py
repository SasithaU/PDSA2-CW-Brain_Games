import unittest
from unittest.mock import patch, MagicMock
from main import TSPGameApp

class TestTSPGameApp(unittest.TestCase):

    def setUp(self):
        with patch('main.TSPGameUI') as MockUI:
            self.mock_ui = MockUI.return_value
            self.app = TSPGameApp(root=MagicMock())
            self.app.ui = self.mock_ui  # Mock the UI to avoid real UI calls
            self.app.player = "Alice"

    def test_set_player_valid_name(self):
        self.app.set_player(" Bob ")
        self.assertEqual(self.app.player, "Bob")
        self.mock_ui.show_main_menu.assert_called_once()

    def test_set_player_blank_name(self):
        self.app.set_player("   ")
        self.assertEqual(self.app.player, "Alice")  # Should remain unchanged
        self.mock_ui.show_main_menu.assert_not_called()

    @patch('main.random.choice', return_value="A")
    def test_on_start_game_sets_home_and_shows_city_selection(self, mock_choice):
        self.app.on_start_game()
        self.assertEqual(self.app.home, "A")
        self.mock_ui.show_city_selection.assert_called_once()

    @patch('tkinter.messagebox.showerror')
    def test_on_city_selected_none(self, mock_error):
        self.app.home = "A"
        self.app.on_city_selected([])
        mock_error.assert_called_once_with("Error", "❌ Please select at least *two* cities.")
        self.mock_ui.show_distance_matrix.assert_not_called()

    @patch('tkinter.messagebox.showerror')
    def test_on_city_selected_less_than_two(self, mock_error):
        self.app.home = "A"
        self.app.on_city_selected(["B"])
        mock_error.assert_called_once_with("Error", "❌ Please select at least *two* cities.")
        self.mock_ui.show_distance_matrix.assert_not_called()

    @patch('tkinter.messagebox.showerror')
    @patch('main.generate_distance_matrix', return_value={'A': {'A': 0, 'B': 60, 'C': 70}, 'B': {'A': 60, 'B': 0, 'C': 80}, 'C': {'A': 70, 'B': 80, 'C': 0}})
    def test_on_city_selected_valid(self, mock_matrix, mock_error):
        self.app.home = "A"
        selected_cities = ["B", "C"]
        self.app.on_city_selected(selected_cities)

        mock_error.assert_not_called()
        self.assertEqual(self.app.selected_cities, selected_cities)
        self.mock_ui.show_distance_matrix.assert_called_once()

    @patch('tkinter.messagebox.showerror')
    def test_on_route_entered_invalid(self, mock_error):
        self.app.home = "A"
        self.app.on_route_entered(["B", "A"])  # Invalid: does not start and end at home
        mock_error.assert_called_once_with("Error", "❌ Route must start and end at home city.")

    @patch('tkinter.messagebox.showinfo')
    @patch('main.save_result')
    @patch('main.log_algorithm_times')
    @patch('main.dp_tsp', return_value=(['A', 'B', 'A'], 100, 0.1))
    @patch('main.greedy_tsp', return_value=(['A', 'B', 'A'], 100, 0.2))
    @patch('main.brute_force_tsp', return_value=(['A', 'B', 'A'], 100, 0.3))
    def test_on_route_entered_correct_route(self, mock_bf, mock_greedy, mock_dp, mock_log, mock_save, mock_info):
        self.app.player = "Alice"
        self.app.home = "A"
        self.app.round_number = 1
        self.app.selected_cities = ["B"]
        self.app.matrix = {'A': {'A': 0, 'B': 50}, 'B': {'A': 50, 'B': 0}}

        route = ["A", "B", "A"]
        self.app.on_route_entered(route)

        mock_log.assert_called_once()
        mock_save.assert_called_once()
        mock_info.assert_called_with("Correct!", "✅ You found the shortest route!\nYour Score: 1")
        self.assertEqual(self.app.total_score, 1)
        self.assertEqual(self.app.round_number, 2)

    @patch('tkinter.messagebox.showinfo')
    @patch('main.save_result')
    @patch('main.log_algorithm_times')
    @patch('main.dp_tsp', return_value=(['A', 'B', 'A'], 100, 0.1))
    @patch('main.greedy_tsp', return_value=(['A', 'B', 'A'], 100, 0.2))
    @patch('main.brute_force_tsp', return_value=(['A', 'B', 'A'], 100, 0.3))
    def test_on_route_entered_incorrect_route(self, mock_bf, mock_greedy, mock_dp, mock_log, mock_save, mock_info):
        self.app.player = "Alice"
        self.app.home = "A"
        self.app.round_number = 1
        self.app.selected_cities = ["B"]
        self.app.matrix = {'A': {'A': 0, 'B': 70}, 'B': {'A': 70, 'B': 0}}

        route = ["A", "B", "A"]
        self.app.on_route_entered(route)

        mock_log.assert_called_once()
        mock_save.assert_not_called()
        mock_info.assert_called_with("Incorrect", "❌ Not the shortest route.\nYour distance: 140 km\nBest: 100 km")
        self.assertEqual(self.app.total_score, 0)
        self.assertEqual(self.app.round_number, 2)

    @patch('tkinter.messagebox.showinfo')
    def test_show_final_result(self, mock_info):
        self.app.total_score = 3
        self.app.show_final_result()
        mock_info.assert_called_once_with("Game Over", "🎯 Final Score: 3")
        self.mock_ui.show_main_menu.assert_called_once()

if __name__ == "__main__":
    unittest.main()
