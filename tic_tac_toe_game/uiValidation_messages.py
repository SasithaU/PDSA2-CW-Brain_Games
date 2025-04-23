import tkinter as tk
from tkinter import messagebox
import game_validation

def validate_inputs(name, difficulty): #Function to validate the inputs and display suitable error messages
    if not game_validation.is_valid_name(name):
        messagebox.showerror("Invalid Name", "Please enter a valid name (letters only).")
        return False
    if not game_validation.is_valid_difficulty(difficulty):
        messagebox.showerror("Invalid Difficulty", "Please select a difficulty level.")
        return False
    return True

def show_invalid_move(): #Function to validate the movement and display suitable error message
    messagebox.showwarning("Invalid Move", "That cell is already occupied or out of bounds.")

def show_game_over(winner): #Function to validate the game over state and display a suitable message to the player
    if winner == "Draw":
        messagebox.showinfo("Game Over", "It's a draw!")
    else:
        messagebox.showinfo("Game Over", f"{winner} wins!")