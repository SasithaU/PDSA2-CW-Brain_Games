import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",           # use your username
        password="Workwithme@123",   # use your password
        database="tsp_game"
    )
