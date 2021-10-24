from typing import List, Tuple

import pygame
from pygame.locals import *

from engine.gamePlayer import GamePlayer, GamePlayerTypeId

from gui.guiNode import GuiNode
from gui.guiLabel import GuiLabel

class GuiPlayerList(GuiNode):
	def __init__(self, position: List, playerNames: List) -> None:
		super().__init__(position)

		self.players: list[GamePlayer] = []
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

	def getActivePlayer(self) -> GamePlayer:
		if self.activePlayerIndex < 0:
			return None

		return self.players[self.activePlayerIndex]

	def addPlayer(self, player: GamePlayer) -> None:
		self.players.append(player.copy())

		self.children[len(self.players) - 1].setText(player.name)

		self.render()

	def updatePlayerType(self, playerIndex: int, playerTypeId: int) -> None:
		self.players[playerIndex].typeId = playerTypeId

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
		if playerIndex > len(self.players):
			return

		self.activePlayerIndex = playerIndex

		for playerIndex in range(len(self.playerNames)):
			playerName = self.players[playerIndex].name
			if playerIndex == self.activePlayerIndex:
				playerName += " <"
			
			self.children[playerIndex].setText(playerName)

		self.render()

	def renderOnSelf(self) -> None:
		self.surface.fill((0, 0, 0, 0))
	