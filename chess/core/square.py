from typing import Optional

from core.piece import Piece


class Square:
    """Represents a square of a given rank and file."""
    rank: int
    file: int

    def __init__(self, rank: int, file: int):
        self.rank = rank
        self.file = file

    def __repr__(self) -> str:
        return f"Rank {self.rank} File {self.file}"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return (self.rank == other.rank) and (self.file == other.file)
        return NotImplemented


class BoardSquare(Square):
    """Represents a square of a chess board, which can be occupied by a piece."""
    rank: int
    file: int
    piece: Optional[Piece]

    def __init__(self, rank: int, file: int, piece: Piece = None):
        super().__init__(rank, file)
        self.piece = piece

    def __repr__(self) -> str:
        return f"Rank {self.rank} File {self.file} Piece {str(self.piece)}"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return (self.rank == other.rank) and (self.file == other.file) and (self.piece == other.piece)
        return NotImplemented
