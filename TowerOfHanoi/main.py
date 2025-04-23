import ui
import database
from hanoi_algorithm import solve_hanoi_recursive, solve_hanoi_iterative
import random
import time

def play_round(selected_algorithm, num_of_disks, user_moves):
    source_peg = 'A'
    destination_peg = 'C'
    auxiliary_peg = 'B'
    correct_moves = []
    start_time = time.time()

    if selected_algorithm == "recursive":
        correct_moves = solve_hanoi_recursive(num_of_disks, source_peg, destination_peg, auxiliary_peg)
    elif selected_algorithm == "iterative":
        correct_moves = solve_hanoi_iterative(num_of_disks, source_peg, destination_peg, auxiliary_peg)
    end_time = time.time()
    algorithm_duration = end_time - start_time

    is_correct = (user_moves == correct_moves)
    return is_correct, correct_moves, num_of_disks, selected_algorithm, algorithm_duration

def main():
    ui.home_page()
    database.connect_db() # Attempt database connection on start

    while True:
        num_of_disks = random.randint(3, 6) # Adjust range as needed for UI
        algorithm_choice, user_moves_str = ui.get_user_input(num_of_disks)
        user_moves = ui.parse_user_moves(user_moves_str)

        if algorithm_choice:
            is_correct, correct_moves, num_of_disks, algorithm, duration = play_round(algorithm_choice, num_of_disks, user_moves)
            ui.display_result(is_correct, correct_moves)

            if is_correct:
                player_name = ui.get_player_name()
                if player_name:
                    database.save_correct_response(player_name, num_of_disks, correct_moves)
                    database.record_algorithm_time(num_of_disks, algorithm, duration)

        if not ui.play_again():
            break

    database.close_db()

if __name__ == "__main__":
    main()


