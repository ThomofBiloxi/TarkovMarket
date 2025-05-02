# main_app.py
import sys
import items_db           # Correct
import tarkov_market_ui   # Correct import for the UI file

def main():
    # 1. Update and fetch data from the database
    # items_db.create_or_update_database() # Uncomment if needed on start
    all_items = items_db.fetch_all_items()

    if not all_items:
        print("No items loaded from database. Exiting.")
        return

    print(f"Fetched {len(all_items)} items for the UI.")

    # 2. Run the UI using the function from tarkov_market_ui
    app, window = tarkov_market_ui.run_ui(all_items) # Correct function call

    # 3. Start the application event loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()