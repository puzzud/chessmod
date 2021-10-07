from typing import List, Tuple

import pygame
from pygame.locals import *

from gui.guiNode import GuiNode
from gui.guiLabel import GuiLabel

class GuiCommandLine(GuiLabel):
	def __init__(self, position: List) -> None:
		super().__init__(position, "", "", 64)

		self.surface = pygame.Surface([256, 64], pygame.SRCALPHA, 32)
		self.surface.convert_alpha()

		self.render()

	def onKeyDown(self, keyCode: int) -> None:
		newText = self.text
		
		if keyCode == pygame.K_BACKSPACE:
			newLength = len(newText) - 1
			if newLength < 0:
				return
			
			newText = newText[:newLength]
		elif keyCode == pygame.K_RETURN:
			self.notify("commandLineEntered", self.text)
			newText = ""
		else:
			newText += chr(keyCode % 256)

		self.setText(newText)

		self.render()
	