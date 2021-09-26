from observer import Observer
import pieceSet
from board import Board

class GameLogic(Observer):
	def __init__(self):
		super().__init__()

		self.signalHandlers = {
			"cellSelected": self.onCellSelected
		}

		self.board = Board(8, 8, pieceSet.ChessPieceSet())

		self.currentTurnTeamIndex = 0
		self.phaseId = 0
		self.turnStateId = 0
		self.validCellIndices = []
		self.activatedPieceCellIndex = -1

	def initialize(self) -> int:
		self.board.loadFromStringRowList(
			[
				"rnbqkbnr",
				"pppppppp",
				"........",
				"........",
				"........",
				"........",
				"PPPPPPPP",
				"RNBQKBNR"
			]
		)

		self.notify("gameInitialized")

		return 0

	def shutdown(self) -> int:
		return 0

	def activatePiece(self, cellIndex: int) -> None:
		pieceTypeIndex = self.board.cellPieceTypes[cellIndex]
		self.activatedPieceCellIndex = cellIndex
		self.turnStateId = 1
		
		print("Activated Piece: " + str(pieceTypeIndex))

		self.notify("pieceActivated", cellIndex)

		#piece = self.board.getPiece(cellIndex)

	def movePiece(self, fromCellIndex: int, toCellIndex: int) -> None:
		pieceTypeIndex = self.board.cellPieceTypes[fromCellIndex]
		teamIndex = self.board.cellPieceTeams[fromCellIndex]

		self.board.cellPieceTypes[fromCellIndex] = -1
		self.board.cellPieceTeams[fromCellIndex] = -1

		self.board.cellPieceTypes[toCellIndex] = pieceTypeIndex
		self.board.cellPieceTeams[toCellIndex] = teamIndex

		self.activatedPieceCellIndex = -1

		#print("Moved Piece: " + str(pieceTypeIndex))

		self.notify("pieceMoved", [fromCellIndex, toCellIndex])

	def endTurn(self) -> None:
		self.currentTurnTeamIndex = (self.currentTurnTeamIndex + 1) % 2
		self.turnStateId = 0

		self.notify("turnEnded")
	
	def onCellSelected(self, cellIndex: int) -> None:
		isValidCell = False
		
		if self.phaseId == 0:
			if self.turnStateId == 0:
				pieceTypeIndex = self.board.cellPieceTypes[cellIndex]
				if pieceTypeIndex != -1:
					teamIndex = self.board.cellPieceTeams[cellIndex]
					if teamIndex == self.currentTurnTeamIndex:
						isValidCell = True
						self.activatePiece(cellIndex)
			elif self.turnStateId == 1:
				isValidCell = self.board.isValidMoveDestination(self.activatedPieceCellIndex, cellIndex)
				if isValidCell:
					self.movePiece(self.activatedPieceCellIndex, cellIndex)
					self.endTurn()

		if not isValidCell:
			print("Invalid Selection: " + str(cellIndex))

			self.notify("invalidCellSelected", cellIndex)
		