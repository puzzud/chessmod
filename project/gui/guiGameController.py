from typing import List

from engine.gameController import GameController
from engine.gameModel import GameModel

class GuiGameController(GameController):
	def __init__(self, gameModel: GameModel):
		super().__init__(gameModel)

		self.signalHandlers["playerJoinRequested"] = self.onPlayerJoinRequested
		self.signalHandlers["cellSelected"] = self.onCellSelected
		self.signalHandlers["textCommandIssued"] = self.onTextCommandIssued

		self.attach(gameModel, "cellSelected")
		self.attach(gameModel, "quitRequested")
	
	def onCellSelected(self, cellIndex: int) -> None:
		self.notify("cellSelected", cellIndex)

	def onTextCommandIssued(self, textCommand: str) -> None:
		textCommand = str(textCommand)
		if textCommand == "quit":
			self.notify("quitRequested")
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
	