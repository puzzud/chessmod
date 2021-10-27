from typing import Any, Dict, List

from gui.guiNode import GuiNode
from gui.guiGameView import GuiGameView

from chess.guiCommandLine import GuiCommandLine
from chess.guiPlayerList import GuiPlayerList
from chess.guiChessBoard import GuiChessBoard

from engine.gamePlayer import GamePlayer, GamePlayerTypeId

from chess.chessGameModel import ChessGameModel
from chess.chessGameController import ChessGameController
from chess.chessBoard import ChessBoard
from chess.chessPlayerAi import ChessPlayerAi

class GuiChessGameView(GuiGameView):
	from chess.board import Board
	
	def __init__(self, chessGameModel: ChessGameModel, chessGameController: ChessGameController):
		super().__init__(chessGameModel, chessGameController)

		self.signalHandlers["turnStarted"] = self.onTurnStarted
		self.signalHandlers["turnEnded"] = self.onTurnEnded
		self.signalHandlers["pieceActivated"] = self.onPieceActivated
		self.signalHandlers["pieceDeactivated"] = self.onPieceDeactivated
		self.signalHandlers["actionsMade"] = self.onActionsMade

		self.attach(chessGameController, "playerJoinRequested")
		self.attach(chessGameController, "cellSelected")
		self.attach(chessGameController, "textCommandIssued")

		chessGameModel.attach(self, "turnStarted")
		chessGameModel.attach(self, "turnEnded")
		chessGameModel.attach(self, "pieceActivated")
		chessGameModel.attach(self, "pieceDeactivated")
		chessGameModel.attach(self, "actionsMade")

		self.guiCommandLine: GuiCommandLine = None
		self.guiChessBoard: GuiChessBoard = None
		self.guiPlayerList: GuiPlayerList = None
	
	def __del__(self):
		super().__del__()

	def getCellIndexFromPoint(self, position: List[int]) -> int:
		cellCoordinates = self.guiChessBoard.getCellCoordinatesFromPoint(position)
		return self.guiChessBoard.board.getCellIndexFromCoordinates(cellCoordinates)

	def process(self) -> None:
		activePlayer = self.guiPlayerList.getActivePlayer()
		if activePlayer is not None:
			if activePlayer.typeId == GamePlayerTypeId.AI.value:
				self.makePlayerAiAction(self.guiPlayerList.activePlayerIndex)

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
		self.guiNodes.append(self.guiChessBoard)

		guiChessBoardDimensions = self.guiChessBoard.getDimensions()
		self.guiPlayerList = GuiPlayerList([guiChessBoardDimensions[0] + 64, 0], payload["teamNames"].copy())
		self.guiNodes.append(self.guiPlayerList)

		self.guiCommandLine = GuiCommandLine([0, guiChessBoardDimensions[1] + 24])
		self.guiCommandLine.attach(self, "commandLineEntered")
		self.guiNodes.append(self.guiCommandLine)

		self.draw()

		for teamIndex in range(len(payload["teamNames"])):
			player = GamePlayer()
			player.typeId = GamePlayerTypeId.LOCAL.value
			player.teamIndex = teamIndex
			player.name = "Player " + str(teamIndex)
			self.notify("playerJoinRequested", player)

	def onGameQuit(self, payload: None) -> None:
		self.running = False

	def onPlayerAdded(self, player: GamePlayer) -> None:
		self.guiPlayerList.addPlayer(player)

	def onPlayerTypeUpdated(self, payload: Dict[str, Any]) -> None:
		playerIndex = payload["index"]
		self.guiPlayerList.updatePlayerType(playerIndex, payload["value"])

	def onTurnStarted(self, currentTurnTeamIndex: int) -> None:
		self.guiChessBoard.clearHighlightedCells()
		self.guiPlayerList.setActivePlayerIndex(currentTurnTeamIndex)

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
	
	def onKeyDown(self, keyCode: int, character: str) -> None:
		self.guiCommandLine.onKeyDown(keyCode, character)

		self.draw()

	def onPointerDown(self, position: List[int]) -> None:
		activePlayerTypeId = self.guiPlayerList.getActivePlayer().typeId
		if activePlayerTypeId != GamePlayerTypeId.LOCAL.value:
			return

		cellIndex = self.getCellIndexFromPoint(position)
		if cellIndex > -1:
			self.selectCell(cellIndex)
	