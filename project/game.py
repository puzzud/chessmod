import pygame
from pygame.locals import *

from gameLogic import GameLogic
from gameRenderer import GameRenderer

def main() -> None:
	pygame.init()
	pygame.font.init()

	done = False

	gameLogic = GameLogic()
	gameRenderer = GameRenderer(gameLogic)

	while not done:
		for event in pygame.event.get():
			if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
				done = True

		gameRenderer.draw()
	
	pygame.quit()

main()
