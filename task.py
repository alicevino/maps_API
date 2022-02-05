import pygame
import requests
import os
import sys


class Params(object):
    def __init__(self):
        self.latitude = 55.753630
        self.longitude = 37.620070

    def ll(self):
        answer = str(self.longitude) + ',' + str(self.latitude)
        return answer


def load_map(map):
    map_request = "http://static-maps.yandex.ru/1.x/?ll={ll}&spn=0.04,0.04&l=map".format(ll=map.ll())
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

running = True

pygame.init()
screen = pygame.display.set_mode((600, 450))
my_map = Params()
map_file = load_map(my_map)
screen.blit(pygame.image.load(map_file), (0, 0))
pygame.display.flip()
while pygame.event.wait().type != pygame.QUIT:
    pass
pygame.quit()

os.remove(map_file)
