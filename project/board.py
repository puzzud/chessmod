from typing import Dict, List

from pieceTypes import *

class Board:
	def __init__(self, cellWidth: int, cellHeight: int):
		self.cellWidth = cellWidth
		self.cellHeight = cellHeight

		numberOfCells = cellWidth * cellHeight

		self.cellPieceTypes = [PieceTypes.NONE.value] * numberOfCells
		self.cellPieceTeams = [-1] * numberOfCells

	def setCell(self, x: int, y: int, contents: Dict) -> None:
		cellIndex = (y * self.cellWidth) + x

		self.cellPieceTypes[cellIndex] = contents["pieceType"]
		self.cellPieceTeams[cellIndex] = contents["teamIndex"]

	def loadFromStringRowList(self, stringRowList: List) -> None:
		y = 0
		for stringRow in stringRowList:
			x = 0
			for character in stringRow:
				pieceType = PieceTypes.NONE.value
				teamIndex = -1

				if character is not PieceTypeLetters[PieceTypes.NONE.value]:
					
					for keyPieceType in PieceTypeLetters:
						pieceLetter = PieceTypeLetters[keyPieceType]

						if character is pieceLetter:
							teamIndex = 0
						elif character == pieceLetter.lower():
							teamIndex = 1
						
						if teamIndex > -1:
							pieceType = keyPieceType
							break
				
				self.setCell(x, y, {"pieceType": pieceType, "teamIndex": teamIndex})

				x += 1
			
			y += 1
		