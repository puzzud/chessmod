from typing import Dict, List

import pieceSet

class Board:
	def __init__(self, cellWidth: int, cellHeight: int, _pieceSet):
		self.cellWidth = cellWidth
		self.cellHeight = cellHeight

		numberOfCells = cellWidth * cellHeight
		self.cellPieceTypes = [-1] * numberOfCells
		self.cellPieceTeams = [-1] * numberOfCells

		self.pieceSet = _pieceSet

	def getCellCoordinatesFromIndex(self, cellIndex: int) -> List:
		return [
			int(cellIndex % self.cellWidth),
			int(cellIndex / self.cellHeight)
		]

	def getCellIndexFromCoordinates(self, cellCoordinates: List) -> int:
		return (cellCoordinates[1] * self.cellWidth) + cellCoordinates[0]

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
	
	def getValidMoveCellIndices(self, cellIndex: int) -> List:
		pieceType = self.cellPieceTypes[cellIndex]
		piece = self.pieceSet.pieces[pieceType]
		return piece.getPossibleMoves(self, cellIndex, self.cellPieceTeams[cellIndex])

	def isValidMoveDestination(self, sourceCellIndex: int, destinationCellIndex: int) -> bool:
		return destinationCellIndex in self.getValidMoveCellIndices(sourceCellIndex)
	