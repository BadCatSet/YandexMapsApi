import sys
from io import BytesIO

import requests
from PIL import Image
from PyQt5 import Qt, uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow


class MainWindow(QMainWindow):
    g_map: QLabel

    def __init__(self):
        super().__init__()
        uic.loadUi('main_window.ui')
        self.zoom = 5
        self.delta = 0.00001
        self.lantitude = 90
        self.ll = '37.677751,55.757718'
        self.map_params = {
            "ll": self.ll,
            "spn": f'{self.delta},{self.delta}',
            "l": "map"
        }
        self.initUI()
        self.get_map()

    def initUI(self):
        self.setGeometry(100, 100, *(600, 400))
        self.setWindowTitle('Отображение карты')

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            if self.zoom != 16:
                self.zoom += 1
        if event.key() == Qt.Key_PageDown:
            if self.zoom != 0:
                self.zoom -= 1

    def get_map(self):
        response = requests.get('https://static-maps.yandex.ru/1.x/',
                                params=self.map_params)

        self.pixmap = QPixmap(Image.open(BytesIO(response.content)))
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec())
