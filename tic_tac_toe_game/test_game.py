import pytest
from algorithms import (
    get_available_moves,
    get_computer_move_minimax,
    get_computer_move_alphabeta,
    check_winner,
    is_draw
)
#Test for available moves
def test_get_available_moves():
    board = [
        ['X', 'O', 'X', 'O', 'X'],
        ['O', 'X', 'O', 'X', 'O'],
        ['X', 'O', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ']
    ]
    moves = get_available_moves(board)
    assert (2, 2) in moves
    assert (0, 0) not in moves
    assert len(moves) == 13

#Test for Horizontal winner
def test_check_winner_horizontal():
    board = [['X'] * 5] + [['-'] * 5 for _ in range(4)]
    assert check_winner(board, 'X') is True

#Test for Vertical winner
def test_check_winner_vertical():
    board = [['O'] + ['-'] * 4 for _ in range(5)]
    assert check_winner(board, 'O') is True

#Test for Diagonal winner
def test_check_winner_diagonal():
    board = [['-' for _ in range(5)] for _ in range(5)]
    for i in range(5):
        board[i][i] = 'X'
    assert check_winner(board, 'X') is True

#Test for Draw check
def test_is_draw():
    board = [
        ['X', 'O', 'X', 'O', 'X'],
        ['O', 'X', 'O', 'X', 'O'],
        ['X', 'O', 'X', 'O', 'X'],
        ['O', 'X', 'O', 'X', 'O'],
        ['X', 'O', 'X', 'O', 'X']
    ]
    assert is_draw(board) is True

#Test for Minimax move validity
def test_minimax_move_returns_valid_move():
    board = [[' ' for _ in range(5)] for _ in range(5)]
    move = get_computer_move_minimax(board)
    assert move in get_available_moves(board)

#Test for Alpha-beta move validity
def test_alphabeta_move_returns_valid_move():
    board = [[' ' for _ in range(5)] for _ in range(5)]
    move = get_computer_move_alphabeta(board)
    assert move in get_available_moves(board)
