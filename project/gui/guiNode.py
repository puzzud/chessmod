from typing import List, Tuple

import pygame
from pygame import surface
from pygame.locals import *

class GuiNode():
	def __init__(self, position: List) -> None:
		self.position = position.copy()
		self.children = []

		self.surface: pygame.Surface = None

	def setPosition(self, position: List) -> None:
		self.position = position.copy()

	def getDimensions(self) -> List:
		if self.surface is None:
			return [0, 0]
		
		return [
			self.surface.get_width(),
			self.surface.get_height()
		]

	def render(self) -> None:
		self.renderOnSelf()
		self.renderChildrenOnSelf()

	def renderOnSelf(self) -> None:
		pass

	def renderChildrenOnSelf(self) -> None:
		for guiNode in self.children:
			guiNode.draw(self.surface)

	def draw(self, destinationSurface: pygame.Surface) -> None:
		if self.surface is not None:
			destinationSurface.blit(self.surface, self.position)
