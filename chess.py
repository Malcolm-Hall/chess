import copy
from enum import Enum
from chessErrors import *

                        #    WHITE, BLACK
UNICODE_PIECE_SYMBOLS = [["\u2654", "\u265A"], # King   |K
                         ["\u2655", "\u265B"], # Queen  |Q
                         ["\u2656", "\u265C"], # Rook   |R
                         ["\u2657", "\u265D"], # Bishop |B
                         ["\u2658", "\u265E"], # Knight |N
                         ["\u2659", "\u265F"]] # Pawn   |P

UNICODE_WHITE_SPACE = "\u3000"

FILE_NOTATION = {chr(i) : int(i-ord('A')) for i in range(ord('A'), ord('I'))}
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
    piece_id = None
    def __init__(self, piece_type: PieceType, colour_type: ColourType):
        self.piece_type = piece_type
        self.colour_type = colour_type

    def __repr__(self):
        return UNICODE_PIECE_SYMBOLS[self.piece_type.value][self.colour_type.value]

    def set_id(self, piece_id):
        self.piece_id = piece_id


chess_pieces = {"k": Piece(PieceType.KING, ColourType.WHITE)  , "q": Piece(PieceType.QUEEN, ColourType.WHITE),
                "r": Piece(PieceType.ROOK, ColourType.WHITE)  , "b": Piece(PieceType.BISHOP, ColourType.WHITE),
                "n": Piece(PieceType.KNIGHT, ColourType.WHITE), "p": Piece(PieceType.PAWN, ColourType.WHITE),

                "K": Piece(PieceType.KING, ColourType.BLACK)  , "Q": Piece(PieceType.QUEEN, ColourType.BLACK),
                "R": Piece(PieceType.ROOK, ColourType.BLACK)  , "B": Piece(PieceType.BISHOP, ColourType.BLACK),
                "N": Piece(PieceType.KNIGHT, ColourType.BLACK), "P": Piece(PieceType.PAWN, ColourType.BLACK)}

class Board:
    board = [[None for _ in range(8)] for _ in range(8)]
    # [K,Q,R,B,N,P][WHITE, BLACK][NUMBER]
    pieces = [[[] for _ in range(2)] for _ in range(6)]
    fullmove_number = 1
    halfmove_number = 0
    en_passant_square = None
    castling_rights = "KQkq"
    turn = ColourType.WHITE

    def __init__(self, fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
        self.read_fen(fen)
        print(self)

    def __repr__(self):
        board_str = ""
        for rank in reversed(self.board):
            board_str += "|"
            for piece in rank:
                if piece is None:
                    board_str += UNICODE_WHITE_SPACE + "|"
                else:
                    board_str += str(piece) + "|"
            board_str += "\n"
        return board_str

    def read_fen(self, fen):
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

        self._id_pieces()

    def _read_board_fen(self, board_fen):
        ranks = board_fen.split("/")
        for rank, pieces in enumerate(ranks):
            file = 0
            for char in pieces:
                if char in [str(i) for i in range(1, 9)]:
                    file += int(char)
                else:
                    next_piece = copy.deepcopy(chess_pieces[char])
                    self.pieces[next_piece.piece_type.value][next_piece.colour_type.value].append(next_piece)
                    self.board[rank][file] = next_piece
                    file +=1

    def _id_pieces(self):
        for type_ in self.pieces:
            for colour in type_:
                for i, piece in enumerate(colour):
                    piece.set_id(i)

    def make_move(self, from_, to_):
        from_file, from_rank = FILE_NOTATION[from_[:1]], RANK_NOTATION[from_[1:2]]
        to_file, to_rank = FILE_NOTATION[to_[:1]], RANK_NOTATION[to_[1:2]]
        piece_to_move = self.board[from_rank][from_file]
        where_to_move = self.board[to_rank][to_file]
        # check the move makes sense
        if piece_to_move is None:
            raise PieceIsNoneError()
        if piece_to_move.colour_type != self.turn:
            raise NotYourTurnError()
        if where_to_move is not None and where_to_move.colour_type == self.turn:
            raise SameColourCaptureError()
        # check the move is legal

        # make the move
        self.board[to_rank][to_file] = piece_to_move
        self.board[from_rank][from_file] = None
        self.turn = ColourType.WHITE if self.turn == ColourType.BLACK else ColourType.BLACK
        print(self)