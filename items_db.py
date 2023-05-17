import sqlite3
import os
import pandas as pd

# Get the directory of the running script
script_dir = os.path.dirname(os.path.realpath(__file__))

# Define the database path
DATABASE_FILE = os.path.join(script_dir, 'tarkov_data.db')

def main():
    # Delete the SQLite database file if it exists
    if os.path.exists(DATABASE_FILE):
        os.remove(DATABASE_FILE)

    # Create a new SQLite database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

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

    # Load data from Google sheet published as CSV
    url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQX3ioboWlpSvL3tdE7jxUs5z0Pgiq1BUodhW4petHvs_HtL8PszVkB8c-0WmoSHqc3nE9l9LaNj3cI/pub?output=csv'
    data = pd.read_csv(url, skiprows=1)
    rows = data.values.tolist()

    # Insert data into SQLite database
    for i, row in enumerate(rows, start=1):
        try:
            tags = row[14] if len(row) > 14 else ''

            cursor.execute('''
            INSERT OR REPLACE INTO items (
                uid, name, price, avg24hPrice, avg7daysPrice, trader, buyBackPrice, currency,
                shortName, slots, imgBig, wikiLink, diff24h, diff7days, tags
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7],
                row[8], row[9], row[10], row[11], row[12], row[13], tags
            ))
        except Exception as e:
            print(f"Error on row {i+2}: {e}")

    # Commit changes and close database connection
    conn.commit()
    conn.close()
