# items_db.py
import sqlite3
import os
import pandas as pd
import utils # <-- IMPORT UTILS

# Define the database path within the user's data directory
USER_DATA_DIR = utils.get_user_data_dir() # <-- GET USER DATA DIR
DATABASE_FILE = os.path.join(USER_DATA_DIR, 'tarkov_data.db') # <-- JOIN PATH
print(f"Database file path set to: {DATABASE_FILE}")

# Get the directory of the running script (Optional: keep if needed elsewhere)
# script_dir = os.path.dirname(os.path.realpath(__file__))

def create_or_update_database():
    print("Updating database from Google Sheet...")
    # Check if directory exists, create if not (utils should handle this, but belt-and-suspenders)
    db_dir = os.path.dirname(DATABASE_FILE)
    if not os.path.exists(db_dir):
        try:
            os.makedirs(db_dir, exist_ok=True)
            print(f"Created database directory: {db_dir}")
        except OSError as e:
            print(f"Error creating database directory '{db_dir}': {e}. Database may fail to save.")

    # Delete the SQLite database file if it exists (Optional: You might want an update strategy instead)
    if os.path.exists(DATABASE_FILE):
        print(f"Removing existing database: {DATABASE_FILE}")
        try:
            os.remove(DATABASE_FILE)
        except OSError as e:
            print(f"Error removing existing database file: {e}")
            # Decide if you want to proceed or exit if removal fails

    conn = None # Initialize conn to None
    try:
        # Create a new SQLite database connection
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        print(f"Database connection established: {DATABASE_FILE}")

        # Create items table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            uid TEXT PRIMARY KEY,
            name TEXT,
            price REAL,
            avg24hPrice REAL,
            avg7daysPrice REAL,
            trader TEXT,
            buyBackPrice REAL,
            currency TEXT,
            shortName TEXT,
            slots TEXT,
            imgBig TEXT,
            wikiLink TEXT,
            diff24h REAL,
            diff7days REAL,
            tags TEXT
        )
        ''')
        print("Table 'items' ensured.")

        # Load data from Google sheet published as CSV
        url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQX3ioboWlpSvL3tdE7jxUs5z0Pgiq1BUodhW4petHvs_HtL8PszVkB8c-0WmoSHqc3nE9l9LaNj3cI/pub?output=csv'
        print(f"Loading data from URL: {url}")
        data = pd.read_csv(url, skiprows=1)

        # Data Cleaning (Ensure correct types and handle NaNs)
        numeric_cols = [2, 3, 4, 6, 12, 13] # Indices for price, avg prices, buyback, diffs
        for col_idx in numeric_cols:
             if col_idx < len(data.columns):
                # Convert to numeric, coercing errors to NaN, then fill NaN with 0.0
                data.iloc[:, col_idx] = pd.to_numeric(data.iloc[:, col_idx], errors='coerce').fillna(0.0)

        string_cols = [0, 1, 5, 7, 8, 9, 10, 11, 14] # Indices for uid, name, trader, etc.
        for col_idx in string_cols:
            if col_idx < len(data.columns):
                # Fill NaN/None in string columns with empty string ''
                data.iloc[:, col_idx] = data.iloc[:, col_idx].fillna('')

        rows = data.values.tolist()
        print(f"Loaded {len(rows)} rows from Google Sheet.")

        # Insert data into SQLite database
        count = 0
        for i, row in enumerate(rows, start=1):
            # Ensure row has enough elements, providing defaults if not
            uid = row[0] if len(row) > 0 and row[0] else f'missing_uid_{i}' # Use default if UID is empty
            name = row[1] if len(row) > 1 else 'N/A'
            price = row[2] if len(row) > 2 else 0.0
            avg24hPrice = row[3] if len(row) > 3 else 0.0
            avg7daysPrice = row[4] if len(row) > 4 else 0.0
            trader = row[5] if len(row) > 5 else 'N/A'
            buyBackPrice = row[6] if len(row) > 6 else 0.0
            currency = row[7] if len(row) > 7 else 'N/A'
            shortName = row[8] if len(row) > 8 else 'N/A'
            slots = row[9] if len(row) > 9 else 'N/A'
            imgBig = row[10] if len(row) > 10 else ''
            wikiLink = row[11] if len(row) > 11 else ''
            diff24h = row[12] if len(row) > 12 else 0.0
            diff7days = row[13] if len(row) > 13 else 0.0
            tags = row[14] if len(row) > 14 else ''

            try:
                cursor.execute('''
                INSERT OR REPLACE INTO items (
                    uid, name, price, avg24hPrice, avg7daysPrice, trader, buyBackPrice, currency,
                    shortName, slots, imgBig, wikiLink, diff24h, diff7days, tags
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    str(uid), str(name), float(price), float(avg24hPrice), float(avg7daysPrice),
                    str(trader), float(buyBackPrice), str(currency), str(shortName), str(slots),
                    str(imgBig), str(wikiLink), float(diff24h), float(diff7days), str(tags)
                ))
                count += 1
            except sqlite3.Error as e:
                print(f"Database Error inserting row {i+1} (UID: {uid}): {e}")
            except Exception as e:
                 print(f"General Error processing row {i+1} (UID: {uid}): {e}")

        # Commit changes
        conn.commit()
        print(f"Successfully inserted/replaced {count} items into the database.")

    except pd.errors.EmptyDataError:
        print(f"Error: Could not load data from the URL '{url}'. It might be empty, invalid, or inaccessible.")
    except sqlite3.Error as e:
        print(f"A database error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during database update: {e}")
    finally:
        if conn:
            conn.close()
            print("Database connection closed.")

def fetch_all_items():
    """Fetches all items from the database."""
    if not os.path.exists(DATABASE_FILE):
        print("Database file not found. Running update first.")
        create_or_update_database() # Attempt to create it

    # Check again after attempting creation
    if not os.path.exists(DATABASE_FILE):
        print(f"Database creation failed or file still not found at {DATABASE_FILE}. Cannot fetch items.")
        return []

    conn = None # Initialize conn
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        print(f"Fetching items from: {DATABASE_FILE}")
        cursor.execute('SELECT * FROM items ORDER BY name ASC')
        rows = cursor.fetchall()
        print(f"Fetched {len(rows)} items.")
        return rows
    except sqlite3.Error as e:
        print(f"Error fetching items from database '{DATABASE_FILE}': {e}")
        return []
    except Exception as e:
        print(f"Unexpected error fetching items: {e}")
        return []
    finally:
        if conn:
            conn.close()
            # print("Fetch connection closed.") # Optional: less verbose

if __name__ == "__main__":
    # Example of running the update directly
    print("Running database update directly...")
    create_or_update_database()
    print("Database update process finished.")
    # Example fetch
    # items = fetch_all_items()
    # if items:
    #     print(f"\nSuccessfully fetched {len(items)} items after update.")