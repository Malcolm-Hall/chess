import copy
from enum import Enum
from typing import Callable, Iterator, Union, Optional, List

from chessExceptions import *

# [Piece, Colour]            WHITE, BLACK
UNICODE_PIECE_SYMBOLS = [["\u2654", "\u265A"], # King   |K
                         ["\u2655", "\u265B"], # Queen  |Q
                         ["\u2656", "\u265C"], # Rook   |R
                         ["\u2657", "\u265D"], # Bishop |B
                         ["\u2658", "\u265E"], # Knight |N
                         ["\u2659", "\u265F"]] # Pawn   |P

UNICODE_WHITE_SPACE = "\u3000"
# ['A'...'H': 0...7]
FILE_NOTATION = {chr(i) : int(i - ord('A')) for i in range(ord('A'), ord('I'))}
# ['1'...'8': 0...7]
RANK_NOTATION = {str(i+1) : i for i in range(8)}

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
    rank: int
    file: int
    piece_id: int
    def __init__(self, piece_type: PieceType, colour_type: ColourType):
        self.piece_type = piece_type
        self.colour_type = colour_type

    def __repr__(self) -> str:
        return UNICODE_PIECE_SYMBOLS[self.piece_type.value][self.colour_type.value]

    @property
    def type(self) -> int:
        return self.piece_type.value

    @property
    def colour(self) -> int:
        return self.colour_type.value

chess_pieces = {"k": Piece(PieceType.KING, ColourType.WHITE)  , "q": Piece(PieceType.QUEEN, ColourType.WHITE),
                "r": Piece(PieceType.ROOK, ColourType.WHITE)  , "b": Piece(PieceType.BISHOP, ColourType.WHITE),
                "n": Piece(PieceType.KNIGHT, ColourType.WHITE), "p": Piece(PieceType.PAWN, ColourType.WHITE),

                "K": Piece(PieceType.KING, ColourType.BLACK)  , "Q": Piece(PieceType.QUEEN, ColourType.BLACK),
                "R": Piece(PieceType.ROOK, ColourType.BLACK)  , "B": Piece(PieceType.BISHOP, ColourType.BLACK),
                "N": Piece(PieceType.KNIGHT, ColourType.BLACK), "P": Piece(PieceType.PAWN, ColourType.BLACK)}

class Board:
    # [Rank][File]
    board: list[list[Optional[Piece]]] = [[None for _ in range(8)] for _ in range(8)]
    # [K,Q,R,B,N,P][WHITE, BLACK][NUMBER]
    pieces: list[list[list[Piece]]] = [[[] for _ in range(2)] for _ in range(6)]
    # Board state variables
    fullmove_number: int = 1
    halfmove_number: int = 0
    en_passant_square = None
    castling_rights = "KQkq"
    turn: ColourType = ColourType.WHITE

    def __init__(self, fen: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
        self._read_fen(fen)
        print(self)

    def __repr__(self) -> str:
        board_str = ""
        for rank in reversed(self.board):
            for piece in rank:
                board_str += "|" + (str(piece) if piece is not None else UNICODE_WHITE_SPACE)
            board_str += "|\n"
        return board_str

    def _read_fen(self, fen: str) -> None:
        # rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
        fen = fen.split()
        self.fullmove_number = int(fen.pop())
        self.halfmove_number = int(fen.pop())

        en_passant_fen = fen.pop()
        self.en_passant_square = None if en_passant_fen == "-" else en_passant_fen

        self.castling_rights = fen.pop()

        turn_fen = fen.pop()
        self.turn = ColourType.WHITE if turn_fen == "w" else ColourType.BLACK

        board_fen = fen.pop()
        self._read_board_fen(board_fen)


    def _read_board_fen(self, board_fen: str) -> None:
        ranks = board_fen.split("/")
        for rank, pieces in enumerate(ranks):
            file = 0
            for char in pieces:
                if char in [str(i) for i in range(1, 9)]:
                    file += int(char)
                else:
                    self._setup_piece(char, rank, file)
                    file +=1

    def _setup_piece(self, piece_fen: str, rank: int, file: int) -> None:
        piece = copy.deepcopy(chess_pieces[piece_fen])
        piece.rank, piece.file = rank, file
        piece.id = len(self.pieces[piece.type][piece.colour])
        self.pieces[piece.type][piece.colour].append(piece)
        self.board[rank][file] = piece

    def move(self, from_rank: int, from_file: int, to_rank: int, to_file: int) -> None:
        piece_to_move = self.board[from_rank][from_file]
        where_to_move = self.board[to_rank][to_file]
        # check the move makes sense
        if piece_to_move is None:
            raise PieceIsNoneException()
        if piece_to_move.colour_type != self.turn:
            raise NotYourTurnException()
        if where_to_move is not None and where_to_move.colour_type == self.turn:
            raise SameColourCaptureException()
        # check the move is legal

        # make the move
        piece_to_move.rank = to_rank
        piece_to_move.file = to_file
        self.board[to_rank][to_file] = piece_to_move
        self.board[from_rank][from_file] = None
        self.turn = ColourType.WHITE if self.turn == ColourType.BLACK else ColourType.BLACK
        print(self)

    def make_move(self, from_: str, to_: str) -> None:
        from_file, from_rank = FILE_NOTATION[from_[:1]], RANK_NOTATION[from_[1:2]]
        to_file, to_rank = FILE_NOTATION[to_[:1]], RANK_NOTATION[to_[1:2]]
        self.move(from_rank, from_file, to_rank, to_file)

