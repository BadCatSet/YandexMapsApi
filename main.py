import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
import requests


class MainWindow(QMainWindow):
    g_map: QLabel

    def __init__(self):
        super().__init__()
        uic.loadUi('main_window.ui')
        self.zoom = 5
        self.delta_press = 0.00001
        self.lantitude = 90

    def get_map(self):
        response = requests.get('https://static-maps.yandex.ru/1.x/', params={'z': self.z})


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec())
