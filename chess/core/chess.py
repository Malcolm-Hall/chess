from typing import Optional

from core.board import Board
from core.move import EnPassantMove
from core.move import Move
from core.move import PromotionMove
from core.piece import Piece
from core.piece import PieceType
from core.square import BoardSquare
from core.square import Square
from util import is_en_passant
from util import is_pawn_promotion
from util import read_chess_notation


class Chess:
    # [Rank][File]
    board: Board
    # State variables
    fullmove_number: int = 1
    halfmove_number: int = 0

    def __init__(self, fen: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
        # TODO: verify fen
        fen_split = fen.split()
        self.fullmove_number = int(fen_split.pop())
        self.halfmove_number = int(fen_split.pop())
        self.board = Board(fen_split)
        print(self.board)

    def undo_move(self) -> None:
        # TODO: logic involving fullmove and halfmove number
        self.board.undo_move()

    def move_from_notation(self, from_position: str, to_position: str) -> None:
        from_square = read_chess_notation(from_position)
        to_square = read_chess_notation(to_position)
        self.move_from_position(from_square, to_square)

    def move_from_position(self, from_square: Square, to_square: Square, promotion_piece_type: PieceType = PieceType.QUEEN) -> bool:
        from_ = self.get_board_square_at(from_square)
        to_ = self.get_board_square_at(to_square)
        if from_.piece is None:
            return False
        move: Move
        if is_pawn_promotion(to_.rank, from_.piece):
            move = PromotionMove(from_, to_, self.board.en_passant_square, promotion_piece_type)
        elif is_en_passant(from_.piece.piece_type, to_, self.board.en_passant_square):
            capture_square = self.board.get_en_passant_capture_square()
            move = EnPassantMove(from_, to_, self.board.en_passant_square, capture_square)
        else:
            move = Move(from_, to_, self.board.en_passant_square)
        return self.board.try_move(move)

    def get_board_square_at(self, square: Square) -> BoardSquare:
        return self.board.state[square.rank][square.file]

    def get_piece_at(self, square: Square) -> Optional[Piece]:
        board_square = self.get_board_square_at(square)
        return board_square.piece
