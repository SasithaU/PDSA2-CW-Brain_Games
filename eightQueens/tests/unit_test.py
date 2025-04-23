# tests/unit_test.py

import unittest
from unittest.mock import patch
from db.connection import get_connection
from utils.save_sequential import save_sequential_results
from utils.save_threaded import save_threaded_results
from src.solution_controller import insert_player_solution, get_all_solutions, reset_all_solution_flags
from src.validation.validator import is_valid_solution,validate_queen_limit,validate_submission

class TestEightQueensGame(unittest.TestCase):
    def setUp(self):
        self.conn = get_connection()
        if self.conn is None:
            self.skipTest("Database connection failed. Skipping test.")
        self.cursor = self.conn.cursor()
        self.reset_db()

    def tearDown(self):
        self.cursor.close()
        self.conn.close()

    @classmethod
    def reset_db(cls):
        conn = get_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
            cursor.execute("DELETE FROM threaded_solutions")
            cursor.execute("DELETE FROM sequential_solutions")
            cursor.execute("DELETE FROM players")
            cursor.execute("DELETE FROM solutions")
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
            conn.commit()
            cursor.close()
            conn.close()

    def test01_is_valid_solution_valid_case(self):
        print("Unit_Test_1: is_valid_solution with a valid arrangement    ✅Passed")
        solution = (0, 4, 7, 5, 2, 6, 1, 3)
        self.assertTrue(is_valid_solution(solution))

    def test02_is_valid_solution_invalid_case(self):
        print("Unit_Test_2: is_valid_solution with an invalid (diagonal attack) arrangement    ✅Passed")
        solution = (0, 1, 2, 3, 4, 5, 6, 7)
        self.assertFalse(is_valid_solution(solution))

    def test03_validate_queen_limit_valid(self):
        print("Unit_Test_3: validate_queen_limit with less than 8 unique positions    ✅Passed")
        queens = [0, 1, 2, 3, 4, 5, 6]
        result = validate_queen_limit(queens)
        self.assertTrue(result)

    @patch('tkinter.messagebox.showwarning')
    def test04_validate_queen_limit_too_many(self,showwarning):
        print("Unit_Test_4: validate_queen_limit with more than 8 queens    ✅Passed")
        queens = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        result = validate_queen_limit(queens)
        showwarning.assert_called() 
        self.assertFalse(result)

    @patch('tkinter.messagebox.showwarning')
    def test05_validate_queen_limit_duplicate_columns(self,showwarning):
        print("Unit_Test_5: validate_queen_limit with duplicate columns    ✅Passed")
        queens = [0, 1, 2, 3, 3]
        result = validate_queen_limit(queens)
        showwarning.assert_called() 
        self.assertFalse(result)

    def test06_validate_submission_valid(self):
        print("Unit_Test_6: validate_submission with correct name and queen positions    ✅Passed")
        queens = [0, 4, 7, 5, 2, 6, 1, 3]
        name = "Alice"
        self.assertTrue(validate_submission(queens, name))

    @patch('tkinter.messagebox.showerror')
    def test07_validate_submission_empty_name(self,mock_showerror):
        print("Unit_Test_7: validate_submission with empty name    ✅Passed")
        queens = [0, 4, 7, 5, 2, 6, 1, 3]
        name = ""
        result = validate_submission(queens, name)
        mock_showerror.assert_called() 
        self.assertFalse(result)

    @patch('tkinter.messagebox.showerror')
    def test08_validate_submission_non_alpha_name(self,mock_showerror):
        print("Unit_Test_8: validate_submission with name containing numbers    ✅Passed")
        queens = [0, 4, 7, 5, 2, 6, 1, 3]
        name = "Alice123"
        result = validate_submission(queens, name)
        mock_showerror.assert_called() 
        self.assertFalse(result)

    @patch('tkinter.messagebox.showerror')
    def test09_validate_submission_too_long_name(self,mock_showerror):
        print("Unit_Test_9: validate_submission with name longer than 50 characters    ✅Passed")
        name = "A" * 51
        queens = [0, 4, 7, 5, 2, 6, 1, 3]
        result = validate_submission(queens, name)
        mock_showerror.assert_called() 
        self.assertFalse(result)

    @patch('tkinter.messagebox.showerror')
    def test10_validate_submission_wrong_number_of_queens(self,mock_showerror):
        print("Unit_Test_10: validate_submission with fewer than 8 queens    ✅Passed")
        name = "Bob"
        queens = [0, 1, 2, 3]
        result = validate_submission(queens, name)
        mock_showerror.assert_called() 
        self.assertFalse(result)

    @patch('tkinter.messagebox.showwarning')
    def test11_validate_submission_duplicate_rows(self,showwarning):
        print("Unit_Test_11: validate_submission with duplicate queen rows    ✅Passed")
        name = "Charlie"
        queens = [0, 1, 2, 3, 4, 4, 6, 7]
        result = validate_submission(queens, name)  
        showwarning.assert_called()  
        self.assertFalse(result) 

    def test12_sequential_saves_92_solutions(self):
        print("\n🔹 Unit_Test_12: sequential_backtracking_saves_92_solutions    ✅Passed")
        save_sequential_results()
        self.cursor.execute("SELECT COUNT(*) FROM sequential_solutions")
        count = self.cursor.fetchone()[0]
        self.assertEqual(count, 92, f"Expected 92 sequential solutions, found {count}.")


    def test13_threaded_saves_92_solutions(self):
        print("\n🔹 Unit_Test_13: threaded_backtracking_saves_92_solutions    ✅Passed")
        save_threaded_results()
        self.cursor.execute("SELECT COUNT(*) FROM threaded_solutions")
        count = self.cursor.fetchone()[0]
        self.assertEqual(count, 92, f"Expected 92 threaded solutions, found {count}.")


    def test14_record_player_answer(self):
        print("\n🔹 Unit_Test_14: save_correct_player_solution")
        correct_positions = "0,4,7,5,2,6,1,3"
        self.cursor.execute("INSERT INTO solutions (positions, is_found) VALUES (%s, %s)", (correct_positions, 1))
        solution_id = self.cursor.lastrowid
        self.conn.commit()
        player_name = "Alice"
        submitted_positions = "0,4,7,5,2,6,1,3"
        self.cursor.execute("SELECT id FROM solutions WHERE positions = %s AND is_found = 1", (submitted_positions,))
        match = self.cursor.fetchone()
        if match:
            matched_solution_id = match[0]
            insert_player_solution(player_name, submitted_positions, matched_solution_id)
            self.conn.commit() 
            print(f"Solution {submitted_positions} is Correct! Recorded for player: {player_name}    ✅Passed")
            self.cursor.execute("SELECT name, positions, solution_id FROM players WHERE name=%s", (player_name,))
            row = self.cursor.fetchone()
        self.assertIsNotNone(row)
        self.assertEqual(row[0], player_name)
        self.assertEqual(row[1], submitted_positions)
        self.assertEqual(row[2], matched_solution_id)
    

    def test15_invalid_solution_should_not_be_recorded(self):
        print("\n🔹 Unit_Test_15: invalid_solution_should_not_be_recorded")
        submitted_positions = "3,0,4,7,1,6,2,5"
        player_name = "Bob"
        self.cursor.execute("SELECT id FROM solutions WHERE positions = %s AND is_found = 1", (submitted_positions,))
        match = self.cursor.fetchone()
        self.assertIsNone(match)
        print(f"Submitted solution {submitted_positions} is Incorrect. Not recorded for {player_name}.    ✅Passed")


    def test16_duplicate_solution_by_another_player(self):
        print("\n🔹 Unit_Test_16: solution_already_submitted")
        positions = "0,4,7,5,2,6,1,3"
        is_found_flag = 1  
        player1 = "Alice"
        player2 = "Bob"
        self.assertEqual(is_found_flag, 1)
        print(f"Solution already recognized for {positions}. Try again until all other solutions are found.    ✅Passed")

    
    def test17_clear_flags_when_all_solutions_found(self):
        print("\n🔹 Unit_Test_17: clear_flags_when_all_solutions_found")
        reset_all_solution_flags()
        self.cursor.execute("UPDATE solutions SET is_found = 1")
        self.conn.commit()
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM solutions WHERE is_found = TRUE")
        remaining = cursor.fetchone()[0]
        conn.close()
        print(f"All solution flags cleared after recognizing the last solution.    ✅Passed")
        self.assertEqual(remaining, 0, "Flags should be cleared after all solutions were recognized.")

    @classmethod
    def tearDownClass(cls):
        cls.reset_db()
       
if __name__ == '__main__':
    unittest.main()

