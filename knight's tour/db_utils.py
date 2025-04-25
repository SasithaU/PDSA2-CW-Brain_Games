# import mysql.connector

# def save_winner_to_db(name, move_count):
#     try:
#         conn = mysql.connector.connect(
#             host="localhost",
#             user="root",
#             password="badagediya",
#             database="knights_tour_game"
#         )
#         cursor = conn.cursor()
#         cursor.execute("INSERT INTO winners (name, move_count) VALUES (%s, %s)", (name, move_count))
#         conn.commit()
#         cursor.close()
#         conn.close()
#         print("Data inserted successfully.")
#     except Exception as e:
#         print("Error saving to DB:", e)




# import mysql.connector
# import json

# def save_winner_to_db(name,move_count path):
#     try:
#         conn = mysql.connector.connect(
#             host="localhost",
#             user="root",
#             password="badagediya",
#             database="knights_tour_game"
#         )
#         cursor = conn.cursor()

#         # Convert path list to JSON string for storage
#         path_str = json.dumps(path)

#         cursor.execute(
#             "INSERT INTO winners (name, path) VALUES (%s, %s)",
#             (name, path_str)
#         )
#         conn.commit()
#         cursor.close()
#         conn.close()
#         print("Data inserted successfully.")
#     except Exception as e:
#         print("Error saving to DB:", e)




import mysql.connector
import json

def save_winner_to_db(name, move_count, path):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="badagediya",
            database="knights_tour_game"
        )
        cursor = conn.cursor()

        query = "INSERT INTO winners (name, move_count, path) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, move_count, json.dumps(path)))  # <-- convert path to JSON string

        conn.commit()
        cursor.close()
        conn.close()
        print("Winner saved successfully.")
    except mysql.connector.Error as err:
        print(f"Error saving winner: {err}")
