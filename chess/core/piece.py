from enum import Enum

from constants import piece_str
from constants import UNICODE_PIECE_SYMBOLS


class ColourType(Enum):
    """The colour type of a piece"""
    WHITE = 0
    BLACK = 1


class PieceType(Enum):
    """The type of a piece"""
    KING = 0
    QUEEN = 1
    ROOK = 2
    BISHOP = 3
    KNIGHT = 4
    PAWN = 5


class Piece:
    """Represents a chess piece of a given type and colour"""
    piece_type: PieceType
    colour_type: ColourType

    def __init__(self, piece_type: PieceType, colour_type: ColourType):
        self.piece_type = piece_type
        self.colour_type = colour_type

    def __repr__(self) -> str:
        return UNICODE_PIECE_SYMBOLS[self.piece_type.value][self.colour_type.value]

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return (self.piece_type == other.piece_type) and (self.colour_type == other.colour_type)
        return NotImplemented

    @property
    def type_value(self) -> int:
        """Returns the type value of the piece. Used as an index for arrays"""
        return self.piece_type.value

    @property
    def colour_value(self) -> int:
        """Returns the colour value of the piece. Used as an index for arrays"""
        return self.colour_type.value


CHESS_PIECES: dict[piece_str, Piece] = {"k": Piece(PieceType.KING, ColourType.WHITE), "q": Piece(PieceType.QUEEN, ColourType.WHITE),
                                        "r": Piece(PieceType.ROOK, ColourType.WHITE), "b": Piece(PieceType.BISHOP, ColourType.WHITE),
                                        "n": Piece(PieceType.KNIGHT, ColourType.WHITE), "p": Piece(PieceType.PAWN, ColourType.WHITE),

                                        "K": Piece(PieceType.KING, ColourType.BLACK), "Q": Piece(PieceType.QUEEN, ColourType.BLACK),
                                        "R": Piece(PieceType.ROOK, ColourType.BLACK), "B": Piece(PieceType.BISHOP, ColourType.BLACK),
                                        "N": Piece(PieceType.KNIGHT, ColourType.BLACK), "P": Piece(PieceType.PAWN, ColourType.BLACK)}
