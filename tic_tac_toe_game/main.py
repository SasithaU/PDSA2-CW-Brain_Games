from ui import show_main_menu
from database import initialize_database

if __name__ == "__main__":
    initialize_database()  # Make sure database tables are created
    show_main_menu()       # Launch GUI
