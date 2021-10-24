from typing import List
from enum import Enum

from engine.gameModel import GameModel
from engine.gamePlayer import GamePlayer
import chess.chessPieceSet
import chess.chessBoard

class ChessPhaseId(Enum):
	PLAY = 0

class ChessTurnStateId(Enum):
	PIECE_NOT_ACTIVE = 0
	PIECE_ACTIVE = 1

class ChessGameModel(GameModel):
	MaximumNumberOfPlayers = 2

	def __init__(self):
		super().__init__()

		self.signalHandlers["cellSelected"] = self.onCellSelected

		self.teamNames = [
			"White",
			"Black"
		]

		self.board = chess.chessBoard.ChessBoard()

		self.currentTurnTeamIndex = -1
		self.phaseId = ChessPhaseId.PLAY
		self.turnStateId = ChessTurnStateId.PIECE_NOT_ACTIVE
		self.activatedPieceCellIndex = -1

	def initialize(self) -> int:
		boardStringRowList = [
			"rnbqkbnr",
			"pppppppp",
			"........",
			"........",
			"........",
			"........",
			"PPPPPPPP",
			"RNBQKBNR"
		]

		self.board.loadFromStringRowList(boardStringRowList)

		payload = {
			"teamNames": self.teamNames.copy(),
			"boardStringRowList": boardStringRowList.copy()
		}

		self.notify("gameInitialized", payload)
		
		return 0

	def getNextCurrentTurnTeamIndex(self) -> int:
		return (self.currentTurnTeamIndex + 1) % len(self.teamNames)

	def shutdown(self) -> int:
		return super().shutdown()

	def onPlayerJoinRequested(self, player: GamePlayer) -> None:
		currentNumberOfPlayers = len(self.players)
		if currentNumberOfPlayers >= self.MaximumNumberOfPlayers:
			return
		
		super().onPlayerJoinRequested(player)
		
		currentNumberOfPlayers = len(self.players)
		if currentNumberOfPlayers == self.MaximumNumberOfPlayers:
			self.startGame()

	def activatePiece(self, cellIndex: int) -> None:
		self.activatedPieceCellIndex = cellIndex
		self.turnStateId = ChessTurnStateId.PIECE_ACTIVE

		payload = {
			"activatedCellIndex": cellIndex,
			"validCellIndices": self.board.getValidTargetCellIndices(cellIndex)
		}

		self.notify("pieceActivated", payload)

	def deactivatePiece(self, cellIndex: int) -> None:
		self.activatedPieceCellIndex = -1
		self.turnStateId = ChessTurnStateId.PIECE_NOT_ACTIVE

		self.notify("pieceDeactivated", cellIndex)

	def performPieceAction(self, activeCellIndex: int, targetCellIndex: int) -> None:
		pieceActions = self.board.performPieceAction(activeCellIndex, targetCellIndex)

		self.activatedPieceCellIndex = -1

		self.notify("actionsMade", pieceActions)

		#self.board.print()

	def startTurn(self) -> None:
		self.turnStateId = ChessTurnStateId.PIECE_NOT_ACTIVE
		self.activatedPieceCellIndex = -1

		self.notify("turnStarted", self.currentTurnTeamIndex)

		currentMetEndOfGameCondition = self.board.getCurrentMetEndOfGameCondition(self.currentTurnTeamIndex)
		if currentMetEndOfGameCondition is not chess.chessBoard.ChessEndGameCondition.NONE:
			self.endGame(currentMetEndOfGameCondition)

	def endTurn(self) -> None:
		self.notify("turnEnded", self.currentTurnTeamIndex)

		self.currentTurnTeamIndex = self.getNextCurrentTurnTeamIndex()
		self.startTurn()
	
	def startGame(self) -> None:
		self.currentTurnTeamIndex = 0
		self.phaseId = ChessPhaseId.PLAY

		self.notify("gameStarted")

		self.startTurn()

	def endGame(self, endOfGameCondition: int) -> None:
		if endOfGameCondition == chess.chessBoard.ChessEndGameCondition.CHECKMATE:
			winningTeamIndex = self.getNextCurrentTurnTeamIndex()
		elif endOfGameCondition == chess.chessBoard.ChessEndGameCondition.STALEMATE:
			winningTeamIndex = -1

		self.notify("gameEnded", winningTeamIndex)

	def onCellSelected(self, cellIndex: int) -> None:
		isValidCell = False
		
		if self.phaseId == ChessPhaseId.PLAY:
			if self.turnStateId == ChessTurnStateId.PIECE_NOT_ACTIVE:
				if not self.board.isCellEmpty(cellIndex):
					teamIndex = self.board.getPieceFromCell(cellIndex).teamIndex
					if teamIndex == self.currentTurnTeamIndex:
						isValidCell = True
						self.activatePiece(cellIndex)
			elif self.turnStateId == ChessTurnStateId.PIECE_ACTIVE:
				if cellIndex == self.activatedPieceCellIndex:
					isValidCell = True
					self.deactivatePiece(cellIndex)
				else:
					isValidCell = self.board.isValidTargetCell(self.activatedPieceCellIndex, cellIndex)
					if isValidCell:
						self.performPieceAction(self.activatedPieceCellIndex, cellIndex)
						self.endTurn()

		if not isValidCell:
			self.notify("invalidCellSelected", cellIndex)
