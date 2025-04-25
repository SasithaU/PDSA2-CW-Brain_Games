# 🧭 Traveling Salesman Problem (TSP) Game 🎮🗺️

This project is an interactive and educational game built around the **Traveling Salesman Problem (TSP)** — a famous computer science optimization challenge. The goal is to help a salesman find the **shortest possible route** to visit a set of cities **once each** and return to the starting city.

---

## 🧩 Game Concept

  You are a traveling salesman, and your mission is to choose the shortest route that visits every city exactly once and returns to the home city.

### 📏 Rules:
      - You’ll be shown a list of cities and the distances between them.
      - Choose which cities to visit.
      - Try to manually solve the problem — or let the computer solve it!
      - Algorithms will show you the **optimal** route and distance.
      - Compare your answer with the best one!

---

## 🎯 Objectives

        - Teach players about optimization and shortest path algorithms.
        - Compare different algorithmic approaches:
          - Brute Force (💥 exhaustive search)
          - Greedy Algorithm (🍭 quick win, not always optimal)
          - Dynamic Programming (🧠 smart memory-based optimization)

---

## 🚀 Features

      - ✅ User-friendly **Tkinter GUI**
      - 🧠 Three algorithms implemented:
        - Brute Force
        - Greedy
        - Dynamic Programming
      - 💾 Stores game results in a **MySQL database**
      - 🌟 Allows manual play + algorithmic verification

---

## 🗂️ File Structure

        tsp_game/
        │
        ├── main.py                  # Entry point of the game
        ├── game/
        │   ├── __init__.py
        │   ├── ui.py                # Attractive user interface
        │   ├── logic.py             # TSP solving logic
        │   ├── utils.py             # Helpers like distance matrix generation
        │
        ├── db/
        │   ├── __init__.py
        │   ├── models.py            # MySQL table logic
        │   ├── connect.py           # DB connection setup
        │
        ├── tests/
        │   └── test_algorithms.py   # Unit tests for the algorithms
        ├── requirements.txt         # Python dependencies
        └── README.md                # Project description



---

## 🗄️ Database Setup

Ensure MySQL is installed and create a database with the following tables:

```sql
      CREATE DATABASE tsp_game;

        CREATE TABLE tsp_results (
        id INT AUTO_INCREMENT PRIMARY KEY,
        player_name VARCHAR(100) NOT NULL,
        home_city VARCHAR(100) NOT NULL,
        selected_cities TEXT NOT NULL,        
        shortest_route TEXT NOT NULL,         
        route_cost FLOAT NOT NULL,
        brute_force_time FLOAT,              
        greedy_time FLOAT,
        dp_time FLOAT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );



        CREATE TABLE IF NOT EXISTS tsp_algorithm_times (
        id INT AUTO_INCREMENT PRIMARY KEY,
        player_name VARCHAR(100) NOT NULL,
        round_number INT NOT NULL,
        brute_force_time FLOAT,
        greedy_time FLOAT,
        dp_time FLOAT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );

Update your db/connect.py with your database credentials:

        host = "your_host"
        user = "your_username"
        password = "your_password"
        database = "tsp_game"


🖥️ How to Run

      Activate virtual environment to install dependencies
        
              venv\Scripts\activate   

      Install required dependencies:

              pip install -r requirements.txt

                
      Run the game:

              python main.py

🧪 Testing
        To run unit tests on algorithms:
        
                pytest --rich --tb=short -v


📦 Requirements
      Python 3.11+
      MySQL Server
      mysql-connector-python
      tkinter
      rich (for improved terminal visuals)