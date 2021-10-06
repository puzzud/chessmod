from typing import Dict, List
import copy

class Piece:
	def __init__(self, teamIndex: int = -1):
		self.teamIndex: int = teamIndex

	def __copy__(self):
		return Piece(teamIndex = self.teamIndex)

	def copy(self):
		return copy.copy(self)
	
	def getAttributesAsDict(self) -> Dict:
		return self.__dict__

	def populateAttributesFromDict(self, fromDict: dict) -> None:
		for key in fromDict:
			attributeValue = getattr(self, key, None)
			if attributeValue is not None:
				setattr(self, key, fromDict[key])

	def getPossibleMoves(self, _board, cellIndex: int) -> List[int]:
		return []
	