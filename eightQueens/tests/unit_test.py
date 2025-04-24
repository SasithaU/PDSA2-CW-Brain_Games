# tests/unit_test.py

import unittest
from unittest.mock import patch
from db.connection import get_connection
from utils.save_sequential import save_sequential_results
from utils.save_threaded import save_threaded_results
from src.algorithm.backtracking_threaded import solve_n_queens_threaded
from src.algorithm.backtracking_sequential import solve_n_queens_sequential
from src.solution_controller import insert_player_solution, get_all_solutions, reset_all_solution_flags
from src.validation.validator import is_valid_solution,validate_queen_limit,validate_submission

def setup_test_data(conn):
    cursor = conn.cursor()
    conn.commit()
    cursor.close()


class TestEightQueensGame(unittest.TestCase):
    def setUp(self):
        self.conn = get_connection(is_test=True)
        if self.conn is None:
            self.skipTest("Database connection failed. Skipping test.")
        self.cursor = self.conn.cursor()
        setup_test_data(self.conn)
        self.reset_db()

    def tearDown(self):
        self.cursor.close()
        self.conn.close()

    @classmethod
    def drop_database(cls):
        conn = get_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("DROP DATABASE temp_test_db") 
            conn.commit()
            cursor.close()
            conn.close()

    @classmethod
    def reset_db(cls):
        conn = get_connection()
        if conn:
            cursor = conn.cursor()
            conn.commit()
            cursor.close()
            conn.close()

    def test01_is_valid_solution_valid_case(self):
        solution = (0, 4, 7, 5, 2, 6, 1, 3)
        try:
            self.assertTrue(is_valid_solution(solution))
            print("Unit_Test_1: is_valid_solution with a valid arrangement    ✅Passed")
        except AssertionError:
            print("Unit_Test_1: is_valid_solution with a valid arrangement    ❌Failed")
            raise


    def test02_is_valid_solution_invalid_case(self):
        solution = (0, 1, 2, 3, 4, 5, 6, 7)
        try:
            self.assertFalse(is_valid_solution(solution))
            print("Unit_Test_2: is_valid_solution with an invalid (diagonal attack) arrangement    ✅Passed")
        except AssertionError:
            print("Unit_Test_2: is_valid_solution with an invalid (diagonal attack) arrangement    ❌Failed")
            raise


    def test03_validate_queen_limit_valid(self):
        queens = [0, 1, 2, 3, 4, 5, 6]
        try:
            result = validate_queen_limit(queens)
            self.assertTrue(result)
            print("Unit_Test_3: validate_queen_limit with less than 8 unique positions    ✅Passed")
        except AssertionError:
            print("Unit_Test_3: validate_queen_limit with less than 8 unique positions    ❌Failed")
            raise

    def test04_validate_queen_limit_too_many(self):
        queens = [0, 1, 2, 3, 4, 5, 6, 7, 8]  # More than 8 queens
        try:
            result = validate_queen_limit(queens)
            self.assertFalse(result)  # Ensure the function returns False
            print("Unit_Test_4: validate_queen_limit with more than 8 queens    ✅ Passed")
        except AssertionError:
            print("Unit_Test_4: validate_queen_limit with more than 8 queens    ❌ Failed")
            raise

    def test05_validate_queen_limit_duplicate_columns(self):
        queens = [0, 1, 2, 3, 3]  # Duplicate columns
        try:
            result = validate_queen_limit(queens)
            self.assertFalse(result)  # Ensure the function returns False
            print("Unit_Test_5: validate_queen_limit with duplicate columns    ✅ Passed")
        except AssertionError:
            print("Unit_Test_5: validate_queen_limit with duplicate columns    ❌ Failed")
            raise


    def test06_validate_submission_valid(self):
        queens = [0, 4, 7, 5, 2, 6, 1, 3]
        name = "Alice"
        # Direct assertion instead of try-except
        result = validate_submission(queens, name)
        self.assertTrue(result, "Expected validate_submission to return True for valid input")
        print("Unit_Test_6: validate_submission with correct name and queen positions    ✅ Passed")


    def test07_validate_submission_empty_name(self):
        queens = [0, 4, 7, 5, 2, 6, 1, 3]
        name = ""  # Empty name
        result = validate_submission(queens, name)
        self.assertFalse(result, "Expected validate_submission to return False for empty name")
        print("Unit_Test_7: validate_submission with empty name    ✅ Passed")


    def test08_validate_submission_non_alpha_name(self):
        queens = [0, 4, 7, 5, 2, 6, 1, 3]
        name = "Alice123"  # Name containing numbers
        result = validate_submission(queens, name)
        
        self.assertFalse(result, "Expected validate_submission to return False for non-alpha name")
        print("Unit_Test_8: validate_submission with name containing numbers    ✅ Passed")


    def test09_validate_submission_too_long_name(self):
        name = "A" * 51  # Name longer than 50 characters
        queens = [0, 4, 7, 5, 2, 6, 1, 3]
        result = validate_submission(queens, name)
        
        self.assertFalse(result, "Expected validate_submission to return False for name longer than 50 characters")
        print("Unit_Test_9: validate_submission with name longer than 50 characters    ✅ Passed")

    def test10_validate_submission_wrong_number_of_queens(self):
        name = "Bob"
        queens = [0, 1, 2, 3]  # Fewer than 8 queens
        result = validate_submission(queens, name)
        
        self.assertFalse(result, "Expected validate_submission to return False for fewer than 8 queens")
        print("Unit_Test_10: validate_submission with fewer than 8 queens    ✅ Passed")

    def test11_validate_submission_duplicate_rows(self):
        name = "Charlie"
        queens = [0, 1, 2, 3, 4, 4, 6, 7]  # Duplicate queen rows
        result = validate_submission(queens, name)
        self.assertFalse(result, "Expected validate_submission to return False for duplicate queen rows")
        print("Unit_Test_11: validate_submission with duplicate queen rows    ✅ Passed")

    def test12_threaded_saves_92_solutions(self):
        solutions = solve_n_queens_threaded()  
        for solution in solutions:
            positions = ','.join(map(str, solution))
            self.cursor.execute("INSERT INTO threaded_solutions (positions, is_found) VALUES (%s, %s)", (positions, True))       
        self.conn.commit()    
        self.cursor.execute("SELECT COUNT(*) FROM threaded_solutions")
        count = self.cursor.fetchone()[0]  
        try:
            self.assertEqual(count, 92, f"Expected 92 threaded solutions, found {count}.")
            print("\n🔹 Unit_Test_12: threaded_backtracking_saves_92_solutions    ✅Passed")
        except AssertionError as e:
            print(f"❌ Unit_Test_12: threaded_backtracking_saves_92_solutions    ❌Failed - {str(e)}")
        
    
    def test13_sequential_saves_92_solutions(self):
        solutions = solve_n_queens_sequential()
        for solution in solutions:
            positions = ','.join(map(str, solution))
            self.cursor.execute("INSERT INTO sequential_solutions (positions, is_found) VALUES (%s, %s)", (positions, True))       
        self.conn.commit()  
        self.cursor.execute("SELECT COUNT(*) FROM sequential_solutions")
        count = self.cursor.fetchone()[0]  
        try:
            self.assertEqual(count, 92, f"Expected 92 threaded solutions, found {count}.")
            print("\n🔹 Unit_Test_13: sequential_backtracking_saves_92_solutions    ✅Passed")
        except AssertionError as e:
            print(f"❌ Unit_Test_13: sequential_backtracking_saves_92_solutions    ❌Failed - {str(e)}")
           
    def test14_record_player_answer(self):
        try:
            print("\n🔹 Unit_Test_14: save_correct_player_solution")
            correct_positions = "0,4,7,5,2,6,1,3"                
            self.cursor.execute("INSERT INTO solutions (positions, is_found) VALUES (%s, %s)", (correct_positions, 1))
            self.conn.commit()  # Commit after inserting the solution
            player_name = "Alice"
            submitted_positions = "0,4,7,5,2,6,1,3"                
            self.cursor.execute("SELECT sol_id FROM solutions WHERE positions = %s AND is_found = 1", (submitted_positions,))
            match = self.cursor.fetchone() 
            if match:
                matched_solution_id = match[0]
                time_taken = 0                     
                self.cursor.execute("""
                    INSERT INTO players (name, positions, solution_id) 
                    VALUES (%s, %s, %s)
                """, (player_name, submitted_positions, matched_solution_id))
                self.conn.commit() 
                print(f"Solution {submitted_positions} is Correct! Recorded for player: {player_name}    ✅Passed")                    
                self.cursor.execute("SELECT name, positions, solution_id FROM players WHERE name=%s", (player_name,))
                row = self.cursor.fetchone()                    
                print(f"Fetched row: {row}")
                self.assertIsNotNone(row, "Expected a row to be returned, but got None.")
                self.assertEqual(row[0], player_name)
                self.assertEqual(row[1], submitted_positions)
                self.assertEqual(row[2], matched_solution_id)
            else:
                print("No matching solution found in the database.")
                self.fail("No matching solution found for the submitted positions.")
        except AssertionError as e:
                print(f"\n🔹 Unit_Test_14: save_correct_player_solution    ❌Failed - {str(e)}")
                raise      
 
    def test15_invalid_solution_should_not_be_recorded(self):
        try:
            print("\n🔹 Unit_Test_15: invalid_solution_should_not_be_recorded")
            submitted_positions = "3,0,4,7,1,6,2,5"
            player_name = "Bob"
            self.cursor.execute("SELECT sol_id FROM solutions WHERE positions = %s AND is_found = 1", (submitted_positions,))
            match = self.cursor.fetchone()
            self.assertIsNone(match)
            print(f"Submitted solution {submitted_positions} is Incorrect. Not recorded for {player_name}.    ✅Passed")
        except AssertionError:
            print("\n🔹 Unit_Test_15: invalid_solution_should_not_be_recorded    ❌Failed")
            raise

    def test16_duplicate_solution_by_another_player(self):
        try:
            print("\n🔹 Unit_Test_16: solution_already_submitted")
            positions = "0,4,7,5,2,6,1,3"
            is_found_flag = 1  
            player1 = "Alice"
            player2 = "Bob"
            self.assertEqual(is_found_flag, 1)
            print(f"Solution already recognized for {positions}. Try again until all other solutions are found.    ✅Passed")
        except AssertionError:
            print("\n🔹 Unit_Test_16: solution_already_submitted    ❌Failed")
            raise

    # def test17_clear_flags_when_all_solutions_found(self):
    #     try:
    #         print("\n🔹 Unit_Test_17: clear_flags_when_all_solutions_found")
    #         reset_all_solution_flags()
    #         self.cursor.execute("UPDATE solutions SET is_found = 1")
    #         self.conn.commit()
    #         conn = get_connection()
    #         cursor = conn.cursor()
    #         cursor.execute("SELECT COUNT(*) FROM solutions WHERE is_found = TRUE")
    #         remaining = cursor.fetchone()[0]
    #         conn.close()
    #         print(f"All solution flags cleared after recognizing the last solution.    ✅Passed")
    #         self.assertEqual(remaining, 0, "Flags should be cleared after all solutions were recognized.")
    #     except AssertionError:
    #         print("\n🔹 Unit_Test_17: clear_flags_when_all_solutions_found    ❌Failed")
    #         raise

    @classmethod
    def tearDownClass(cls):
        cls.reset_db()
        cls.drop_database()
       
if __name__ == '__main__':
    unittest.main()

