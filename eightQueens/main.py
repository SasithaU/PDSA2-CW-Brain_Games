# main.py
from utils.save_sequential import save_sequential_results
from utils.save_threaded import save_threaded_results
from utils.save_time import record_timing
from utils.common_solution import insert_common_solutions
from ui.main_menu_ui import run_main_menu


def main():
    try:
        print("\n🚀 Running Sequential Solver...")
        sequential_time = save_sequential_results()

        print("\n🚀 Running Threaded Solver...")
        threaded_time = save_threaded_results()

        if sequential_time < threaded_time:
            print("\n✅ The Sequential Solver was faster than Threaded Solver.")
        elif threaded_time < sequential_time:
            print("\n✅ The Threaded Solver was faster Sequential Solver.")
        else:
            print("⏳ Both solvers took the same amount of time.")


        print("\n🔁 Inserting Common Solutions into 'solutions' Table...")
        insert_common_solutions()

        run_main_menu()
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")

if __name__ == "__main__":
    main()