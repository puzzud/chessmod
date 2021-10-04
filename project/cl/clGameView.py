from typing import Dict, List

from engine.gameView import GameView
from chess.chessGameModel import ChessGameModel
from chess.chessBoard import ChessBoard

class ClGameView(GameView):
	from chess.board import Board
	
	def __init__(self, chessGameModel: ChessGameModel):
		super().__init__(chessGameModel)

		self.signalHandlers = {
			"gameInitialized": self.onGameInitialized,
			"gameEnded": self.onGameEnded,
			"turnStarted": self.onTurnStarted,
			"turnEnded" : self.onTurnEnded,
			"pieceActivated": self.onPieceActivated,
			"pieceDeactivated": self.onPieceDeactivated,
			"invalidCellSelected": self.onInvalidCellSelected,
			"pieceMoved": self.onPieceMoved
		}

		self.attach(chessGameModel, "cellSelected")

		chessGameModel.attach(self, "gameInitialized")
		chessGameModel.attach(self, "gameEnded")
		chessGameModel.attach(self, "turnStarted")
		chessGameModel.attach(self, "turnEnded")
		chessGameModel.attach(self, "pieceActivated")
		chessGameModel.attach(self, "pieceDeactivated")
		chessGameModel.attach(self, "invalidCellSelected")
		chessGameModel.attach(self, "pieceMoved")
	
		self.board: ChessBoard = None
		self.teamNames = []

	def __del__(self):
		super().__del__()
	
	def draw(self) -> None:
		self.drawBoard(self.board)

	def drawBoard(self, board: ChessBoard) -> None:
		for y in range(0, board.cellHeight):
			for x in range(0, board.cellWidth):
				cellIndex = board.getCellIndexFromCoordinates([x, y])

	def onGameInitialized(self, payload: Dict) -> None:
		self.board = ChessBoard()
		self.board.loadFromStringRowList(payload["boardStringRowList"])

		self.teamNames = payload["teamNames"].copy()

	def onGameEnded(self, winningTeamIndex: int) -> None:
		print("Game Ended")
		print("Winner: " + self.teamNames[winningTeamIndex])

	def onTurnStarted(self, currentTurnTeamIndex: int) -> None:
		#print("Turn: " + self.chessGameModel.teamNames[self.chessGameModel.currentTurnTeamIndex])
		pass

	def onTurnEnded(self, payload: None) -> None:
		pass

	def onPieceActivated(self, payload: Dict) -> None:
		#piece = self.chessGameModel.board.getPiece(cellIndex)
		#print("Activated Piece")
		pass

	def onPieceDeactivated(self, cellIndex: int) -> None:
		#print("Deactivated Piece")
		pass

	def onInvalidCellSelected(self, cellIndex: int) -> None:
		print("Invalid Selection: " + str(cellIndex))

	def onPieceMoved(self, payload: List) -> None:
		#print("Moved Piece")
		pass
	