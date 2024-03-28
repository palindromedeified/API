import os
import sys
from PyQt5 import uic
import requests
from PyQt5.QtGui import QPixmap, QKeyEvent
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.Qt import *
from fileui import Ui_MainWindow

SCREEN_SIZE = [600, 450]
pt = None


def get_coord(address):
    try:
        url = 'http://geocode-maps.yandex.ru/1.x/'
        params = {
            "apikey": '40d1649f-0493-4b70-98ba-98533de7710b',
            "geocode": address,
            "format": "json",
            'lang': 'ru_RU'
        }
        response = requests.get(url, params=params).json()
        # Получаем координаты центра объекта
        pos = response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"]
        res = list(map(float, pos.split()))
        return res
    except Exception:
        return None


class Example(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.press_delta = 1
        self.map_zoom = 5
        self.map_ll = [37.977751, 55.757718]
        self.lst = ['map', 'sat', 'sat,skl']
        self.index = 0
        self.map_l = self.lst[self.index]
        self.map_key = ''
        self.pushButton.clicked.connect(self.run)
        self.coords = None
        self.lineEdit.mousePressEvent = self.mousePressEvent
        self.getImage()

    def run(self):
        global pt
        self.coords = get_coord(self.lineEdit.text())
        if self.coords is not None:
            self.map_ll = self.coords
            pt = f'{self.coords[0]},{self.coords[1]}'
            self.getImage()
        self.lineEdit.clear()

    def getImage(self):
        map_request = 'https://static-maps.yandex.ru/1.x/'
        map_params = {
            "ll": ','.join(map(str, self.map_ll)),
            "l": self.map_l,
            'z': self.map_zoom,
        }
        if self.coords is not None:
            map_params['pt'] = f'{pt},pm2rdm'
        self.response = requests.get(map_request, params=map_params)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Отображение карты')
        # Изображение
        pixmap = QPixmap()
        pixmap.loadFromData(self.response.content)
        self.label.setPixmap(pixmap)

    def mousePressEvent(self, a0):
        pos = a0.pos()
        if 10 <= pos.x() <= 471 and 10 <= pos.y() <= 41:
            self.lineEdit.setEnabled(True)
            self.pushButton.setEnabled(True)
        else:
            self.lineEdit.setEnabled(False)
            self.pushButton.setEnabled(False)

    def keyPressEvent(self, event):
        key = event.key()
        key2 = event.text()
        if key == Qt.Key_Up:
            self.map_zoom += 1
        if key == Qt.Key_Down:
            self.map_zoom -= 1
        if key == Qt.Key_E or key2 == 'у':
            self.index = (self.index + 1) % 3
            self.map_l = self.lst[self.index]
        if key == Qt.Key_W or key2 == 'ц':
            self.map_ll[1] += self.press_delta / self.map_zoom
        if key == Qt.Key_S or key2 == 'ы':
            self.map_ll[1] -= self.press_delta / self.map_zoom
        if key == Qt.Key_A or key2 == 'ф':
            self.map_ll[0] -= self.press_delta / self.map_zoom
        if key == Qt.Key_D or key2 == 'в':
            self.map_ll[0] += self.press_delta / self.map_zoom
        self.getImage()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
