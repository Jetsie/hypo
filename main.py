import pygame
import sys, time
from pygame.locals import *

import isometric

#
pygame.font.init()
font = pygame.font.SysFont("Arial", 30)
#

res = (900, 900)
pygame.init()
pygame.display.set_caption('Hypo')
screen = pygame.display.set_mode(res, 0, 32)
clock = pygame.time.Clock()

pix_res = (res[0] / 3, res[1] / 3)
sprite_res = (20, 24)
half_width = int(sprite_res[0] / 2)
quarter_width = int(sprite_res[0] / 4)

iso = isometric.Isometric(pygame.Surface((res[0] / 3, res[1] / 3)))

level = iso.loadLevel('map.json')
pygame.display.set_caption(f'Hypo - {level.name}')

player = level.player_pos
offset = (pix_res[0] / 2 - player[0], pix_res[1] / 2 - player[1])


ghostN = pygame.image.load("textures/entities/ghost/ghost_N.png").convert()
ghostN.set_colorkey((0, 0, 0))
ghostE = pygame.image.load("textures/entities/ghost/ghost_E.png").convert()
ghostE.set_colorkey((0, 0, 0))
ghostS = pygame.image.load("textures/entities/ghost/ghost_S.png").convert()
ghostS.set_colorkey((0, 0, 0))
ghostW = pygame.image.load("textures/entities/ghost/ghost_W.png").convert()
ghostW.set_colorkey((0, 0, 0))
ghostNE = pygame.image.load("textures/entities/ghost/ghost_NE.png").convert()
ghostNE.set_colorkey((0, 0, 0))
ghostNW = pygame.image.load("textures/entities/ghost/ghost_NW.png").convert()
ghostNW.set_colorkey((0, 0, 0))
ghostSE = pygame.image.load("textures/entities/ghost/ghost_SE.png").convert()
ghostSE.set_colorkey((0, 0, 0))
ghostSW = pygame.image.load("textures/entities/ghost/ghost_SW.png").convert()
ghostSW.set_colorkey((0, 0, 0))
current = ghostN

while True:
	dt = clock.tick() / 1000
	iso.display.fill((0, 0, 0))

	for z, layer in enumerate(level.data):
		for y, row in enumerate(layer):
			for x, tile in enumerate(row):
				if type(level.textures[tile]) == pygame.Surface:
					ptile = ((x * half_width - y * half_width) + offset[0] - half_width, (x * quarter_width + y * quarter_width) + offset[1] - (z * 14) + half_width)
					ppos = ((player[0] * half_width - player[1] * half_width) + offset[0] - sprite_res[0], (player[0] * quarter_width + player[1] * quarter_width) + offset[1] - (player[2] * 14) - half_width)

					point = False
					if (player[0] < x and player[1] < y and player[2] < z) and (player[0]+1 > x and player[1]+1 > y and player[2]+2 > z):
						iso.display.blit(current, ppos)
						iso.display.blit(level.textures[tile], ptile)
						point = True
					else:
						iso.display.blit(level.textures[tile], ptile)

					if not point:
						iso.display.blit(current, ppos)
				# if player[0] in range(x, x+1):

	# pygame.draw.circle(iso.display, (255, 0, 0), ((player[0] * half_width - player[1] * half_width) + offset[0] - half_width, (player[0] * quarter_width + player[1] * quarter_width) + offset[1] - (player[2] * 14) + half_width), 2)
	# iso.display.blit(current, ((player[0] * half_width - player[1] * half_width) + offset[0] - half_width, (player[0] * quarter_width + player[1] * quarter_width) + offset[1] - (player[2] * 14) + half_width))

	# This line is where the camera follows the player, add cam effects here
	offset = (player[0] * -1 + pix_res[0] / 2, player[1] * -1 + pix_res[1] / 2)

	# print((int(player[0]), int(player[1]), int(player[2])))

	speed = 5

	keys = pygame.key.get_pressed()
	if keys[K_w]:
		player = (player[0], player[1] - speed * dt, player[2])
	if keys[K_s]:
		player = (player[0], player[1] + speed * dt, player[2])
	if keys[K_a]:
		player = (player[0] - speed * dt, player[1], player[2])
	if keys[K_d]:
		player = (player[0] + speed * dt, player[1], player[2])

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

		if event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				pygame.quit()
				sys.exit()
			if event.key == K_r:
				level = iso.loadLevel('map.json')
				pygame.display.set_caption(f'Hypo - {level.name}')

	screen.blit(pygame.transform.scale(iso.display, res), (0, 0))

	screen.blit(font.render(f'FPS: {str(int(clock.get_fps()))}', False, (255, 255, 255)),(0,0))
	pygame.display.update()
