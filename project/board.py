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

	def setCell(self, x: int, y: int, contents: Dict) -> None:
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
				self.setCell(x, y, self.getCellContentsFromCharacter(character))
				x += 1
			y += 1
		