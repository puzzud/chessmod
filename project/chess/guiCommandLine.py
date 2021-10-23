from typing import List, Tuple

import pygame
from pygame.locals import *

from gui.guiNode import GuiNode
from gui.guiLabel import GuiLabel

class GuiCommandLine(GuiLabel):
	def __init__(self, position: List) -> None:
		super().__init__(position, "", "", 64)

		self.prefixTest = ":"
		self.commandText = ""

		self.surface = pygame.Surface([256, 64], pygame.SRCALPHA, 32)
		self.surface.convert_alpha()

		self.setCommandText(self.commandText)

		self.render()

	def setCommandText(self, commandText: str) -> None:
		self.commandText = commandText
		self.setText(self.prefixTest + self.commandText)

	def onKeyDown(self, keyCode: int, character: str) -> None:
		newCommandText = self.commandText
		
		if keyCode == pygame.K_BACKSPACE:
			newLength = len(newCommandText) - 1
			if newLength < 0:
				return
			
			newCommandText = newCommandText[:newLength]
		elif keyCode == pygame.K_RETURN:
			self.notify("commandLineEntered", self.commandText)
			newCommandText = ""
		elif len(character) > 0:
			newCommandText += character

		self.setCommandText(newCommandText)
