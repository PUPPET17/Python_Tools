import sys
import hashlib
import time
import random
import json
import urllib.parse
import http.client
import logging
import pyperclip
import keyboard
from PyQt5.QtWidgets import QScrollArea, QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QShortcut, QSlider, QMenuBar, QAction
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
import re

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TranslatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.first_time = 0
        self.initUI()
        self.load_config()
        self.start_global_hotkey_listener()

    def load_config(self):
        self.appid = "20240730002112250"
        self.secret_key = "lu4XOwBMJHDjLXUum_Pz"

    def baidu_translate(self, q, from_lang, to_lang):
        myurl = '/api/trans/vip/translate'
        salt = random.randint(32768, 65536)
        sign = self.appid + q + str(salt) + self.secret_key
        m1 = hashlib.md5()
        m1.update(sign.encode('utf-8'))
        sign = m1.hexdigest()
        myurl = (myurl + '?appid=' + self.appid + '&q=' + urllib.parse.quote(q) + '&from=' + from_lang + '&to=' + to_lang + '&salt=' + str(salt) + '&sign=' + sign)

        try:
            http_client = http.client.HTTPConnection('api.fanyi.baidu.com')
            http_client.request('GET', myurl)
            response = http_client.getresponse()
            json_response = response.read().decode('utf-8')
            result = json.loads(json_response)
            print(result)
            return result
        except Exception as e:
            logging.error(f"Translation error: {e}")
            return None
        finally:
            if http_client:
                http_client.close()

    def check_clipboard(self):
        clipboard_content = pyperclip.paste()
        text = re.sub(r' {3,}', ' ', clipboard_content)
        text = re.sub(r'\n+', ' ', text)
        formatted_content = text
        result = self.baidu_translate(formatted_content, 'auto', 'zh')
        if result:
            translation = result.get('trans_result', [{}])[0].get('dst', 'No translation found.')
            self.result_label.setText(translation)
        else:
            self.result_label.setText("Error during translation.")
    
    def initUI(self):
        self.setWindowTitle('Translator')
        self.setGeometry(6, 800, 500, 219)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        # Set up the main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.result_label = QLabel("Double-press Ctrl+C to translate")
        self.result_label.setFont(QFont('Helvetica', 12))
        self.result_label.setStyleSheet('background-color: #2C3E50; color: #ECF0F1; padding: 10px')
        self.result_label.setWordWrap(True)  # Enable word wrapping

        scroll_area = QScrollArea()
        scroll_area.setWidget(self.result_label)
        scroll_area.setWidgetResizable(True)

        self.layout.addWidget(scroll_area)
        
        # Create and configure the menu bar
        menubar = self.menuBar()
        settings_menu = menubar.addMenu('Settings')

        transparency_action = QAction('Transparency', self)
        transparency_action.triggered.connect(self.open_settings)
        settings_menu.addAction(transparency_action)

        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        settings_menu.addAction(exit_action)

        self.show()

    def start_global_hotkey_listener(self):
        # Start a thread to listen for global hotkeys
        keyboard.add_hotkey('ctrl+c', self.on_ctrl_c_double)

    def on_ctrl_c_double(self):
        current_time = time.time()
        logging.info(f"Ctrl+C pressed at {current_time}")
        if current_time - self.first_time < 0.5:
            self.check_clipboard() 
        self.first_time = current_time

    def open_settings(self):
        self.settings_window = QWidget()
        self.settings_window.setWindowTitle('Transparency Settings')
        self.settings_window.setStyleSheet('background-color: #2C3E50; color: #ECF0F1')

        layout = QVBoxLayout()
        self.settings_window.setLayout(layout)

        label = QLabel("Adjust Transparency:")
        label.setStyleSheet('color: #ECF0F1')
        layout.addWidget(label)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(20)
        self.slider.setMaximum(100)
        self.slider.setValue(int(self.windowOpacity() * 100))
        self.slider.setStyleSheet('background-color: #2C3E50; color: #ECF0F1')
        self.slider.valueChanged.connect(self.set_transparency)
        layout.addWidget(self.slider)

        self.settings_window.show()

    def set_transparency(self, value):
        self.setWindowOpacity(value / 100.0)

    def closeEvent(self, event):
        keyboard.unhook_all()  # Clean up global hotkeys
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TranslatorApp()
    sys.exit(app.exec_())
