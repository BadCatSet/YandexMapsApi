import sys

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QMainWindow
import requests


class MainWindow(QMainWindow):
    g_map: QLabel
    g_search: QLineEdit
    press_delta = 5

    def __init__(self):
        super().__init__()
        uic.loadUi('main_window.ui', self)

        self.map_zoom = 5
        self.map_ll = [37.977751, 55.757718]
        self.map_l = 'map'
        self.map_key = ''

        self.g_search.returnPressed.connect(self.search)

        self.refresh_map()

    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key_PageUp:
            if self.map_zoom < 17:
                self.map_zoom += 1
        elif key == Qt.Key_PageDown:
            if self.map_zoom > 0:
                self.map_zoom -= 1

        elif key == Qt.Key_Escape:
            self.g_map.setFocus()

        elif key == Qt.Key_Right:
            self.map_ll[0] += self.press_delta
            if self.map_ll[0] > 180:
                self.map_ll[0] = self.map_ll[0] - 360
        elif key == Qt.Key_Left:
            self.map_ll[0] -= self.press_delta
            if self.map_ll[0] < 0:
                self.map_ll[0] = self.map_ll[0] + 360
        elif key == Qt.Key_Up:
            if self.map_ll[1] + self.press_delta < 90:
                self.map_ll[1] += self.press_delta
        elif key == Qt.Key_Down:
            if self.map_ll[1] - self.press_delta > -90:
                self.map_ll[1] -= self.press_delta
        else:
            return

        self.refresh_map()

    def refresh_map(self):
        map_params = {
            "ll": f'{self.map_ll[0]},{self.map_ll[1]}',
            "l": self.map_l,
            'z': self.map_zoom,
        }
        response = requests.get('https://static-maps.yandex.ru/1.x/', params=map_params)
        if not response:
            print('error: could not get map')
            return
        with open('tmp.png', mode='wb') as tmp:
            tmp.write(response.content)

        pixmap = QPixmap()
        pixmap.load('tmp.png')

        self.g_map.setPixmap(pixmap)

    def search(self):
        print(geo_locate(self.g_search.text()))


def geo_locate(name):
    params = {
        'apikey': '40d1649f-0493-4b70-98ba-98533de7710b',
        'geocode': name,
        'format': 'json'
    }
    response = requests.get('http://geocode-maps.yandex.ru/1.x/', params=params)
    if not response:
        print(f'error: could not get geo_locate object {name}')
        return -1, -1
    geo_objects = response.json()['response']["GeoObjectCollection"]["featureMember"]
    if not geo_objects:
        print('error: could not get geo_objects')
        return -1, -1
    return geo_objects[0]["GeoObject"]["Point"]["pos"]


def clip(v, _min, _max):
    if v < _min:
        return _min
    if v > _max:
        return _max
    return v


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec())
