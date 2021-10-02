from typing import Optional
from .square import Square

def is_en_passant(to_square: Square, en_passant_square: Optional[Square]) -> bool:
    return to_square == en_passant_square