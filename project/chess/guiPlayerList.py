from typing import List, Tuple

import pygame
from pygame.locals import *

from gui.guiNode import GuiNode
from gui.guiLabel import GuiLabel

class GuiPlayerList(GuiNode):
	def __init__(self, position: List, playerNames: List) -> None:
		super().__init__(position)

		self.activePlayerIndex = -1
		self.playerNames = playerNames.copy()

		numberOfPlayers = len(self.playerNames)

		for playerIndex in range(numberOfPlayers):
			playerName = self.playerNames[playerIndex]
			guiLabel = GuiLabel([0, playerIndex * 64], playerName, "", 64)
			self.children.append(guiLabel)

		self.surface = pygame.Surface([256, 64 * numberOfPlayers], pygame.SRCALPHA, 32)
		self.surface.convert_alpha()

		self.render()

	#def addPlayerName(self, playerName: str) -> None:
	#	self.playerNames.append(playerName)
	#	# TODO: Adjust child nodes.
	#	self.render()
	
	#def removePlayerName(self, playerName: str) -> None:
	#	self.playerNames.remove(playerName)
	#	# TODO: Adjust child nodes.
	#	self.render()

	def setActivePlayerIndex(self, playerIndex: int) -> None:
		self.activePlayerIndex = playerIndex

		for playerIndex in range(len(self.playerNames)):
			playerName = self.playerNames[playerIndex]
			if playerIndex == self.activePlayerIndex:
				playerName += " <"
			
			self.children[playerIndex].setText(playerName)

		self.render()

	def renderOnSelf(self) -> None:
		self.surface.fill((0, 0, 0, 0))
	