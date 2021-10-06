from typing import Optional
from constants import RANK_NOTATION, FILE_NOTATION
from core.square import Square
from core.piece import ColourType, PieceType, Piece

def read_chess_notation(position: str) -> tuple[int,int]:
    return RANK_NOTATION[position[1:2]], FILE_NOTATION[position[:1]]

def is_pawn_promotion(to_rank: int, piece: Piece) -> bool:
    if piece.piece_type != PieceType.PAWN:
        return False
    if piece.colour_type == ColourType.WHITE:
        return to_rank == 7
    else:
        return to_rank == 0

def is_en_passant(piece_type: PieceType, to_square: Square, en_passant_square: Optional[Square]) -> bool:
    return piece_type == PieceType.PAWN and to_square == en_passant_square