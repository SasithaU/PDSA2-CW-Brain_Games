# utils/common_solution.py
from db.connection import get_connection

def insert_common_solutions():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT positions FROM sequential_solutions")
        sequential = set(row[0].strip() for row in cursor.fetchall())

        cursor.execute("SELECT positions FROM threaded_solutions")
        threaded = set(row[0].strip() for row in cursor.fetchall())

        common = sorted(sequential & threaded)
        inserted_count = 0

        if len(common) != 92:
            print(f"Warning: Expected 92 common solutions, but found {len(common)}.")
            return

        for idx, pos_str in enumerate(common, start=1):
            cursor.execute(
                "INSERT IGNORE INTO solutions (positions, is_found) VALUES (%s, %s)",
                (pos_str, 0)
            )
            if cursor.rowcount > 0:
                inserted_count += 1

        conn.commit()
        print(f"\n{inserted_count} new common solutions inserted into 'solutions' table.")

    except Exception as e:
        print("Error inserting common solutions:", e)

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
