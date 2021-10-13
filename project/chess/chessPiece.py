from typing import Dict, List
import functools

from chess.piece import Piece
import chess.chessBoard

class ChessPiece(Piece):
	def __init__(self, teamIndex: int = -1, moveCount = 0):
		super().__init__(teamIndex, moveCount)
	
	def __copy__(self):
		return ChessPiece(teamIndex = self.teamIndex, moveCount = self.moveCount)

	# Most chess pieces will just use all possible target cells that have
	# opponents in them, as most of them just move.	
	def getPossibleAttackCellIndices(self, _board, cellIndex: int) -> List[int]:
		board: chess.chessBoard.ChessBoard = _board
		possibleTargetCellIndices = self.getPossibleTargetCellIndices(board, cellIndex)
		return list(filter(lambda cellIndex: board.doesCellHaveOpponentPiece(cellIndex, self.teamIndex), possibleTargetCellIndices))

	def getPieceActionsFromTargetCell(self, _board, activeCellIndex: int, targetCellIndex: int) -> List[dict]:
		board: chess.chessBoard.ChessBoard = _board
		return board.getMovePieceActions(activeCellIndex, targetCellIndex)

class PawnChessPiece(ChessPiece):
	def __init__(self):
		super().__init__()

	def getPossibleTargetCellIndices(self, _board, cellIndex: int) -> List[int]:
		possibleTargetCellIndices: list[int] = []

		board: chess.chessBoard.ChessBoard = _board
		cellCoordinates = board.getCellCoordinatesFromIndex(cellIndex)

		# Move forward
		moveDirection = self.getPrimaryDirection()
		
		moveDistance = 2 if self.getRank(board, cellCoordinates) == 2 else 1

		rayCells = board.getCellsFromRay(cellCoordinates, moveDirection, moveDistance)
		possibleTargetCellIndices += list(filter(lambda cellIndex: board.isCellEmpty(cellIndex), rayCells))
		
		# Attack forward left
		moveDirection[0] = -1
		rayCells = board.getCellsFromRay(cellCoordinates, moveDirection, 1)
		possibleTargetCellIndices += list(filter(lambda cellIndex: board.doesCellHaveOpponentPiece(cellIndex, self.teamIndex), rayCells))

		# Attack forward right
		moveDirection[0] = 1
		rayCells = board.getCellsFromRay(cellCoordinates, moveDirection, 1)
		possibleTargetCellIndices += list(filter(lambda cellIndex: board.doesCellHaveOpponentPiece(cellIndex, self.teamIndex), rayCells))

		# Check for en passant.
		enPassantTargetCellIndex = self.getEnPassantTargetCellIndex(_board, cellCoordinates)
		if enPassantTargetCellIndex > -1:
			possibleTargetCellIndices.append(enPassantTargetCellIndex)

		return possibleTargetCellIndices
	
	def getPieceActionsFromTargetCell(self, _board, activeCellIndex: int, targetCellIndex: int) -> List[dict]:
		board: chess.chessBoard.ChessBoard = _board

		if targetCellIndex == self.getEnPassantTargetCellIndex(board, board.getCellCoordinatesFromIndex(activeCellIndex)):
			return self.getPieceActionsFromEnPassant(board, activeCellIndex, targetCellIndex)

		# Check for promotion.
		pieceActions = board.getMovePieceActions(activeCellIndex, targetCellIndex)
		if self.getRank(board, board.getCellCoordinatesFromIndex(targetCellIndex)) == 8:
			pieceActions += self.getPieceActionsFromPawnPromotion(board, targetCellIndex)
				
		return pieceActions

	def getPrimaryDirection(self) -> List[int]:
		direction = [0, 1]
		if self.teamIndex == 0:
			direction[1] *= -1
		
		return direction

	def getRank(self, _board, cellCoordinates: List[int]) -> int:
		board: chess.chessBoard.ChessBoard = _board
		return board.cellHeight - cellCoordinates[1] if self.teamIndex == 0 else cellCoordinates[1] + 1

	def getEnPassantTargetCellIndex(self, _board, cellCoordinates: List[int]) -> int:
		board: chess.chessBoard.ChessBoard = _board
		
		# Get last piece to move.
		numberOfPieceActionsInHistory = len(board.pieceActionHistory)
		if numberOfPieceActionsInHistory == 0:
			return -1
		
		lastPieceAction = board.pieceActionHistory[numberOfPieceActionsInHistory - 1]
		
		if lastPieceAction["type"] != chess.chessBoard.BoardPieceActionType.MOVE_TO_CELL:
			return -1

		# It needs to be a pawn.
		lastMovedPieceTypeId = lastPieceAction["pieceTypeId"]
		if lastMovedPieceTypeId != board.pieceSet.getTypeIdFromPieceType(PawnChessPiece):
			return -1

		# It cannot have moved more than once.
		lastMovedPieceCellIndex = lastPieceAction["toCellIndex"]
		lastMovedPawn: PawnChessPiece = board.getPieceFromCell(lastMovedPieceCellIndex)
		if lastMovedPawn.moveCount > 1:
			return -1

		# It needs to be at rank 4.
		# TODO: Is it better to make sure its only moved 2 cells at once
		# (checking fromCellIndex and vertical distance),
		# in order to allow for alternate starting piece formations?
		# Would want to change associated logic with first move rules to match.
		lastMovedPieceCellCoordinates = board.getCellCoordinatesFromIndex(lastMovedPieceCellIndex)
		if lastMovedPawn.getRank(board, lastMovedPieceCellCoordinates) != 4:
			return -1

		# It needs to be directly to the left or right of this pawn.
		distance = board.getDistanceBetweenCellCoordinates(cellCoordinates, lastMovedPieceCellCoordinates)
		if distance[1] > 0 or distance[0] > 1:
			return -1

		# Pawn move & en passant rules implicate that the cell directly behind
		# the captured pawn will be empty.
		# Assume it's a legit cell that can be moved into.
		primaryDirection = self.getPrimaryDirection()
		enPassantToCoordinates = [
			lastMovedPieceCellCoordinates[0],
			lastMovedPieceCellCoordinates[1] + primaryDirection[1]
		]
		
		return board.getCellIndexFromCoordinates(enPassantToCoordinates)

	def getPieceActionsFromEnPassant(self, _board, activeCellIndex: int, targetCellIndex: int) -> List[dict]:
		board: chess.chessBoard.ChessBoard = _board
		
		# NOTE: Assumes piece is a pawn.
		pawnPiece: PawnChessPiece = self

		# NOTE: Assumes en passant is possible.
		pawnFromCellCoordinates = board.getCellCoordinatesFromIndex(activeCellIndex)
		pawnToCellCoordinates = board.getCellCoordinatesFromIndex(targetCellIndex)
		otherPawnCellCoordinates = [
			pawnToCellCoordinates[0],
			pawnFromCellCoordinates[1]
		]

		otherPawnRemovePieceActions = board.getRemovePieceActions(board.getCellIndexFromCoordinates(otherPawnCellCoordinates))
		movePawnPieceActions = board.getMovePieceActions(activeCellIndex, targetCellIndex)

		return otherPawnRemovePieceActions + movePawnPieceActions

	def getPieceActionsFromPawnPromotion(self, _board, cellIndex: int) -> List[dict]:
		board: chess.chessBoard.ChessBoard = _board

		pieceActions = board.getRemovePieceActions(cellIndex, board.pieceSet.getTypeIdFromPieceType(type(self)))
		
		pieceAttributes = {
				"teamIndex": self.teamIndex
			}
		
		pieceActions += board.getAddPieceActions(cellIndex, board.pieceSet.getTypeIdFromPieceType(QueenChessPiece), pieceAttributes)

		return pieceActions

class RookChessPiece(ChessPiece):
	def __init__(self):
		super().__init__()
	
	def getPossibleTargetCellIndices(self, _board, cellIndex: int) -> List[int]:
		possibleTargetCellIndices: list[int] = []

		board: chess.chessBoard.ChessBoard = _board
		cellCoordinates = board.getCellCoordinatesFromIndex(cellIndex)

		moveDistance = max(board.cellWidth, board.cellHeight)

		moveDirections = [
			[0, -1],
			[1, 0],
			[0, 1],
			[-1, 0]
		]

		for moveDirection in moveDirections:
			rayCells = board.getCellsFromRay(cellCoordinates, moveDirection, moveDistance)
			possibleTargetCellIndices += list(filter(lambda cellIndex: board.isCellEmpty(cellIndex) or board.doesCellHaveOpponentPiece(cellIndex, self.teamIndex), rayCells))

		return possibleTargetCellIndices

class KnightChessPiece(ChessPiece):
	def __init__(self):
		super().__init__()
	
	def getPossibleTargetCellIndices(self, _board, cellIndex: int) -> List[int]:
		possibleTargetCellIndices: list[int] = []

		board: chess.chessBoard.ChessBoard = _board
		cellCoordinates = board.getCellCoordinatesFromIndex(cellIndex)

		moveOffsets = [
			[-1, -2],
			[1, -2],
			[2, -1],
			[2, 1],
			[1, 2],
			[-1, 2],
			[-2, 1],
			[-2, -1]
		]

		for moveOffset in moveOffsets:
			moveCellCoordinates = cellCoordinates.copy()
			moveCellCoordinates[0] += moveOffset[0]
			moveCellCoordinates[1] += moveOffset[1]
			if not board.areCellCoordinatesOnBoard(moveCellCoordinates):
				continue

			possibleTargetCellIndices.append(board.getCellIndexFromCoordinates(moveCellCoordinates))

		possibleTargetCellIndices = list(filter(lambda cellIndex: board.isCellEmpty(cellIndex) or board.doesCellHaveOpponentPiece(cellIndex, self.teamIndex), possibleTargetCellIndices))

		return possibleTargetCellIndices

class BishopChessPiece(ChessPiece):
	def __init__(self):
		super().__init__()
	
	def getPossibleTargetCellIndices(self, _board, cellIndex: int) -> List[int]:
		possibleTargetCellIndices: list[int] = []

		board: chess.chessBoard.ChessBoard = _board
		cellCoordinates = board.getCellCoordinatesFromIndex(cellIndex)

		moveDistance = max(board.cellWidth, board.cellHeight)

		moveDirections = [
			[-1, -1],
			[1, -1],
			[-1, 1],
			[1, 1]
		]

		for moveDirection in moveDirections:
			rayCells = board.getCellsFromRay(cellCoordinates, moveDirection, moveDistance)
			possibleTargetCellIndices += list(filter(lambda cellIndex: board.isCellEmpty(cellIndex) or board.doesCellHaveOpponentPiece(cellIndex, self.teamIndex), rayCells))

		return possibleTargetCellIndices

class QueenChessPiece(ChessPiece):
	def __init__(self):
		super().__init__()
	
	def getPossibleTargetCellIndices(self, _board, cellIndex: int) -> List[int]:
		possibleTargetCellIndices: list[int] = []

		board: chess.chessBoard.ChessBoard = _board
		cellCoordinates = board.getCellCoordinatesFromIndex(cellIndex)

		moveDistance = max(board.cellWidth, board.cellHeight)

		moveDirections = [
			[0, -1],
			[1, 0],
			[0, 1],
			[-1, 0],
			[-1, -1],
			[1, -1],
			[-1, 1],
			[1, 1]
		]

		for moveDirection in moveDirections:
			rayCells = board.getCellsFromRay(cellCoordinates, moveDirection, moveDistance)
			possibleTargetCellIndices += list(filter(lambda cellIndex: board.isCellEmpty(cellIndex) or board.doesCellHaveOpponentPiece(cellIndex, self.teamIndex), rayCells))

		return possibleTargetCellIndices

class KingChessPiece(ChessPiece):
	def __init__(self):
		super().__init__()

	def getPossibleTargetCellIndices(self, _board, cellIndex: int) -> List[int]:
		possibleTargetCellIndices: list[int] = self.getPossibleMoveCellIndices(_board, cellIndex)
		possibleTargetCellIndices += self.getPossibleCastleTargetCellIndices(_board, cellIndex)
		return possibleTargetCellIndices

	def getPossibleMoveCellIndices(self, _board, cellIndex: int) -> List[int]:
		possibleMoveCellIndices: list[int] = []

		board: chess.chessBoard.ChessBoard = _board
		cellCoordinates = board.getCellCoordinatesFromIndex(cellIndex)

		moveDistance = 1

		moveDirections = [
			[0, -1],
			[1, 0],
			[0, 1],
			[-1, 0],
			[-1, -1],
			[1, -1],
			[-1, 1],
			[1, 1]
		]

		for moveDirection in moveDirections:
			rayCells = board.getCellsFromRay(cellCoordinates, moveDirection, moveDistance)
			possibleMoveCellIndices += list(filter(lambda cellIndex: board.isCellEmpty(cellIndex) or board.doesCellHaveOpponentPiece(cellIndex, self.teamIndex), rayCells))
		
		# TODO: Should result castle move cells be reported here?

		return possibleMoveCellIndices

	def getPossibleAttackCellIndices(self, _board, cellIndex: int) -> List[int]:
		board: chess.chessBoard.ChessBoard = _board
		possibleMoveCellIndices = self.getPossibleMoveCellIndices(board, cellIndex)
		return list(filter(lambda cellIndex: board.doesCellHaveOpponentPiece(cellIndex, self.teamIndex), possibleMoveCellIndices))

	def getPieceActionsFromTargetCell(self, _board, activeCellIndex: int, targetCellIndex: int) -> List[dict]:
		board: chess.chessBoard.ChessBoard = _board

		if self.isValidCastleTargetCell(board, activeCellIndex, targetCellIndex):
			return self.getPieceActionsFromCastle(board, activeCellIndex, targetCellIndex)

		return super().getPieceActionsFromTargetCell(board, activeCellIndex, targetCellIndex)

	def getPossibleCastleTargetCellIndices(self, _board, cellIndex: int) -> List[int]:
		possibleTargetCellIndices: list[int] = []
		
		board: chess.chessBoard.ChessBoard = _board

		if self.moveCount == 0:
			rookIndices = board.getAllRookIndices(self.teamIndex)
			for rookIndex in rookIndices:
				if self.isValidCastleTargetCell(board, cellIndex, rookIndex):
					possibleTargetCellIndices.append(rookIndex)
		
		return possibleTargetCellIndices

	def isValidCastleTargetCell(self, _board, cellIndex: int, targetCellIndex: int) -> bool:
		board: chess.chessBoard.ChessBoard = _board
		
		piece = board.getPieceFromCell(cellIndex)
		if piece is None or not isinstance(piece, KingChessPiece):
			return False
		
		if piece.moveCount > 0:
			return False
		
		targetPiece = board.getPieceFromCell(targetCellIndex)
		if targetPiece is None or not isinstance(targetPiece, RookChessPiece):
			return False
		
		if targetPiece.moveCount > 0:
			return False
		
		kingCellCoordinates = board.getCellCoordinatesFromIndex(cellIndex)
		rookCellCoordinates = board.getCellCoordinatesFromIndex(targetCellIndex)

		# Must be at same row.
		if kingCellCoordinates[1] != rookCellCoordinates[1]:
			return False

		moveDirection = board.getDirectionBetweenCellCoordinates(kingCellCoordinates, rookCellCoordinates)

		# Check if any of the cells between the king and the rook are not empty.
		rayCellIndices = board.getCellsFromRay(kingCellCoordinates, moveDirection)
		if targetCellIndex not in rayCellIndices:
			return False

		# Check if either of the two cells from the king to the rook would put this king into check.
		if len(rayCellIndices) < 2:
			return False
		
		rayCellIndices = rayCellIndices[:2]
		for rayCellIndex in rayCellIndices:
			if board.doesTargetCellPutTeamKingIntoCheck(cellIndex, rayCellIndex, piece.teamIndex):
				return False

		return True

	def getPieceActionsFromCastle(self, _board, activeCellIndex: int, targetCellIndex: int) -> List[dict]:
		board: chess.chessBoard.ChessBoard = _board
		
		# NOTE: Assumes piece is a king.
		kingPiece: KingChessPiece = self

		# NOTE: Assumes a castle is possible (isValidCastleTargetCell is True).
		kingCellCoordinates = board.getCellCoordinatesFromIndex(activeCellIndex)
		rookCellCoordinates = board.getCellCoordinatesFromIndex(targetCellIndex)

		moveDirection = board.getDirectionBetweenCellCoordinates(kingCellCoordinates, rookCellCoordinates)
		
		rookCellCoordinates[0] = kingCellCoordinates[0] + moveDirection[0] # Distance 1
		kingCellCoordinates[0] += (moveDirection[0] * 2) # Distance 2

		rookToCellIndex = board.getCellIndexFromCoordinates(rookCellCoordinates)
		kingToCellIndex = board.getCellIndexFromCoordinates(kingCellCoordinates)

		kingMovePieceActions = board.getMovePieceActions(activeCellIndex, kingToCellIndex)
		rookMovePieceActions = board.getMovePieceActions(targetCellIndex, rookToCellIndex)

		return rookMovePieceActions + kingMovePieceActions
	