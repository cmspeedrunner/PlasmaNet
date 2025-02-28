import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QTextEdit
from PyQt5.QtGui import QFont, QTextCharFormat, QCursor
from PyQt5.QtCore import Qt, QPoint
import re
import client as pttp

class BrowserWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ion Browser")
        self.resize(1920, 1080)
        self.history = ["pttp://main.com/main.pst"]  # Store visited URLs
        self.history_index = 0

        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("Enter URL")
        self.url_input.setText("pttp://main.com/main.pst")
        self.url_input.setFixedHeight(45)

        self.back_button = QPushButton("←", self)
        self.forward_button = QPushButton("→", self)
        self.go_button = QPushButton("Go", self)

        self.page_label = QTextEdit()
        self.page_label.setReadOnly(True)
        cursor = self.page_label.textCursor()
        self.page_label.setStyleSheet("""
            background-color: white;
            border: 2px solid #ccc;
            padding: 50px;
            font-size: 22px;
        """)
        self.page_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        # Set larger fonts
        font_large = QFont("Arial", 24)
        font_medium = QFont("Arial", 15)

        self.url_input.setFont(font_medium)
        self.page_label.setFont(font_large)

        # Set button sizes
        button_size = "padding: 15px 30px; font-size: 20px; border-radius: 10px;"

        self.back_button.setStyleSheet(f"background-color: #E0E0E0; {button_size}")
        self.forward_button.setStyleSheet(f"background-color: #E0E0E0; {button_size}")
        self.go_button.setStyleSheet(f"background-color: #E0E0E0; {button_size}")

        self.back_button.setFixedSize(80, 60)
        self.forward_button.setFixedSize(80, 60)
        self.go_button.setFixedSize(100, 60)
        self.url_input.setFixedHeight(45)

        top_layout = QHBoxLayout()
        top_layout.setSpacing(10)
        top_layout.addWidget(self.back_button)
        top_layout.addWidget(self.forward_button)
        top_layout.addWidget(self.url_input, stretch=1)
        top_layout.addWidget(self.go_button)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.page_label, stretch=1)

        self.setLayout(main_layout)

        self.back_button.clicked.connect(self.on_back_click)
        self.forward_button.clicked.connect(self.on_forward_click)
        self.go_button.clicked.connect(self.on_go_click)
        self.url_input.returnPressed.connect(self.on_go_click)
        self.on_go_click()

    def on_back_click(self):
        if self.history_index > 0:
            self.history_index -= 1
            self.load_page(self.history[self.history_index])
            self.url_input.setText(self.history[self.history_index])

    def on_forward_click(self):
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.load_page(self.history[self.history_index])
            self.url_input.setText(self.history[self.history_index])

    def on_go_click(self):
        url = self.url_input.text()
        if url.strip() != "":
            if self.history_index < len(self.history) - 1:
                self.history = self.history[:self.history_index + 1]
            self.history.append(url)
            self.history_index = len(self.history) - 1
            self.load_page(url)

    def load_page(self, url):
        def insert_clickable_link(text_edit, text, linkto, formatval):
            cursor = text_edit.textCursor()

            formatval.setFontUnderline(True)
            formatval.setForeground(Qt.blue)

            start_pos = cursor.position()
            cursor.insertText(text, formatval)
            end_pos = cursor.position()
            formatval.setFontUnderline(False)
            formatval.setForeground(Qt.black)

            if not hasattr(text_edit, "links"):
                text_edit.links = {}
            text_edit.links[(start_pos, end_pos)] = linkto

            def handle_click(event):
                pos = text_edit.cursorForPosition(event.pos()).position()
                for (start, end), link in text_edit.links.items():
                    if start <= pos <= end:
                        self.url_input.setText(link)
                        self.on_go_click()
                        return

            text_edit.mouseReleaseEvent = handle_click

        self.page_label.clear()
        self.page_label.setStyleSheet("""
            background-color: white;
            border: 2px solid #ccc;
            padding: 50px;
            font-size: 22px;
        """)
        self.page_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        if url.startswith("pttp://"):
            url = url.split("pttp://")[1]
        else:
            pass
        url = url.strip()
        if "/" not in url or url.endswith("/"):
            domain = url
            content = pttp.pttpGET(domain)
            if "index.pst" in content:
                page = "index.pst"
                content = pttp.pttpGET(domain, page)
        else:
            domain = url.split("/")[0].strip()
            page = url.split("/")[1].strip()
            content = pttp.pttpGET(domain, page)

        content = content.removeprefix("PTTP/1.0 200 OK").strip()
        if content.strip().startswith("@"):
            redirect = content.strip().removeprefix("@").strip()
            content = pttp.pttpGET(domain, redirect)
            if url.endswith("/"):
                self.url_input.setText("pttp://" + domain + redirect)
            else:
                self.url_input.setText("pttp://" + domain + "/" + redirect)
        if content.startswith("PTTP/1.0 404 Not Found"):
            lines = ["[s=50][u][center][font=Ariel]", "line>Error 404: Not Found<", "[s=25][/u]", "line>Page does not exist or was removed<"]
        else:
            content = content.removeprefix("PTTP/1.0 200 OK").strip()
            lines = content.splitlines()
        formatted = False

        for i, line in enumerate(lines):
            if "<" not in line:
                formatted = True
                formatval = QTextCharFormat()
                formatval.setFontPointSize(16)

                if "[b" in line:
                    weight = line.split("[b")[1].split("]")[0].strip().removeprefix("=")
                    formatval.setFontWeight(int(weight))

                if "[s" in line:
                    size = line.split("[s")[1].split("]")[0].strip().removeprefix("=")
                    formatval.setFontPointSize(float(size))
                if "[u]" in line:
                    formatval.setFontUnderline(True)
                if "[i]" in line:
                    formatval.setFontItalic(True)
                if "[center]" in line:
                    self.page_label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
                if "[right]" in line:
                    self.page_label.setAlignment(Qt.AlignTop | Qt.AlignRight)

                if "[/b]" in line:
                    formatval.setFontWeight(0)
                if "[/u]" in line:
                    formatval.setFontUnderline(False)
                if "[/i]" in line:
                    formatval.setFontItalic(False)

                if "[left]" in line:
                    self.page_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
                if "[font" in line:
                    font = line.split("[font")[1].split("]")[0].strip().removeprefix("=")
                    formatval.setFontFamily(font)

            else:
                if line.startswith("line>"):
                    cursor = self.page_label.textCursor()
                    value = line.removeprefix("line>").removesuffix("<") + "\n"
                    if formatted:
                        cursor.insertText(value, formatval)
                    else:
                        formatval = QTextCharFormat()
                        cursor.insertText(value, formatval)
                if line.startswith("text>"):
                    cursor = self.page_label.textCursor()
                    value = line.removeprefix("text>").removesuffix("<")
                    if formatted:
                        cursor.insertText(value, formatval)
                    else:
                        formatval = QTextCharFormat()
                        cursor.insertText(value, formatval)

                elif line.startswith("link<"):
                    cursor = self.page_label.textCursor()
                    linkto = line.split("link<")[1].split(">")[0].strip()
                    text = line.split("link<")[1].split(">")[1].strip().removesuffix("<")
                    if "pttp://" in linkto:
                        pass
                    elif "pttp://" not in linkto:
                        linkto = "pttp://" + linkto

                    insert_clickable_link(self.page_label, text, linkto, formatval)

        # Override mouseMoveEvent to change cursor shape
        def mouseMoveEvent(event):
            pos = self.page_label.cursorForPosition(event.pos()).position()
            for (start, end), link in self.page_label.links.items():
                if start <= pos <= end:
                    self.page_label.viewport().setCursor(QCursor(Qt.PointingHandCursor))
                    return
            self.page_label.viewport().setCursor(QCursor(Qt.IBeamCursor))

        self.page_label.mouseMoveEvent = mouseMoveEvent

# Main execution
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BrowserWindow()
    window.show()

    sys.exit(app.exec_())