from typing import Dict, List
from enum import Enum

from chess.piece import Piece
from chess.pieceSet import PieceSet

class BoardPieceActionType(Enum):
	REMOVE_FROM_CELL = 0,
	ADD_TO_CELL = 1,
	MOVE_TO_CELL = 2

class Board:
	def __init__(self, cellWidth: int, cellHeight: int, pieceSet):
		self.cellWidth = cellWidth
		self.cellHeight = cellHeight

		numberOfCells = self.getNumberOfCells()
		self.cellContents: list[list[Piece]] = [[]] * numberOfCells

		self.pieceSet: PieceSet = pieceSet

		self.pieceActionHistory: list[dict] = []

	def getNumberOfCells(self) -> int:
		return self.cellWidth * self.cellHeight

	def getCellCoordinatesFromIndex(self, cellIndex: int) -> List[int]:
		return [
			int(cellIndex % self.cellWidth),
			int(cellIndex / self.cellHeight)
		]

	def getCellIndexFromCoordinates(self, cellCoordinates: List[int]) -> int:
		if cellCoordinates[0] >= self.cellWidth:
			return -1

		if cellCoordinates[1] >= self.cellHeight:
			return -1

		return (cellCoordinates[1] * self.cellWidth) + cellCoordinates[0]

	def areCellCoordinatesOnBoard(self, cellCoordinates: List[int]) -> bool:
		if (cellCoordinates[0] < 0) or (cellCoordinates[0] >= self.cellWidth):
			return False
		
		if (cellCoordinates[1] < 0) or (cellCoordinates[1] >= self.cellHeight):
			return False
		
		return True

	def getCellContents(self, cellIndex: int):
		return self.cellContents[cellIndex]
	
	def setCellContents(self, cellIndex: int, cellContents: List) -> None:
		self.cellContents[cellIndex] = cellContents

	def clearCellContents(self, cellIndex: int) -> None:
		self.cellContents[cellIndex].clear()

	#def addPieceToCell(self, cellIndex: int, piece) -> None:
	#	self.cellContents[cellIndex].append(piece)

	# NOTE: This method assumes only one piece can be in cell.
	def getPieceFromCell(self, cellIndex: int):
		if self.isCellEmpty(cellIndex):
			return None
		
		piece: Piece = self.getCellContents(cellIndex)[0]
		return piece

	def isCellEmpty(self, cellIndex: int) -> bool:
		return len(self.getCellContents(cellIndex)) == 0

	def doesCellHaveOpponentPiece(self, cellIndex: int, teamIndex: int) -> bool:
		if not self.isCellEmpty(cellIndex):
			for _piece in self.getCellContents(cellIndex):
				piece: Piece = _piece
				if piece.teamIndex != teamIndex:
					return True
		
		return False

	def createCellContentsFromCharacter(self, character: str):
		cellContents: list[Piece] = []
		
		if character is '.':
			return cellContents
		
		cellContents.append(self.pieceSet.createPieceFromCharacter(character))
		return cellContents

	def loadFromStringRowList(self, stringRowList: List[str]) -> None:
		y = 0
		for stringRow in stringRowList:
			x = 0
			for character in stringRow:
				cellIndex = self.getCellIndexFromCoordinates([x, y])
				self.setCellContents(cellIndex, self.createCellContentsFromCharacter(character))
				x += 1
			y += 1

	def getStringRowList(self) -> List[str]:
		stringRows: List[str] = []
		
		for y in range(self.cellHeight):
			stringRow: str = ""
			for x in range(self.cellWidth):
				piece = self.getPieceFromCell(self.getCellIndexFromCoordinates([x, y]))
				character = '.' if piece is None else self.pieceSet.getCharacterFromPiece(piece)
				stringRow += character
			stringRows.append(stringRow)
		
		return stringRows

	def print(self) -> None:
		for stringRow in self.getStringRowList():
			print(stringRow)
		print("")

	def getValidTargetCellIndices(self, cellIndex: int) -> List[int]:
		piece = self.getPieceFromCell(cellIndex)
		if piece is None:
			print("getValidTargetCellIndices: Error")
			return []
		
		return piece.getPossibleTargetCellIndices(self, cellIndex)

	def isValidTargetCell(self, sourceCellIndex: int, targetCellIndex: int) -> bool:
		return targetCellIndex in self.getValidTargetCellIndices(sourceCellIndex)

	def getValidAttackCellIndices(self, cellIndex: int) -> List[int]:
		piece = self.getPieceFromCell(cellIndex)
		if piece is None:
			print("getValidAttackCellIndices: Error")
			return []
		
		return piece.getPossibleAttackCellIndices(self, cellIndex)

	def reversePieceActions(self, pieceActions: List[dict]) -> List[dict]:
		pieceActions.reverse()
		for pieceAction in pieceActions:
			pieceActionType: int = pieceAction["type"]
			if pieceActionType == BoardPieceActionType.REMOVE_FROM_CELL:
				pieceAction["type"] = BoardPieceActionType.ADD_TO_CELL
			elif pieceActionType == BoardPieceActionType.ADD_TO_CELL:
				pieceAction["type"] = BoardPieceActionType.REMOVE_FROM_CELL
			elif pieceActionType == BoardPieceActionType.MOVE_TO_CELL:
				fromCellIndex: int = pieceAction["fromCellIndex"]
				toCellIndex: int = pieceAction["toCellIndex"]
				pieceAction["toCellIndex"] = fromCellIndex
				pieceAction["fromCellIndex"] = toCellIndex
				if pieceAction["pieceTypeId"] > -1:
					moveCount = pieceAction["moveCount"]
					pieceAction["moveCount"] = moveCount - 1

		return pieceActions

	def executePieceActions(self, pieceActions: List[dict]) -> int:
		for pieceAction in pieceActions:
			pieceActionType: int = pieceAction["type"]
			if pieceActionType == BoardPieceActionType.ADD_TO_CELL:
				cellIndex: int = pieceAction["cellIndex"]
				pieceTypeId = pieceAction["pieceTypeId"]
				if pieceTypeId > -1:
					piece = self.pieceSet.createPieceFromTypeId(pieceTypeId)
					piece.populateAttributesFromDict(pieceAction)
					self.setCellContents(cellIndex, [piece])
			elif pieceActionType == BoardPieceActionType.REMOVE_FROM_CELL:
				cellIndex: int = pieceAction["cellIndex"]
				self.clearCellContents(cellIndex)
			elif pieceActionType == BoardPieceActionType.MOVE_TO_CELL:
				fromCellIndex: int = pieceAction["fromCellIndex"]
				toCellIndex: int = pieceAction["toCellIndex"]
				self.clearCellContents(fromCellIndex)
				pieceTypeId = pieceAction["pieceTypeId"]
				if pieceTypeId > -1:
					piece = self.pieceSet.createPieceFromTypeId(pieceTypeId)
					piece.populateAttributesFromDict(pieceAction)
					piece.moveCount += 1
					self.setCellContents(toCellIndex, [piece])
			else:
				print("Board::executePieceActions - Encountered unhandled BoardPieceActionType: " + str(pieceActionType))
		
		return 0

	def getRemovePieceActions(self, cellIndex: int) -> List[dict]:
		piece = self.getPieceFromCell(cellIndex)

		removeFromCellAction = {
			"type": BoardPieceActionType.REMOVE_FROM_CELL,
			"cellIndex": cellIndex,
			"pieceTypeId": -1 if piece is None else self.pieceSet.getTypeIdFromPieceType(type(piece))
		}

		if piece is not None:
			removeFromCellAction = {**removeFromCellAction, **piece.getAttributesAsDict()}
		
		return [removeFromCellAction]

	def getMovePieceActions(self, fromCellIndex: int, toCellIndex: int) -> List[dict]:
		pieceActions = self.getRemovePieceActions(toCellIndex)

		fromPiece = self.getPieceFromCell(fromCellIndex)
		addToCellAction = {
			"type": BoardPieceActionType.MOVE_TO_CELL,
			"fromCellIndex": fromCellIndex,
			"toCellIndex": toCellIndex,
			"pieceTypeId": -1 if fromPiece is None else self.pieceSet.getTypeIdFromPieceType(type(fromPiece))
		}

		if fromPiece is not None:
			addToCellAction = {**addToCellAction, **fromPiece.getAttributesAsDict()}
		
		pieceActions.append(addToCellAction)

		return pieceActions
	
	def getPieceActionsFromTargetCell(self, activeCellIndex: int, targetCellIndex: int) -> List[dict]:
		piece = self.getPieceFromCell(activeCellIndex)
		if piece is not None:
			return piece.getPieceActionsFromTargetCell(self, activeCellIndex, targetCellIndex)

		return []

	def performPieceAction(self, activeCellIndex: int, targetCellIndex: int) -> List[dict]:
		pieceActions = self.getPieceActionsFromTargetCell(activeCellIndex, targetCellIndex)
	
		self.executePieceActions(pieceActions)

		self.pieceActionHistory += pieceActions

		return pieceActions

	def rollbackPieceActions(self, pieceActions: List[dict]) -> None:
		# Reverse temporary move to restore board state.
		self.reversePieceActions(pieceActions)
		self.executePieceActions(pieceActions)

		self.pieceActionHistory = self.pieceActionHistory[:len(self.pieceActionHistory) - len(pieceActions)]
