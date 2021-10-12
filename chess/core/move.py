from typing import Optional

from core.piece import Piece
from core.piece import PieceType
from core.square import BoardSquare


class Move:
    """Represents a generic move."""
    from_: BoardSquare
    to_: BoardSquare
    moved_piece: Piece
    captured_piece: Optional[Piece]
    previous_en_passant_square: Optional[BoardSquare]

    def __init__(self, from_: BoardSquare, to_: BoardSquare, previous_en_passant_square: Optional[BoardSquare]):
        assert from_.piece is not None, "A piece to move is required."
        self.from_ = from_
        self.to_ = to_
        self.moved_piece = from_.piece
        self.captured_piece = to_.piece
        self.previous_en_passant_square = previous_en_passant_square

    def __repr__(self) -> str:
        return f"From {str(self.from_)} | To {str(self.to_)}\n"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return (self.from_ == other.from_) and (self.to_ == other.to_)
        return NotImplemented

    def make(self) -> None:
        self.to_.piece = self.moved_piece
        self.from_.piece = None

    def undo(self) -> None:
        self.from_.piece = self.moved_piece
        self.to_.piece = self.captured_piece


class PromotionMove(Move):
    """Represents a move where a pawn promotes to a given PieceType."""
    promotion_piece: Piece

    def __init__(self, from_: BoardSquare, to_: BoardSquare, previous_en_passant_square: Optional[BoardSquare], promotion_piece_type: PieceType):
        super().__init__(from_, to_, previous_en_passant_square)
        self.promotion_piece = Piece(promotion_piece_type, self.moved_piece.colour_type)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return (self.from_ == other.from_) and (self.to_ == other.to_) and (self.promotion_piece == other.promotion_piece)
        return NotImplemented

    def make(self) -> None:
        self.to_.piece = self.promotion_piece
        self.from_.piece = None


class EnPassantMove(Move):
    """Represents a move where a pawn makes an en-passant capture."""
    capture_square: BoardSquare

    def __init__(self, from_: BoardSquare, to_: BoardSquare, previous_en_passant_square: Optional[BoardSquare], capture_square: BoardSquare):
        super().__init__(from_, to_, previous_en_passant_square)
        self.capture_square = capture_square
        self.captured_piece = capture_square.piece

    def __repr__(self) -> str:
        return f"From {str(self.from_)} | To {str(self.to_)} | Captured {str(self.capture_square)}\n"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return (self.from_ == other.from_) and (self.to_ == other.to_) and (self.capture_square == other.capture_square)
        return NotImplemented

    def make(self) -> None:
        super().make()
        self.capture_square.piece = None

    def undo(self) -> None:
        self.from_.piece = self.moved_piece
        self.capture_square.piece = self.captured_piece
        self.to_.piece = None
