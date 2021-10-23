from typing import List

import pygame
from pygame.locals import *

from engine.gameController import GameController
from engine.gameModel import GameModel
from gui.guiGameView import GuiGameView

class GuiGameController(GameController):
	def __init__(self, gameModel: GameModel, guiGameView: GuiGameView):
		super().__init__(gameModel)

		self.signalHandlers["playerJoinRequested"] = self.onPlayerJoinRequested
		self.signalHandlers["cellSelected"] = self.onCellSelected
		self.signalHandlers["textCommandIssued"] = self.onTextCommandIssued

		self.eventHandlers: dict[str, function] = {
			pygame.QUIT: self.onQuitEvent,
			pygame.KEYDOWN: self.onKeyEvent,
			pygame.KEYUP: self.onKeyEvent,
			pygame.MOUSEBUTTONDOWN: self.onMouseEvent,
			pygame.MOUSEBUTTONUP: self.onMouseEvent
		}

		guiGameView.attach(self, "playerJoinRequested")
		guiGameView.attach(self, "cellSelected")
		guiGameView.attach(self, "textCommandIssued")

		self.attach(gameModel, "cellSelected")

		self.attach(guiGameView, "keyDown")
		self.attach(guiGameView, "pointerDown")

		self.running = False
	
	def loop(self) -> int:
		self.running = True

		while self.running:
			self.proccessEvents()
		
		return 0

	def proccessEvents(self) -> None:
		for event in pygame.event.get():
			eventHandler = self.eventHandlers.get(event.type, None)
			if eventHandler is not None:
				eventHandler(event)
	
	def onQuitEvent(self, event) -> None:
		self.running = False
	
	def onKeyEvent(self, event: pygame.event) -> None:
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				self.running = False
				return
			
			self.notify("keyDown", {"keyCode": event.key, "character": event.unicode})
	
	def onMouseEvent(self, event: pygame.event) -> None:
		if event.type == pygame.MOUSEBUTTONDOWN:
			self.notify("pointerDown", event.pos)
	
	def onCellSelected(self, cellIndex: int) -> None:
		self.notify("cellSelected", cellIndex)

	def onTextCommandIssued(self, textCommand: str) -> None:
		textCommand = str(textCommand)
		if textCommand == "quit":
			self.running = False
			return
		
		commandParts = textCommand.split(' ')
		numberOfCommandParts = len(commandParts)
		if numberOfCommandParts <= 0:
			return

		commandName = commandParts[0].lower()

		if commandName == "player_type":
			if numberOfCommandParts == 3:
				command = {
					"name": commandName,
					"index": int(commandParts[1]),
					"value": commandParts[2]
				}
				self.notify("commandIssued", command)
	