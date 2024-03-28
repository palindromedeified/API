import os
import sys

import pygame
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Определение констант
WHITE = (255, 255, 255)
TEXT_COLOR = (0, 0, 0)


# Функция для поиска объекта по его названию
def get_coord(address):
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
    lon, lat = map(float, pos.split())
    return lon, lat


class MainWindow():
    def __init__(self, *args, **kwargs):
        self.press_delta = 0.1
        self.map_zoom = 5
        self.map_ll = [37.977751, 55.757718]
        self.lst = ['map', 'sat', 'sat,skl']
        self.index = 0
        self.map_l = self.lst[self.index]
        self.map_key = ''

    def keyPressEvent(self, event):
        if event == 'up':
            self.map_zoom += 1
        elif event == 'down':
            self.map_zoom -= 1
        if event == 'e':
            self.index = (self.index + 1) % 3
            self.map_l = self.lst[self.index]
        if event == 'w':
            self.map_ll[1] += self.press_delta
        if event == 's':
            self.map_ll[1] -= self.press_delta
        if event == 'a':
            self.map_ll[0] -= self.press_delta
        if event == 'd':
            self.map_ll[0] += self.press_delta

    def update_map(self):
        map_params = {
            "ll": ','.join(map(str, self.map_ll)),
            "l": self.map_l,
            'z': self.map_zoom,
        }
        response = requests.get('https://static-maps.yandex.ru/1.x/', params=map_params)
        with open('tmp.png', mode='wb') as tmp:
            tmp.write(response.content)

        screen.blit(pygame.image.load('tmp.png'), (0, 0))


pygame.init()
screen = pygame.display.set_mode((600, 400))
font = pygame.font.Font(None, 24)
running2 = True
w = MainWindow()
w.update_map()
pygame.display.flip()


def func():
    w.update_map()
    pygame.display.flip()


while running2:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running2 = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                w.keyPressEvent('up')
            elif event.key == pygame.K_DOWN:
                w.keyPressEvent('down')
            elif event.key == pygame.K_w:
                w.keyPressEvent('w')
                w.update_map()
            elif event.key == pygame.K_s:
                w.keyPressEvent('s')
            elif event.key == pygame.K_a:
                w.keyPressEvent('a')
            elif event.key == pygame.K_d:
                w.keyPressEvent('d')
            elif event.key == pygame.K_e:
                w.keyPressEvent('e')
            w.update_map()
            pygame.display.flip()
# Удаляем за собой файл с изображением.
os.remove('tmp.png')
