from typing import Any, Dict, List

import pygame
from pygame.locals import *

from gui.guiNode import GuiNode
from chess.guiCommandLine import GuiCommandLine
from chess.guiPlayerList import GuiPlayerList
from chess.guiChessBoard import GuiChessBoard

from engine.gameView import GameView
from engine.gamePlayer import GamePlayer, GamePlayerTypeId

from chess.chessGameModel import ChessGameModel
from chess.chessBoard import ChessBoard
from chess.chessPlayerAi import ChessPlayerAi

class GuiGameView(GameView):
	from chess.board import Board
	
	def __init__(self, chessGameModel: ChessGameModel):
		super().__init__(chessGameModel)

		self.signalHandlers["gameInitialized"] = self.onGameInitialized
		self.signalHandlers["keyDown"] = self.onKeyDown
		self.signalHandlers["pointerDown"] = self.onPointerDown
		self.signalHandlers["commandLineEntered"] = self.onCommandLineEntered
		self.signalHandlers["turnStarted"] = self.onTurnStarted
		self.signalHandlers["turnEnded"] = self.onTurnEnded
		self.signalHandlers["pieceActivated"] = self.onPieceActivated
		self.signalHandlers["pieceDeactivated"] = self.onPieceDeactivated
		self.signalHandlers["actionsMade"] = self.onActionsMade

		chessGameModel.attach(self, "gameInitialized")
		chessGameModel.attach(self, "turnStarted")
		chessGameModel.attach(self, "turnEnded")
		chessGameModel.attach(self, "pieceActivated")
		chessGameModel.attach(self, "pieceDeactivated")
		chessGameModel.attach(self, "actionsMade")

		self.backgroundColor = (0, 0, 0)

		pygame.init()
		pygame.font.init()

		self.screen = pygame.display.set_mode((800, 600))

		self.guiCommandLine: GuiCommandLine = None
		self.guiChessBoard: GuiChessBoard = None
		self.guiPlayerList: GuiPlayerList = None
	
	def __del__(self):
		pygame.quit()
		super().__del__()

	def getCellIndexFromPoint(self, position: List[int]) -> int:
		cellCoordinates = self.guiChessBoard.getCellCoordinatesFromPoint(position)
		return self.guiChessBoard.board.getCellIndexFromCoordinates(cellCoordinates)
	
	def draw(self) -> None:
		self.screen.fill(self.backgroundColor)
		
		self.guiChessBoard.draw(self.screen)
		self.guiPlayerList.draw(self.screen)
		self.guiCommandLine.draw(self.screen)

		pygame.display.update()

	def selectCell(self, cellIndex: int) -> None:
		self.notify("cellSelected", cellIndex)

	def makePlayerAiAction(self, teamIndex: int) -> None:
		activeCellIndex: int = -1
		targetCellIndex: int = -1
		chessPlayerAi = ChessPlayerAi(self.guiChessBoard.board, self.guiPlayerList.activePlayerIndex)
		(activeCellIndex, targetCellIndex) = chessPlayerAi.getPieceActionCells()

		if activeCellIndex > -1 and targetCellIndex > -1:
			self.selectCell(activeCellIndex)
			self.selectCell(targetCellIndex)

	def onGameInitialized(self, payload: Dict[str, Any]) -> None:
		board = ChessBoard()
		board.loadFromStringRowList(payload["boardStringRowList"])
		self.guiChessBoard = GuiChessBoard([0, 0], board)

		guiChessBoardDimensions = self.guiChessBoard.getDimensions()
		self.guiPlayerList = GuiPlayerList([guiChessBoardDimensions[0] + 64, 0], payload["teamNames"].copy())

		self.guiCommandLine = GuiCommandLine([0, guiChessBoardDimensions[1] + 24])
		self.guiCommandLine.attach(self, "commandLineEntered")

		self.draw()

		for teamIndex in range(len(payload["teamNames"])):
			player = GamePlayer()
			player.typeId = GamePlayerTypeId.LOCAL.value
			player.teamIndex = teamIndex
			player.name = "Player " + str(teamIndex)
			self.notify("playerJoinRequested", player)

	def onPlayerAdded(self, player: GamePlayer) -> None:
		self.guiPlayerList.addPlayer(player)

	def onPlayerTypeUpdated(self, payload: Dict[str, Any]) -> None:
		playerIndex = payload["index"]
		self.guiPlayerList.updatePlayerType(playerIndex, payload["value"])

		if playerIndex == self.guiPlayerList.activePlayerIndex:
			if self.guiPlayerList.getActivePlayer().typeId == GamePlayerTypeId.AI.value:
				self.makePlayerAiAction(playerIndex)

	def onKeyDown(self, payload: Dict[str, Any]) -> None:
		keyCode: int = payload["keyCode"]
		character: str = payload["character"]
		self.guiCommandLine.onKeyDown(keyCode, character)

		self.draw()

	def onPointerDown(self, position: List[int]) -> None:
		activePlayerTypeId = self.guiPlayerList.getActivePlayer().typeId
		if activePlayerTypeId != GamePlayerTypeId.LOCAL.value:
			return

		cellIndex = self.getCellIndexFromPoint(position)
		if cellIndex > -1:
			self.selectCell(cellIndex)

	def onCommandLineEntered(self, textCommand: str) -> None:
		self.notify("textCommandIssued", textCommand)

	def onTurnStarted(self, currentTurnTeamIndex: int) -> None:
		self.guiChessBoard.clearHighlightedCells()
		self.guiPlayerList.setActivePlayerIndex(currentTurnTeamIndex)

		activePlayer = self.guiPlayerList.getActivePlayer()
		if activePlayer.typeId == GamePlayerTypeId.AI.value:
			self.makePlayerAiAction(currentTurnTeamIndex)

		self.draw()

	def onTurnEnded(self, currentTurnTeamIndex: int) -> None:
		self.guiChessBoard.clearHighlightedCells()

		self.draw()
	
	def onPieceActivated(self, payload: Dict[str, Any]) -> None:
		self.guiChessBoard.setHighlightedCells(payload["activatedCellIndex"], payload["validCellIndices"])

		self.draw()

	def onPieceDeactivated(self, cellIndex: int) -> None:
		self.guiChessBoard.clearHighlightedCells()

		self.draw()
	
	def onActionsMade(self, pieceActions: List[dict]) -> None:
		self.guiChessBoard.board.executePieceActions(pieceActions)

		self.draw()
