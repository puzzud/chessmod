from typing import Tuple

import random

from chess.chessBoard import ChessBoard

class ChessPlayerAi():
	def __init__(self, chessBoard: ChessBoard, teamIndex: int):
		self.chessBoard = chessBoard
		self.teamIndex = teamIndex
	
	def getPieceActionCells(self) -> Tuple[int]:
		return self.getRandomPieceActionCells()
	
	def getRandomPieceActionCells(self) -> Tuple[int]:
		teamPieceIndices = self.chessBoard.getAllTeamPieceIndices(self.teamIndex)

		numberOfTeamPieceIndices = len(teamPieceIndices)
		if numberOfTeamPieceIndices < 1:
			return (-1, -1)

		randomPivotIndex = random.randint(0, numberOfTeamPieceIndices - 1)

		for index in reversed(range(randomPivotIndex)):
			cellIndex = teamPieceIndices[index]
			validTargetCellIndices = self.chessBoard.getValidTargetCellIndices(cellIndex)
			if len(validTargetCellIndices) > 0:
				randomTargetCellIndex = random.randint(0, len(validTargetCellIndices) - 1)
				return (cellIndex, validTargetCellIndices[randomTargetCellIndex])
		
		for index in range(randomPivotIndex, numberOfTeamPieceIndices - 1):
			cellIndex = teamPieceIndices[index]
			validTargetCellIndices = self.chessBoard.getValidTargetCellIndices(cellIndex)
			if len(validTargetCellIndices) > 0:
				randomTargetCellIndex = random.randint(0, len(validTargetCellIndices) - 1)
				return (cellIndex, validTargetCellIndices[randomTargetCellIndex])

		for cellIndex in teamPieceIndices:
			validTargetCellIndices = self.chessBoard.getValidTargetCellIndices(cellIndex)
			if len(validTargetCellIndices) > 0:
				randomTargetCellIndex = random.randint(0, len(validTargetCellIndices) - 1)
				return (cellIndex, validTargetCellIndices[randomTargetCellIndex])

		return (-1, -1)
	