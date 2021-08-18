from enum import Enum
import constants

class ColourType(Enum):
    WHITE = 0
    BLACK = 1


class PieceType(Enum):
    KING = 0
    QUEEN = 1
    ROOK = 2
    BISHOP = 3
    KNIGHT = 4
    PAWN = 5


class Piece:
    piece_type: PieceType
    colour_type: ColourType
    piece_id: int
    def __init__(self, piece_type: PieceType, colour_type: ColourType):
        self.piece_type = piece_type
        self.colour_type = colour_type

    def __repr__(self) -> str:
        return constants.UNICODE_PIECE_SYMBOLS[self.piece_type.value][self.colour_type.value]

    def __eq__(self, other) -> bool:
        if isinstance(other, Piece):
            return (self.piece_type.value == other.piece_type.value) and (self.colour_type.value == other.colour_type.value)
        return False

    @property
    def type(self) -> int:
        return self.piece_type.value

    @property
    def colour(self) -> int:
        return self.colour_type.value


CHESS_PIECES = {"k": Piece(PieceType.KING, ColourType.WHITE)  , "q": Piece(PieceType.QUEEN, ColourType.WHITE),
                "r": Piece(PieceType.ROOK, ColourType.WHITE)  , "b": Piece(PieceType.BISHOP, ColourType.WHITE),
                "n": Piece(PieceType.KNIGHT, ColourType.WHITE), "p": Piece(PieceType.PAWN, ColourType.WHITE),

                "K": Piece(PieceType.KING, ColourType.BLACK)  , "Q": Piece(PieceType.QUEEN, ColourType.BLACK),
                "R": Piece(PieceType.ROOK, ColourType.BLACK)  , "B": Piece(PieceType.BISHOP, ColourType.BLACK),
                "N": Piece(PieceType.KNIGHT, ColourType.BLACK), "P": Piece(PieceType.PAWN, ColourType.BLACK)}

