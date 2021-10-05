from typing import Optional
from core.square import Square
from core.piece import PieceType, Piece

def is_en_passant(piece_type: PieceType, to_square: Square, en_passant_square: Optional[Square]) -> bool:
    return piece_type == PieceType.PAWN and to_square == en_passant_square