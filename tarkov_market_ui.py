# tarkov_market_ui.py
import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QLineEdit,
    QWidget, QHBoxLayout, QSplitter, QLabel, QSizePolicy, QFormLayout,
    QSpacerItem, QScrollArea, QFrame, QApplication, QStyle, QTreeWidgetItemIterator
)
from PyQt5.QtCore import Qt, QUrl, pyqtSignal, QByteArray, QBuffer, QIODevice
from PyQt5.QtGui import QDesktopServices, QPalette, QColor, QPixmap, QIcon, QFont
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply

import utils # <-- IMPORT UTILS

# Define paths relative to the application root (where assets will be bundled)
PLACEHOLDER_IMAGE_PATH = utils.resource_path("placeholder.png") # <-- USE RESOURCE PATH
ERROR_IMAGE_PATH = utils.resource_path("error.png") # <-- USE RESOURCE PATH
print(f"Placeholder image path: {PLACEHOLDER_IMAGE_PATH}")
print(f"Error image path: {ERROR_IMAGE_PATH}")


# --- (Placeholder file creation code using Pillow - Primarily for standalone testing) ---
def _create_assets_if_needed():
    placeholder_exists = os.path.exists(PLACEHOLDER_IMAGE_PATH)
    error_exists = os.path.exists(ERROR_IMAGE_PATH)

    if placeholder_exists and error_exists:
        # print("Asset images already exist.") # Less verbose
        return # Both files exist, do nothing

    print("Attempting to create missing asset images using Pillow...")
    try:
        from PIL import Image, ImageDraw
        print("Pillow library found.")

        # Create Placeholder if missing
        if not placeholder_exists:
            try:
                print(f"Creating '{PLACEHOLDER_IMAGE_PATH}'...")
                img_placeholder = Image.new('RGB', (128, 128), color=(128, 128, 128))
                img_placeholder.save(PLACEHOLDER_IMAGE_PATH)
                print("  Placeholder created successfully.")
            except Exception as e_placeholder:
                print(f"  Error creating placeholder: {e_placeholder}")

        # Create Error Icon if missing
        if not error_exists:
            try:
                print(f"Creating '{ERROR_IMAGE_PATH}'...")
                img_error = Image.new('RGB', (128, 128), color=(128, 128, 128))
                draw = ImageDraw.Draw(img_error)
                draw.line([(0, 0), (127, 127)], fill=(255, 0, 0), width=8)
                draw.line([(127, 0), (0, 127)], fill=(255, 0, 0), width=8)
                img_error.save(ERROR_IMAGE_PATH)
                print("  Error icon created successfully.")
            except Exception as e_error:
                print(f"  Error creating error icon: {e_error}")

    except ImportError:
        print("Warning: Pillow library not found. Cannot automatically create missing asset images.")
        print("         Please ensure placeholder.png and error.png exist in the application directory or bundle.")
    except Exception as e_general:
        print(f"An unexpected error occurred during asset creation: {e_general}")

# Run asset creation check when module loads (or specifically when run_ui is called)
# _create_assets_if_needed() # Might run too early if called here, better in run_ui or main_app

# --- (create_dark_palette - Unchanged) ---
def create_dark_palette():
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(40, 40, 40))
    palette.setColor(QPalette.AlternateBase, QColor(50, 50, 50))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(60, 60, 60))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.white)
    palette.setColor(QPalette.Disabled, QPalette.Text, QColor(127, 127, 127))
    palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(127, 127, 127))
    return palette

# --- (create_separator - Unchanged) ---
def create_separator():
    separator = QFrame()
    separator.setFrameShape(QFrame.HLine)
    separator.setFrameShadow(QFrame.Sunken)
    separator.setStyleSheet("border: 1px solid #444;")
    return separator

# --- (ItemDetailsWidget class - Unchanged, uses the paths defined above) ---
class ItemDetailsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.network_manager = QNetworkAccessManager(self)
        self.network_manager.finished.connect(self.on_image_loaded)
        self.current_image_reply = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        container_widget = QWidget()
        self.details_layout = QVBoxLayout(container_widget)
        self.details_layout.setSpacing(10)
        self.image_label = QLabel("No item selected.")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(128, 128)
        self.image_label.setMaximumSize(256, 256)
        self.image_label.setScaledContents(False)
        self.image_label.setStyleSheet("border: 1px solid #444; background-color: #282828; border-radius: 4px;")
        self.details_layout.addWidget(self.image_label, alignment=Qt.AlignCenter)
        self.details_layout.addSpacing(15)
        self.form_layout = QFormLayout()
        self.form_layout.setContentsMargins(0, 0, 0, 0)
        self.form_layout.setLabelAlignment(Qt.AlignLeft)
        self.form_layout.setHorizontalSpacing(15)
        self.form_layout.setVerticalSpacing(8)
        self.name_label = self._add_row("Name:")
        name_font = self.name_label.font()
        name_font.setPointSize(name_font.pointSize() + 1)
        name_font.setBold(True)
        self.name_label.setFont(name_font)
        self.short_name_label = self._add_row("Short Name:")
        self.slots_label = self._add_row("Slots:")
        self.form_layout.addRow(create_separator())
        self.price_label = self._add_row("Price:")
        self.buyback_label = self._add_row("Buy Back:")
        self.trader_label = self._add_row("Trader:")
        self.form_layout.addRow(create_separator())
        self.avg24h_label = self._add_row("Avg 24h:")
        self.diff24h_label = self._add_row("Diff 24h:")
        self.avg7d_label = self._add_row("Avg 7d:")
        self.diff7d_label = self._add_row("Diff 7d:")
        self.form_layout.addRow(create_separator())
        self.wiki_link_label = self._add_row("Wiki:")
        self.details_layout.addLayout(self.form_layout)
        self.details_layout.addStretch()
        scroll_area.setWidget(container_widget)
        layout.addWidget(scroll_area)
        self.placeholder_pixmap = QPixmap(PLACEHOLDER_IMAGE_PATH).scaled(128, 128, Qt.KeepAspectRatio, Qt.SmoothTransformation) if os.path.exists(PLACEHOLDER_IMAGE_PATH) else None
        self.error_pixmap = QPixmap(ERROR_IMAGE_PATH).scaled(128, 128, Qt.KeepAspectRatio, Qt.SmoothTransformation) if os.path.exists(ERROR_IMAGE_PATH) else None

    def _add_row(self, label_text):
        label = QLabel(label_text)
        value_label = QLabel("-")
        value_label.setWordWrap(True)
        value_label.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.LinksAccessibleByMouse)
        self.form_layout.addRow(label, value_label)
        return value_label

    def format_price(self, value, currency="₽"):
        try:
            f_value = float(value) if value is not None else 0.0
            symbol = ""
            if currency and isinstance(currency, str):
                cur_upper = currency.upper()
                if cur_upper == 'RUB': symbol = " ₽"
                elif cur_upper == 'USD': symbol = " $"
                elif cur_upper == 'EUR': symbol = " €"
                else: symbol = f" {currency}"
            if abs(f_value) >= 1000 or symbol == " ₽": return f"{f_value:,.0f}{symbol}"
            else: return f"{f_value:,.2f}{symbol}"
        except (ValueError, TypeError): return str(value) if value is not None else "-"

    def format_diff(self, value):
        try:
            f_value = float(value) if value is not None else 0.0
            color = "white"
            sign = ""
            if f_value > 0.001: color = "#4CAF50"; sign = "+"
            elif f_value < -0.001: color = "#F44336"; sign = ""
            formatted_value = f"{f_value:.2f}"
            return f"<span style='color:{color};'>{sign}{formatted_value}%</span>"
        except (ValueError, TypeError): return str(value) if value is not None else "-"

    def update_details(self, item_data):
        if not item_data: self.clear_details(); return
        currency_code = item_data[7]
        self.name_label.setText(item_data[1] or "N/A")
        self.short_name_label.setText(item_data[8] or "N/A")
        self.slots_label.setText(str(item_data[9]) if item_data[9] is not None else "N/A")
        self.price_label.setText(self.format_price(item_data[2], currency_code))
        self.buyback_label.setText(self.format_price(item_data[6], currency_code))
        self.trader_label.setText(item_data[5] or "N/A")
        self.avg24h_label.setText(self.format_price(item_data[3], currency_code))
        self.diff24h_label.setText(self.format_diff(item_data[12]))
        self.avg7d_label.setText(self.format_price(item_data[4], currency_code))
        self.diff7d_label.setText(self.format_diff(item_data[13]))
        wiki_url = item_data[11]
        if wiki_url:
            link_color = QApplication.palette().color(QPalette.Link).name()
            link_text = "Open Wiki Page"
            self.wiki_link_label.setText(f"<a href='{wiki_url}' style='color: {link_color}; text-decoration: none;'>{link_text}</a>")
            self.wiki_link_label.setOpenExternalLinks(False)
            try: self.wiki_link_label.linkActivated.disconnect(self.open_link)
            except TypeError: pass
            self.wiki_link_label.linkActivated.connect(self.open_link)
        else:
            self.wiki_link_label.setText("N/A")
            try: self.wiki_link_label.linkActivated.disconnect(self.open_link)
            except TypeError: pass
        image_url = item_data[10]
        if image_url: self.load_image(image_url)
        else: self._set_placeholder_or_text("No image available")

    def load_image(self, url_string):
        if self.current_image_reply and self.current_image_reply.isRunning():
            self.current_image_reply.abort()
        url = QUrl(url_string)
        if not url.isValid() or url.scheme() not in ['http', 'https']:
            self._set_placeholder_or_text("Invalid image URL"); return
        self._set_placeholder_or_text("Loading image...")
        request = QNetworkRequest(url)
        request.setHeader(QNetworkRequest.UserAgentHeader, "TarkovMarketApp/1.0 (Python/PyQt5)")
        request.setAttribute(QNetworkRequest.FollowRedirectsAttribute, True)
        self.current_image_reply = self.network_manager.get(request)

    def on_image_loaded(self, reply):
        if reply != self.current_image_reply: reply.deleteLater(); return
        request_url = reply.request().url().toString()
        final_url = reply.url().toString()
        error = reply.error()
        if error == QNetworkReply.NoError:
            image_data = reply.readAll()
            pixmap = QPixmap()
            if image_data and pixmap.loadFromData(image_data):
                 scaled_pixmap = pixmap.scaled(self.image_label.maximumSize(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                 self.image_label.setPixmap(scaled_pixmap)
                 self.image_label.setAlignment(Qt.AlignCenter)
            else: self._set_placeholder_or_text("Failed to load image", use_error_icon=True)
        elif error == QNetworkReply.OperationCanceledError: pass
        else: self._set_placeholder_or_text(f"Error: {reply.errorString()}", use_error_icon=True)
        reply.deleteLater()
        self.current_image_reply = None

    def _set_placeholder_or_text(self, text, use_error_icon=False):
        icon_to_use = self.error_pixmap if use_error_icon else self.placeholder_pixmap
        if icon_to_use:
            self.image_label.setPixmap(icon_to_use)
            self.image_label.setToolTip(text)
        else: # Fallback if icons themselves failed to load
            self.image_label.setText(text if not use_error_icon else f"Error: {text}")
            self.image_label.setToolTip("")
        self.image_label.setAlignment(Qt.AlignCenter)

    def clear_details(self):
        self.name_label.setText("-"); self.short_name_label.setText("-")
        self.slots_label.setText("-"); self.price_label.setText("-")
        self.buyback_label.setText("-"); self.trader_label.setText("-")
        self.avg24h_label.setText("-"); self.diff24h_label.setText("-")
        self.avg7d_label.setText("-"); self.diff7d_label.setText("-")
        self.wiki_link_label.setText("-")
        try: self.wiki_link_label.linkActivated.disconnect(self.open_link)
        except TypeError: pass
        self._set_placeholder_or_text("No item selected")
        if self.current_image_reply and self.current_image_reply.isRunning():
            self.current_image_reply.abort()

    def open_link(self, url_string):
        url = QUrl(url_string)
        if url.isValid(): QDesktopServices.openUrl(url)
        else: print(f"Attempted to open invalid URL: {url_string}")

# --- (MainWindow class - Unchanged) ---
class MainWindow(QWidget):
    def __init__(self, items_data, parent=None):
        super().__init__(parent)
        self.items_data = items_data
        self.init_ui()
        self.populate_tree()

    def init_ui(self):
        self.setWindowTitle("Tarkov Market Info")
        self.setGeometry(100, 100, 1050, 720)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10); main_layout.setSpacing(6)
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search items...")
        self.search_input.textChanged.connect(self.filter_items)
        self.search_input.setClearButtonEnabled(True)
        self.search_input.setStyleSheet("QLineEdit{background-color:#353535;color:#ffffff;border:1px solid #555;border-radius:4px;padding:6px;font-size:14px}QLineEdit:focus{border:1px solid #2a82da}")
        search_layout.addWidget(self.search_input)
        main_layout.addLayout(search_layout)
        self.splitter = QSplitter(Qt.Horizontal)
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderHidden(True)
        self.tree_widget.itemClicked.connect(self.on_item_clicked)
        self.tree_widget.setStyleSheet("QTreeWidget{border:1px solid #444;border-radius:4px;background-color:#282828;font-size:13px}QTreeWidget::item{padding:5px 2px;border-radius:2px}QTreeWidget::item:hover{background-color:#3a3a3a}QTreeWidget::item:selected{background-color:#2a82da;color:#ffffff}QHeaderView::section{background-color:#353535;color:white;padding:4px;border:1px solid #555}QTreeWidget::branch:has-children:!has-siblings:closed,QTreeWidget::branch:closed:has-children:has-siblings{border-image:none;image:url(:/qt-project.org/styles/commonstyle/images/branch-closed-16.png)}QTreeWidget::branch:open:has-children:!has-siblings,QTreeWidget::branch:open:has-children:has-siblings{border-image:none;image:url(:/qt-project.org/styles/commonstyle/images/branch-open-16.png)}")
        self.folder_icon = QApplication.style().standardIcon(QStyle.SP_DirClosedIcon)
        self.item_icon = QIcon()
        self.splitter.addWidget(self.tree_widget)
        self.item_details_widget = ItemDetailsWidget()
        self.splitter.addWidget(self.item_details_widget)
        self.splitter.setSizes([320, 730])
        self.splitter.setCollapsible(0, False); self.splitter.setCollapsible(1, False)
        main_layout.addWidget(self.splitter)

    def process_tags(self, tags_string):
        if not tags_string or not isinstance(tags_string, str): return "Uncategorized", ""
        tags = [tag.strip() for tag in tags_string.split(',') if tag.strip()]
        if not tags: return "Uncategorized", ""
        category = tags[0].replace('_', ' ').title()
        subcategory = tags[1].replace('_', ' ').title() if len(tags) > 1 else ""
        return category, subcategory

    def populate_tree(self):
        self.tree_widget.clear(); categories = {}; uncategorized_items = []; item_count = 0
        for item_data in self.items_data:
            item_count += 1; tags = item_data[14]
            category_name, subcategory_name = self.process_tags(tags)
            if category_name == "Uncategorized": uncategorized_items.append(item_data); continue
            if category_name not in categories: categories[category_name] = {}
            if subcategory_name not in categories[category_name]: categories[category_name][subcategory_name] = []
            categories[category_name][subcategory_name].append(item_data)
        sorted_categories = sorted(categories.keys())
        for category_name in sorted_categories:
            category_item = QTreeWidgetItem(self.tree_widget, [category_name])
            category_item.setIcon(0, self.folder_icon); category_item.setData(0, Qt.UserRole, None)
            sorted_subcategories = sorted(categories[category_name].keys())
            for subcategory_name in sorted_subcategories:
                items_in_subcategory = categories[category_name][subcategory_name]
                items_in_subcategory.sort(key=lambda x: (x[1] or "").lower())
                if subcategory_name and category_name != 'Barter':
                    subcategory_item = QTreeWidgetItem(category_item, [subcategory_name])
                    subcategory_item.setIcon(0, self.folder_icon); subcategory_item.setData(0, Qt.UserRole, None)
                    for item_data in items_in_subcategory:
                        item_name = item_data[1] or "Unnamed Item"
                        item_node = QTreeWidgetItem(subcategory_item, [item_name])
                        item_node.setIcon(0, self.item_icon); item_node.setData(0, Qt.UserRole, item_data)
                else:
                    for item_data in items_in_subcategory:
                        item_name = item_data[1] or "Unnamed Item"
                        item_node = QTreeWidgetItem(category_item, [item_name])
                        item_node.setIcon(0, self.item_icon); item_node.setData(0, Qt.UserRole, item_data)
        if uncategorized_items:
            uncategorized_items.sort(key=lambda x: (x[1] or "").lower())
            category_item = QTreeWidgetItem(self.tree_widget, ["Uncategorized"])
            category_item.setIcon(0, self.folder_icon); category_item.setData(0, Qt.UserRole, None)
            for item_data in uncategorized_items:
                item_name = item_data[1] or "Unnamed Item"
                item_node = QTreeWidgetItem(category_item, [item_name])
                item_node.setIcon(0, self.item_icon); item_node.setData(0, Qt.UserRole, item_data)
        self.tree_widget.collapseAll()

    def filter_items(self, text):
        search_term = text.lower().strip(); visible_item_count = 0
        iterator = QTreeWidgetItemIterator(self.tree_widget, QTreeWidgetItemIterator.All)
        while iterator.value():
            item = iterator.value(); item_data = item.data(0, Qt.UserRole)
            if item_data is not None: # Item
                item_name = (item_data[1] or "").lower()
                matches = search_term in item_name
                item.setHidden(not matches)
                if matches:
                    visible_item_count += 1; parent = item.parent()
                    while parent: parent.setHidden(False); parent.setExpanded(True if search_term else False); parent = parent.parent()
            else: # Category/Subcategory
                 item.setHidden(True)
                 if not search_term: item.setHidden(False); item.setExpanded(False)
            iterator += 1
        if search_term:
            iterator = QTreeWidgetItemIterator(self.tree_widget, QTreeWidgetItemIterator.Reverse | QTreeWidgetItemIterator.All)
            while iterator.value():
                item = iterator.value()
                if item.data(0, Qt.UserRole) is None:
                    has_visible_child = any(not item.child(i).isHidden() for i in range(item.childCount()))
                    if not has_visible_child: item.setHidden(True); item.setExpanded(False)
                iterator += 1

    def on_item_clicked(self, item, column):
        item_data = item.data(0, Qt.UserRole)
        if item_data is not None: self.item_details_widget.update_details(item_data)
        # else: print(f"Category/Subcategory clicked: {item.text(0)}") # Optional

# --- (run_ui function - Unchanged) ---
def run_ui(items_data):
    # Run asset creation check when UI is about to start
    _create_assets_if_needed() # Ensure assets exist or are attempted to be created

    app = QApplication.instance();
    if not app: app = QApplication(sys.argv)
    app.setPalette(create_dark_palette())
    app.setStyleSheet("QToolTip { color: #ffffff; background-color: #1e1e1e; border: 1px solid #555; }")
    main_window = MainWindow(items_data)
    main_window.show()
    return app, main_window

# --- (Testing Block - Unchanged) ---
if __name__ == '__main__':
    print("Running tarkov_market_ui.py directly for testing.")
    _create_assets_if_needed() # Create assets when run directly too
    dummy_items = [
        ('uid1', 'Item Alpha', 100.0, 95.0, 110.0, 'Trader A', 50.0, 'RUB', 'Alpha', '1x1', 'https://via.placeholder.com/128/FF0000/FFFFFF?text=Item+A', 'http://wiki.example.com/Alpha', -5.0, 10.0, 'category_one,sub_a'),
        ('uid2', 'Item Beta', 20000.0, 19000.0, 21000.0, 'Trader B', 10000.0, 'RUB', 'Beta', '2x1', 'https://via.placeholder.com/128/00FF00/FFFFFF?text=Item+B', 'http://wiki.example.com/Beta', -5.0, 5.0, 'category_one,sub_b'),
        # Add more dummy data if needed
    ]
    app, window = run_ui(dummy_items)
    sys.exit(app.exec_())