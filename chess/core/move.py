from typing import Optional
from .util import is_en_passant
from .piece import Piece
from .square import Square

class Move:
    """Represents a move from a starting Square to an end Square."""
    from_: Square
    to_: Square
    previous_en_passant_square: Optional[Square]
    captured_piece: Optional[Piece]
    def __init__(self, from_: Square, to_: Square, previous_en_passant_square: Optional[Square]):
        self.from_ = from_
        self.to_ = to_
        self.previous_en_passant_square = previous_en_passant_square
        self.captured_piece = to_.piece

    def __repr__(self) -> str:
        return f"From {str(self.from_)} To {str(self.to_)}\n"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Move):
            return (self.from_ == other.from_) and (self.to_ == other.to_)
        return NotImplemented

class PawnMove(Move):
    capture_square: Square
    promotion_piece: Optional[Piece]
    def __init__(self, from_: Square, to_: Square, previous_en_passant_square: Optional[Square], capture_square: Square = None, promotion_piece: Piece = None):
        super().__init__(from_, to_, previous_en_passant_square)
        self.promotion_piece = promotion_piece
        if is_en_passant(to_, previous_en_passant_square):
            # print("en-passant!")
            pass
        if capture_square is None:
            self.capture_square = to_
            self.captured_piece = to_.piece
        else:
            # specify different capture square. Used for en-passant.
            self.capture_square = capture_square
            self.captured_piece = capture_square.piece

    def __repr__(self) -> str:
        move_str = f"From {str(self.from_)} To {str(self.to_)}\n"
        if self.capture_square != self.to_:
            move_str += f"Captured {self.captured_piece}"
        return move_str

    def __eq__(self, other: object) -> bool:
        if isinstance(other, PawnMove):
            return (self.from_ == other.from_) and (self.to_ == other.to_) and (self.promotion_piece == other.promotion_piece)
        return NotImplemented