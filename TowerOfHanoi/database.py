import mysql.connector
from tkinter import messagebox



DB_CONFIG = {
    'host' : 'localhost',
    'user' : 'root',
    'password' : 'root',
    'database' : 'hanoi_game_db'
}
mydb = None 
def connect_db(): 
    global mydb 
    try: 
       mydb = mysql.connector.connect(**DB_CONFIG)
       print("Connected to MySQL database.") 
    except mysql.connector.Error as err: 
        messagebox.showerror("Database Error", f"Error connecting to database: {err}") 
        print(f"Error connecting to database: {err}") 
        mydb = None 
def close_db(): 
    global mydb 
    if mydb and mydb.is_connected(): 
        mydb.close() 
        print("MySQL database connection closed.") 
        mydb = None 
def save_correct_response(player_name, num_of_disks, correct_moves): 
    if mydb and mydb.is_connected(): 
        cursor = mydb.cursor() 
        sql = "INSERT INTO correct_responses (player_name, num_of_disks, correct_moves) VALUES (%s, %s, %s)" 
        val = (player_name, num_of_disks, ', '.join([f"{m[0]}->{m[1]}" for m in correct_moves])) 
        try: 
            cursor.execute(sql, val) 
            mydb.commit() 
            messagebox.showinfo("Score Saved", "Correct response saved!") 
        except mysql.connector.Error as err: 
            messagebox.showerror("Database Error", f"Error saving response: {err}") 
            print(f"Error saving response: {err}") 
        finally: 
            cursor.close() 
def record_algorithm_time(num_of_disks, algorithm, duration): 
    if mydb and mydb.is_connected(): 
        cursor = mydb.cursor() 
        sql = "INSERT INTO algorithm_times (num_of_disks, algorithm, duration) VALUES (%s, %s, %s)" 
        val = (num_of_disks, algorithm, duration) 
        try: 
            cursor.execute(sql, val) 
            mydb.commit() 
            print(f"Time recorded for {algorithm} with {num_of_disks} disks: {duration:.4f} seconds.") 
        except mysql.connector.Error as err: 
            messagebox.showerror("Database Error", f"Error recording algorithm time: {err}") 
            print(f"Error recording algorithm time: {err}") 
        finally: 
            cursor.close() 
if __name__ == '__main__': 
    # Example usage (will run if you execute database_utils.py directly) 
    connect_db() 
    if mydb: 
        # Example data (replace with actual game data) 
        save_correct_response("Test Player", 3, [('A', 'C'), ('A', 'B'), ('C', 'B')]) 
        record_algorithm_time(3, "recursive", 0.00123) 
        close_db()

