from typing import Dict, List

import chess.pieceSet

class Board:
	def __init__(self, cellWidth: int, cellHeight: int, _pieceSet):
		self.cellWidth = cellWidth
		self.cellHeight = cellHeight

		numberOfCells = self.getNumberOfCells()
		self.cellPieceTypes = [-1] * numberOfCells
		self.cellPieceTeams = [-1] * numberOfCells

		self.pieceSet = _pieceSet

	def getNumberOfCells(self) -> int:
		return self.cellWidth * self.cellHeight

	def getCellCoordinatesFromIndex(self, cellIndex: int) -> List:
		return [
			int(cellIndex % self.cellWidth),
			int(cellIndex / self.cellHeight)
		]

	def getCellIndexFromCoordinates(self, cellCoordinates: List) -> int:
		if cellCoordinates[0] >= self.cellWidth:
			return -1

		if cellCoordinates[1] >= self.cellHeight:
			return -1

		return (cellCoordinates[1] * self.cellWidth) + cellCoordinates[0]

	def areCellCoordinatesOnBoard(self, cellCoordinates: List) -> bool:
		if (cellCoordinates[0] < 0) or (cellCoordinates[0] >= self.cellWidth):
			return False
		
		if (cellCoordinates[1] < 0) or (cellCoordinates[1] >= self.cellHeight):
			return False
		
		return True

	def getCellContents(self, x: int, y: int) -> Dict:
		cellIndex = self.getCellIndexFromCoordinates([x, y])

		return {
			"pieceType": self.cellPieceTypes[cellIndex],
			"teamIndex": self.cellPieceTeams[cellIndex]
		}

	def setCellContents(self, x: int, y: int, contents: Dict) -> None:
		cellIndex = self.getCellIndexFromCoordinates([x, y])

		self.cellPieceTypes[cellIndex] = contents["pieceType"]
		self.cellPieceTeams[cellIndex] = contents["teamIndex"]

	def isCellEmpty(self, cellIndex: int) -> bool:
		return self.cellPieceTypes[cellIndex] == -1

	def doesCellHaveOpponentPiece(self, cellIndex: int, teamIndex: int) -> bool:
		return (not self.isCellEmpty(cellIndex)) and (self.cellPieceTeams[cellIndex] != teamIndex)

	def getCellContentsFromCharacter(self, character: str) -> Dict:
		if character is '.':
			return {
			"pieceType": -1,
			"teamIndex": -1
		}
		
		return self.pieceSet.getPiecePropertiesFromCharacter(character)

	def loadFromStringRowList(self, stringRowList: List) -> None:
		y = 0
		for stringRow in stringRowList:
			x = 0
			for character in stringRow:
				self.setCellContents(x, y, self.getCellContentsFromCharacter(character))
				x += 1
			y += 1
	
	def getCellsFromRay(self, sourceCellCoordinates: List, direction: List, distance: int) -> List:
		cellIndices = []
		
		cellCoordinates = sourceCellCoordinates.copy()

		for offset in range(distance):
			cellCoordinates[0] += direction[0]
			cellCoordinates[1] += direction[1]
			if not self.areCellCoordinatesOnBoard(cellCoordinates):
				break

			cellIndex = self.getCellIndexFromCoordinates(cellCoordinates)

			cellIndices.append(cellIndex)

			# Stop after meeting a piece.
			if self.cellPieceTypes[cellIndex] != -1:
				break
		
		return cellIndices

	def getValidMoveCellIndices(self, cellIndex: int) -> List:
		pieceType = self.cellPieceTypes[cellIndex]
		piece = self.pieceSet.pieces[pieceType]
		return piece.getPossibleMoves(self, cellIndex, self.cellPieceTeams[cellIndex])

	# TODO: Should be in model?
	def isValidMoveDestination(self, sourceCellIndex: int, toCellIndex: int) -> bool:
		return toCellIndex in self.getValidMoveCellIndices(sourceCellIndex)

	def movePiece(self, fromCellIndex: int, toCellIndex: int) -> int:
		pieceTypeIndex = self.cellPieceTypes[fromCellIndex]
		teamIndex = self.cellPieceTeams[fromCellIndex]
		
		self.cellPieceTypes[fromCellIndex] = -1
		self.cellPieceTeams[fromCellIndex] = -1

		self.cellPieceTypes[toCellIndex] = pieceTypeIndex
		self.cellPieceTeams[toCellIndex] = teamIndex

		return 0

class ChessBoard(Board):
	def __init__(self):
		super().__init__(8, 8, chess.chessPieceSet.ChessPieceSet())
