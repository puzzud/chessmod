from typing import Dict, List
import copy

class Piece:
	def __init__(self, teamIndex: int = -1, moveCount: int = 0):
		self.teamIndex: int = teamIndex
		self.moveCount: int = moveCount

	def __copy__(self):
		return Piece(teamIndex = self.teamIndex, moveCount = self.moveCount)

	def copy(self):
		return copy.copy(self)
	
	def getAttributesAsDict(self) -> Dict:
		return self.__dict__

	def populateAttributesFromDict(self, fromDict: dict) -> None:
		for key in fromDict:
			attributeValue = getattr(self, key, None)
			if attributeValue is not None:
				setattr(self, key, fromDict[key])

	def getPossibleTargetCellIndices(self, _board, cellIndex: int) -> List[int]:
		return []
	
	def getPossibleAttackCellIndices(self, _board, cellIndex: int) -> List[int]:
		return []
	
	def getPieceActionsFromTargetCell(self, _board, activeCellIndex: int, targetCellIndex: int) -> List[dict]:
		return []
