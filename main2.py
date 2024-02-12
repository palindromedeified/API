import os
import sys

import pygame
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class MainWindow():
    def __init__(self, *args, **kwargs):
        self.press_delta = 0.00001
        self.map_zoom = 5
        self.map_ll = [37.977751, 55.757718]
        self.map_l = 'map'
        self.map_key = ''

    def keyPressEvent(self, event):
        if event == 'up':
            self.map_zoom += 1
        elif event == 'down':
            self.map_zoom -= 1

    def update_map(self):
        map_params = {
            "ll": ','.join(map(str, self.map_ll)),
            "l": self.map_l,
            'z': self.map_zoom
        }
        # создаем сессию запросов
        session = requests.Session()
        # устанавливаем настройки для повторного подключения
        retry = Retry(total=10, connect=5, backoff_factor=0.5)
        # задаем настройки количества попыток и т д
        adapter = HTTPAdapter(max_retries=retry)
        # регистрируем адаптеры для подключения
        # session.mount('http://', adapter)
        # session.mount('https://', adapter)
        # выполняем запрос с нашими параметрами
        response = session.get('https://static-maps.yandex.ru/1.x/',
                               params=map_params)
        # создаем файл для записи картинки из запроса
        with open('tmp.png', mode='wb') as tmp:
            tmp.write(response.content)
        screen.blit(pygame.image.load('tmp.png'), (0, 0))


pygame.init()
screen = pygame.display.set_mode((600, 400))
running2 = True
w = MainWindow()
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
                w.update_map()
                pygame.display.flip()
            elif event.key == pygame.K_DOWN:
                w.keyPressEvent('down')
                w.update_map()
                pygame.display.flip()
# Удаляем за собой файл с изображением.
os.remove('tmp.png')
