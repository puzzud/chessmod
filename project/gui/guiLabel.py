from typing import List, Tuple

import pygame
from pygame.locals import *

from .guiNode import GuiNode

class GuiLabel(GuiNode):
	def __init__(self, position: List, text: str, fontName: str = "", fontSize: int = 8, foregroundColor: pygame.Color = (255, 255, 255)) -> None:
		super().__init__(position)
		
		self.text = text
		self.fontName = fontName
		self.fontSize = fontSize
		self.foregroundColor = foregroundColor

		self.render()

	def setText(self, text: str) -> None:
		self.text = text
		self.render()
	
	def setFontName(self, fontName: str) -> None:
		self.fontName = fontName
		self.render()
	
	def setFontName(self, fontSize: int) -> None:
		self.fontSize = fontSize
		self.render()
	
	def setForegroundColor(self, foregroundColor: pygame.Color) -> None:
		self.foregroundColor = foregroundColor
		self.render()

	def renderOnSelf(self) -> None:
		font = pygame.font.SysFont(self.fontName, self.fontSize)
		self.surface = font.render(self.text, True, self.foregroundColor)
