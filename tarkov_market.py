import sys
import sqlite3
import os
from PyQt5.QtWidgets import (QApplication, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QLineEdit, QWidget, QHBoxLayout, QSplitter, QSpacerItem, QSizePolicy, QTextBrowser)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDesktopServices, QPalette, QColor

# Get the directory of the running script
script_dir = os.path.dirname(os.path.realpath(__file__))

# Define the database path
DATABASE_FILE = os.path.join(script_dir, 'tarkov_data.db')

def main():
    # Connect to SQLite database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    # Fetch all items from the database
    cursor.execute('SELECT * FROM items')
    rows = cursor.fetchall()

    # Create a dictionary to store the categories and their corresponding subcategories
    categories = {}

    # Iterate through the items and group them by category and subcategory
    for row in rows:
        # Get the tags for the item
        tags = row[14].split(',')

        # Get the category and subcategory for the item
        if len(tags) == 1:
            category = tags[0].strip()
            subcategory = ''
        else:
            category = tags[0].strip()
            subcategory = tags[1].strip()
        
        # Format the category and subcategory names
        category = category.replace('_', ' ').title()
        subcategory = subcategory.replace('_', ' ').title()

        # Create a new category if it doesn't exist
        if category not in categories:
            categories[category] = {}

        # Add the item to the subcategory
        if subcategory not in categories[category]:
            categories[category][subcategory] = []
        categories[category][subcategory].append(row)

    def filter_items(text):
        if text == '':
            for i in range(tree_widget.topLevelItemCount()):
                category_item = tree_widget.topLevelItem(i)
                category_item.setHidden(False)
                category_item.setExpanded(False)
                for j in range(category_item.childCount()):
                    subcategory_item = category_item.child(j)
                    subcategory_item.setHidden(False)
                    subcategory_item.setExpanded(False)
                    for k in range(subcategory_item.childCount()):
                        item_item = subcategory_item.child(k)
                        item_item.setHidden(False)
        else:
            for i in range(tree_widget.topLevelItemCount()):
                category_item = tree_widget.topLevelItem(i)
                category_item.setHidden(False)
                visible_subcategories = 0
                visible_items = 0

                if category_item.text(0) != 'Barter':
                    for j in range(category_item.childCount()):
                        subcategory_item = category_item.child(j)
                        subcategory_visible_items = 0

                        for k in range(subcategory_item.childCount()):
                            item_item = subcategory_item.child(k)
                            if text.lower() in item_item.text(0).lower():
                                item_item.setHidden(False)
                                subcategory_visible_items += 1
                                visible_items += 1
                            else:
                                item_item.setHidden(True)

                        subcategory_item.setHidden(subcategory_visible_items == 0)
                        if subcategory_visible_items > 0:
                            visible_subcategories += 1
                            subcategory_item.setExpanded(True)
                        else:
                            subcategory_item.setExpanded(False)

                    category_item.setHidden(visible_subcategories == 0)
                    if visible_subcategories > 0:
                        category_item.setExpanded(True)
                    else:
                        category_item.setExpanded(False)
                else:  # If 'Barter', handle items directly under the category
                    for j in range(category_item.childCount()):
                        item_item = category_item.child(j)
                        if text.lower() in item_item.text(0).lower():
                            item_item.setHidden(False)
                            visible_items += 1
                        else:
                            item_item.setHidden(True)

                    category_item.setHidden(visible_items == 0)
                    if visible_items > 0:
                        category_item.setExpanded(True)
                    else:
                        category_item.setExpanded(False)


    # Create the main window and layout
    app = QApplication(sys.argv)
    window = QWidget()
    layout = QVBoxLayout()
    window.setWindowTitle("Tarkov Market App")

    # Create a dark palette
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(40, 40, 40))
    palette.setColor(QPalette.AlternateBase, QColor(50, 50, 50))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)

    # Set the palette
    app.setPalette(palette)

    # Create the search input field
    search_input = QLineEdit()
    search_input.setPlaceholderText("Search items...")
    search_input.textChanged.connect(filter_items)
    search_input.setStyleSheet("""
        background-color: #353535;
        color: #ffffff;
    """)

    # Create a QHBoxLayout for search input and spacer
    search_layout = QHBoxLayout()

    # Add the search_input to the search_layout
    search_layout.addWidget(search_input)

    # Add a spacer to search_layout to push the search_input to the left
    spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
    search_layout.addSpacerItem(spacer)

    # Add the search_layout to the main layout
    layout.addLayout(search_layout)

    # Create the tree widget
    tree_widget = QTreeWidget()
    tree_widget.setHeaderLabels(['Items'])
    tree_widget.setHeaderHidden(True)

    # Add the items to the tree widget
    for category, subcategories in categories.items():
        # Create the category item
        category_item = QTreeWidgetItem(tree_widget, [category])
        category_item.setExpanded(False)

        for subcategory, items in subcategories.items():
            if subcategory and category != 'Barter':  # Only create a subcategory if it's not an empty string and not 'Barter'
                # Create the subcategory item
                subcategory_item = QTreeWidgetItem(category_item, [subcategory])
                subcategory_item.setExpanded(False)

                # Add the items to the subcategory
                for item in items:
                    item_item = QTreeWidgetItem(subcategory_item, [item[1]])
                    item_item.setData(0, Qt.UserRole, item)  # Store the whole item as data

            else:  # If subcategory is an empty string or the category is 'Barter', add items directly under the category
                for item in items:
                    item_item = QTreeWidgetItem(category_item, [item[1]])
                    item_item.setData(0, Qt.UserRole, item)  # Store the whole item as data

    # Commit changes and close database connection
    conn.commit()
    conn.close()

    # Create a QTextBrowser to display the item information
    item_info_browser = QTextBrowser()
    item_info_browser.setOpenLinks(False)  # Disable default link handling

    def link_clicked(url):
        QDesktopServices.openUrl(url)

    item_info_browser.anchorClicked.connect(link_clicked)

    def on_item_clicked(item, column):
        # Get the data for the clicked item
        item_data = item.data(0, Qt.UserRole)

        # Check if the item has data before trying to access it
        if item_data is not None:
            item_info = f"""
            <center>
            <p><strong>Name:</strong> {item_data[1]}</p>
            <p><strong>Short Name:</strong> {item_data[8]}</p>
            <p><strong>Currency:</strong> {item_data[7]}</p>
            <p><strong>Price:</strong> {item_data[2]}</p>
            <p><strong>Trader:</strong> {item_data[5]}</p>
            <p><strong>Buy Back Price:</strong> {item_data[6]}</p>
            <p><strong>Slots:</strong> {item_data[9]}</p>
            <p><strong>Avg 24h Price:</strong> {item_data[3]}</p>
            <p><strong>24h Price Diff:</strong> {item_data[12]}</p>
            <p><strong>Avg 7 days Price:</strong> {item_data[4]}</p>
            <p><strong>7d Price Diff:</strong> {item_data[13]}</p>
            <p><a href='{item_data[10]}'>Image</a></p>
            <p><a href='{item_data[11]}'>Wiki Link</a></p>
            </center>
            """
            item_info_browser.setHtml(item_info)
        else:
            item_info_browser.setHtml('')

    tree_widget.itemClicked.connect(on_item_clicked)

    # Add the tree widget and item info browser to a splitter
    splitter = QSplitter()
    splitter.addWidget(tree_widget)
    splitter.addWidget(item_info_browser)

    # Set the stretch factor so that both widgets share the available space equally
    splitter.setStretchFactor(0, 1)
    splitter.setStretchFactor(1, 1)

    # Add the splitter to the main layout
    layout.addWidget(splitter)

    # Set the main layout of the window
    window.setLayout(layout)

    # Set the initial size of the window
    window.resize(800, 400)

    # Show the window
    window.show()

    return app, window


