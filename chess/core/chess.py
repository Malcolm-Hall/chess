from core.util import is_en_passant
from core.board import Board, read_chess_notation, is_pawn_promotion, encode_pawn_promotion
from core.piece import PieceType
from core.move import Move, PawnMove


class Chess:
    # [Rank][File]
    board: Board
    # State variables
    fullmove_number: int = 1
    halfmove_number: int = 0
    def __init__(self, fen: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
        # TODO: verify fen
        self.setup_from_fen(fen)
        print(self.board)

    def setup_from_fen(self, fen: str) -> None:
        # rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
        fen_split = fen.split()
        self.fullmove_number = int(fen_split.pop())
        self.halfmove_number = int(fen_split.pop())
        self.board = Board(fen_split)

    def undo_move(self) -> None:
        # Todo: undo logic involving fullmove and halfmove number
        self.board.undo_move()

    def move_from_notation(self, from_position: str, to_position: str) -> None:
        from_rank, from_file = read_chess_notation(from_position)
        to_rank, to_file = read_chess_notation(to_position)
        self.move_from_position(from_rank, from_file, to_rank, to_file)

    def move_from_position(self, from_rank: int, from_file: int, to_rank: int, to_file: int, promotion_piece: PieceType = PieceType.QUEEN) -> bool:
        from_ = self.board.state[from_rank][from_file]
        to_ = self.board.state[to_rank][to_file]
        move: Move
        if from_.piece is None:
            return False
        if from_.piece.piece_type == PieceType.PAWN:
            move = PawnMove(from_, to_, self.board.en_passant_square)
            if is_pawn_promotion(to_.rank, from_.piece.colour_type):
                encode_pawn_promotion(move, promotion_piece)
            if is_en_passant(to_, self.board.en_passant_square) and from_.piece.piece_type == PieceType.PAWN:
                captured_piece = self.board.get_en_passant_captured_piece()
                move.captured_piece = captured_piece
        else:
            move = Move(from_, to_, self.board.en_passant_square)

        return self.board.try_move(move)
