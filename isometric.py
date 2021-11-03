import pygame, sys, time
from pygame.locals import *
import json

# Class to store basic level information
class Level:
    def __init__(self, name: str, player_pos: tuple, textures, data: list) -> None:
        self.name = name
        self.player_pos = player_pos
        self.data = data
        self.textures = textures

class Vector2D:
    def __init__(self, name: str, player_pos: tuple, textures, data: list) -> None:
        self.name = name
        self.player_pos = player_pos
        self.data = data
        self.textures = textures

# Base isometric renderer class
class Isometric:
    def __init__(self, display: pygame.Surface) -> None:
        self.display = display

    # Loads a texture to a pygame surface given the path
    def loadTex(self, path: str) -> pygame.Surface:
        tex = pygame.image.load(path).convert()
        tex.set_colorkey((0, 0, 0)) # Remove solid black pixels to avoid cutoff
        return tex

    # Loads a level to a "Level" instance given the path
    def loadLevel(self, path: str) -> Level:
        with open('map.json') as f:
            data = json.loads(f.read()) # Get level as a dict

            # Get level name
            try: name = data['name']
            except KeyError: name = 'Unnamed'

            # Get starting position of the camera
            try: player_pos = tuple(map(int, data['player_pos'].strip('(').strip(')').split(',')))
            except KeyError: player_pos = (int(self.pix_size[0] / 2), int(self.pix_size[1] / 2))

            # Load specified textures
            textures = []
            for texture in data['tex_bank']:
                if texture != 'BLANK':
                    textures.append(self.loadTex(texture))
                else:
                    textures.append(texture)
            map_data = [[[int(c) for c in row] for row in layer] for layer in data['data']] # Loads map layout data into a 2d array

            return Level(name=name, player_pos=player_pos, textures=textures, data=map_data)
#
# offset = (0, 0)
# # limits = (()())
#
# while True:
#     display.fill((0,0,0))
#
#     for y, row in enumerate(map_data):
#         for x, tile in enumerate(row):
#             if tile != 0:
#                 pygame.draw.circle(display, (0, 200, 200), ((150 + x * 10 - y * 10)+offset[0], (100 + x * 5 + y * 5)+offset[1]), 5)
#                 display.blit(texs[tile], ((150 + x * 10 - y * 10)+offset[0], (100 + x * 5 + y * 5)+offset[1]))
#                 # if random.randint(0, 1):
#                 #     display.blit(grass_img, (150 + x * 10 - y * 10, 100 + x * 5 + y * 5 - 14))
#
#     keys = pygame.key.get_pressed()
#     if keys[K_w]:
#         offset = (offset[0], offset[1] + 1)
#     if keys[K_s]:
#         offset = (offset[0], offset[1] - 1)
#     if keys[K_a]:
#         offset = (offset[0] + 1, offset[1])
#     if keys[K_d]:
#         offset = (offset[0] - 1, offset[1])
#
#     for event in pygame.event.get():
#         if event.type == QUIT:
#             pygame.quit()
#             sys.exit()
#
#         if event.type == KEYDOWN:
#             if event.key == K_ESCAPE:
#                 pygame.quit()
#                 sys.exit()
#
#     screen.blit(pygame.transform.scale(display, screen.get_size()), (0, 0))
#     pygame.display.update()
#     clock.tick(60)