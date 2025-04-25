import mysql.connector
import json
from db.connect import get_connection

def save_result(player, home, selected_cities, route, cost, bf_time, greedy_time, dp_time):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO tsp_results (player_name, home_city, selected_cities, shortest_route, route_cost,
                                      brute_force_time, greedy_time, dp_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            player,
            home,
            json.dumps(selected_cities),
            json.dumps(route),
            cost,
            bf_time,
            greedy_time,
            dp_time
        ))
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Error saving result: {err}")
    finally:
        cursor.close()
        conn.close()


def log_algorithm_times(player_name, round_number, brute_force_time, greedy_time, dp_time):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tsp_algorithm_times (
            player_name, round_number, brute_force_time, greedy_time, dp_time
        ) VALUES (%s, %s, %s, %s, %s)
    """, (player_name, round_number, brute_force_time, greedy_time, dp_time))
    conn.commit()
    cursor.close()
    conn.close()
