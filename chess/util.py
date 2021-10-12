from typing import Optional

from constants import FILE_NOTATION
from constants import RANK_NOTATION
from core.piece import ColourType
from core.piece import Piece
from core.piece import PieceType
from core.square import Square


def read_chess_notation(position: str) -> Square:
    """Convert chess notation into a Square with a rank and file."""
    assert len(position) == 2, "Invalid notation"
    return Square(RANK_NOTATION[position[1:2]], FILE_NOTATION[position[:1]])


def is_pawn_promotion(to_rank: int, piece: Optional[Piece]) -> bool:
    """Returns a bool indicating whether a piece moving to a given rank is a pawn and promoting."""
    if piece is None or piece.piece_type != PieceType.PAWN:
        return False
    if piece.colour_type == ColourType.WHITE:
        return to_rank == 7
    else:
        return to_rank == 0


def is_en_passant(piece_type: PieceType, to_square: Square, en_passant_square: Optional[Square]) -> bool:
    """Returns a bool indicating whether a piece is a pawn performing en-passant."""
    return piece_type == PieceType.PAWN and to_square == en_passant_square
