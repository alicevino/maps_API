import pygame
import pygame_gui
import requests
import os
import sys


class Params(object):
    def __init__(self):
        self.latitude = 55.753630
        self.longitude = 37.620070
        self.spn = 0.003125
        self.type = 'map'

    def ll(self):
        answer = str(self.longitude) + ',' + str(self.latitude)
        return answer


def load_map(map):
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={map.ll()}&spn={map.spn},{map.spn}&l=map"
    response = requests.get(map_request)
    if not response:
        print('Ошибка:', map_request)
        print('Http статус:', response.status_code, '(', response.reason, ')')
        sys.exit(1)

    map_file = 'map.png'
    try:
        with open(map_file, 'wb') as f:
            f.write(response.content)
    except IOError as exception:
        print('Ошибка при записи временного файла:', exception)
        sys.exit(2)
    return map_file


pygame.init()
screen = pygame.display.set_mode((600, 450))
my_map = Params()
manager = pygame_gui.UIManager((600, 450))

PgUp = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((550, 350), (50, 50)),
    text='+',
    manager=manager
)
PgDown = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((550, 400), (50, 50)),
    text='-',
    manager=manager
)
running = True
clock = pygame.time.Clock()
while running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            os.remove(map_file)
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == PgUp:
                    if my_map.spn >= 0.00078125:
                        my_map.spn /= 2
                if event.ui_element == PgDown:
                    if my_map.spn <= 50:
                        my_map.spn *= 2
        manager.process_events(event)
    map_file = load_map(my_map)
    screen.blit(pygame.image.load(map_file), (0, 0))
    manager.update(time_delta)
    manager.draw_ui(screen)
    pygame.display.flip()

pygame.quit()
