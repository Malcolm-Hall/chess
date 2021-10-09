from typing import Optional

from core.piece import Piece


class Square:
    """Represents a square of a chess board of a given rank and file."""
    rank: int
    file: int
    piece: Optional[Piece]

    def __init__(self, rank: int, file: int, piece: Piece = None):
        self.rank = rank
        self.file = file
        self.piece = piece

    def __repr__(self) -> str:
        return f"Rank {self.rank} File {self.file} {str(self.piece)}"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Square):
            return (self.rank == other.rank) and (self.file == other.file) and (self.piece == other.piece)
        return NotImplemented
