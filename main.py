import items_db
import tarkov_market
import sys

def main():
    items_db.main()
    app, window = tarkov_market.main()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()