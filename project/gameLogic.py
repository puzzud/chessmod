from observer import Observer
from pieceTypes import PieceTypes, PieceTypeLetters

class GameLogic(Observer):
	from board import Board
	
	def __init__(self):
		super().__init__()

		self.signalHandlers = {
			"cellSelected": self.onCellSelected
		}

		self.done = False

		self.board = self.Board(8, 8)

		self.currentTurnTeamIndex = 0
		self.phaseId = 0
		self.turnStateId = 0
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
		
		print("Activated Piece: " + PieceTypeLetters[pieceTypeIndex])

		self.notify("pieceActivated", cellIndex)

	def movePiece(self, fromCellIndex: int, toCellIndex: int) -> None:
		pieceTypeIndex = self.board.cellPieceTypes[fromCellIndex]
		teamIndex = self.board.cellPieceTeams[fromCellIndex]

		self.board.cellPieceTypes[fromCellIndex] = PieceTypes.NONE.value
		self.board.cellPieceTeams[fromCellIndex] = -1

		self.board.cellPieceTypes[toCellIndex] = pieceTypeIndex
		self.board.cellPieceTeams[toCellIndex] = teamIndex

		self.activatedPieceCellIndex = -1

		#print("Moved Piece: " + str(PieceTypeLetters[pieceTypeIndex]))

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
				if pieceTypeIndex != PieceTypes.NONE:
					teamIndex = self.board.cellPieceTeams[cellIndex]
					if teamIndex == self.currentTurnTeamIndex:
						isValidCell = True
						self.activatePiece(cellIndex)
			elif self.turnStateId == 1:
				teamIndex = self.board.cellPieceTeams[cellIndex]
				if teamIndex != self.currentTurnTeamIndex:
					isValidCell = True
					self.movePiece(self.activatedPieceCellIndex, cellIndex)
					self.endTurn()

		if not isValidCell:
			print("Invalid Selection: " + str(cellIndex))

			self.notify("invalidCellSelected", cellIndex)
		