# src/validation/validator.py

from tkinter import messagebox
from ui.message_ui import show_error, show_warning, show_success, show_info
from src.solution_controller import get_all_solutions, insert_player_solution,reset_all_solution_flags

# Solution Validations
def is_valid_solution(solution):
    for i in range(len(solution)):
        for j in range(i + 1, len(solution)):
            if abs(solution[i] - solution[j]) == abs(i - j):  # Check diagonals
                return False
    return True

# Solution Invalid ,already found, Correct 
def validate_and_save(name, player_pos):
    try:
        if not check_all_solutions_found():  # Stops if all are already found
            return
        try:
                all_solutions = get_all_solutions()
        except (ConnectionError, RuntimeError) as db_err:
                show_error("Database Error", f"Could not fetch solutions: {db_err}")
                return

        if not is_valid_solution(player_pos):
            show_error("Invalid Solution", "Incorrect! Queens are attacking each other. Try again!")
            return
        
        for sol_id, pos_str, is_found in all_solutions:
            try:
                stored_pos = tuple(map(int, pos_str.strip("()").split(",")))
            except (ValueError, TypeError) as parse_err:
                show_warning("Data Format Warning", f"Skipping a malformed solution entry: {parse_err}")
                continue
            if player_pos == stored_pos:
                if is_found:
                    show_warning("Already Found", "That solution has already been submitted!")
                    return
                try:
                    insert_player_solution(name, player_pos, sol_id)
                except (ConnectionError, RuntimeError) as insert_err:
                    show_error("Save Error", f"Failed to save solution: {insert_err}")
                    return

                remaining = [s for s in all_solutions if not s[2]]
                try:
                    if len(remaining) == 1:  # Current one was the last missing
                        win = show_success("Correct!", "You found the final solution! 🎉")
                        win.wait_window() 
                        show_info("🎉 All Solutions Found", "All 92 solutions have now been found!")
                        reset_all_solution_flags()
                    else:
                        show_success("Correct!", "You found a valid solution!")
                except Exception as e:
                        show_error("Reset Error", f"Something went wrong while resetting: {e}")
                return
        show_error("Wrong", "That's not a valid solution.")
    except Exception as e:
        show_error("Unexpected Error", f"An unexpected error occurred: {e}")

# Check if all solutions are found, reset the sound solutions
def check_all_solutions_found():
    try:
        all_solutions = get_all_solutions()
        remaining_solutions = [sol for sol in all_solutions if not sol[2]]  # If `is_found` is False
        if not remaining_solutions:
            show_info("🎉 All Solutions Found", "All solutions have already been found!")
            try:
                reset_all_solution_flags()
            except (ConnectionError, RuntimeError) as reset_err:
                show_error("Reset Error", f"Failed to reset solutions: {reset_err}")  
            return False
        return True
    except (ConnectionError, RuntimeError) as db_err:
        show_error("Database Error", f"Could not check solution status: {db_err}")
        return False
    except Exception as e:
        show_error("Unexpected Error", f"Unexpected issue during solution check: {e}")
        return False

# Board and queen Validations
def validate_queen_limit(queens):
    try:
        if len(queens) >= 8:
            show_warning("Limit", "You can only place up to 8 queens.")
            return False
        if len(set(queens)) != len(queens):  
            show_warning("Duplicate Position", "Queens cannot be placed in the same column.")
            return False
        return True
    except TypeError as te:
        show_error("Type Error", f"Invalid input type: {te}")
        return False
    except Exception as e:
        show_error("Unexpected Error", f"An unexpected error occurred: {e}")
        return False

# Player Input Validations (Name, Answers)
def validate_submission(queens, name):
    try:
        if len(queens) != 8:
            show_error("Error", "Place exactly 8 queens.")
            return False
        
        if not name.strip():
            show_error("Error", "Please Enter your name!")
            return False
        
        if len(name) > 50:  # Limit name length to 50 characters
            show_error("Error", "Name cannot exceed 50 characters.")
            return False

        if not name.isalpha():
            show_error("Error", "Name should only contain alphabetic characters.")
            return False
        
        if not queens:
            show_error("Error", "No queens placed. Please place queens on the board.")
            return False
        
        if len(set(queens)) != len(queens):
            show_warning("Duplicate Row", "You cannot place more than one queen on the same row.")
            return False
        
        return True
    except (TypeError, ValueError) as val_err:
        show_error("Validation Error", f"Invalid data: {val_err}")
        return False
    except Exception as e:
        show_error("Unexpected Error", f"An unexpected error occurred: {e}")
        return False

