from .connect import get_connection
import mysql.connector

def save_result(player, home, cities, route, algo, time, score, round_num):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
        INSERT INTO results (player_name, home_city, selected_cities, shortest_route, algorithm, time_taken, score, game_round)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (player, home, ",".join(cities), " -> ".join(route), algo, time, score, round_num))
        conn.commit()
    except mysql.connector.Error as err:
        print(f"❌ Database Error: {err}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


def get_leaderboard(limit=10):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
        SELECT player_name, algorithm, score, game_round, time_taken
        FROM results
        ORDER BY score DESC, time_taken ASC
        LIMIT %s
        """
        cursor.execute(query, (limit,))
        rows = cursor.fetchall()
        return rows
    except mysql.connector.Error as err:
        print(f"❌ Database Error: {err}")
        return []
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
