from board import Board, read_chess_notation
from piece import Piece, PieceType
from move import Move

class Game:
    # [Rank][File]
    board: Board
    # [K,Q,R,B,N,P][WHITE, BLACK][NUMBER]
    pieces: list[list[list[Piece]]] = [[[] for _ in range(2)] for _ in range(6)]
    move_log: list[Move] = []
    # State variables
    fullmove_number: int = 1
    halfmove_number: int = 0
    # Captured pieces

    def __init__(self, fen: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
        # TODO: verify fen
        self.setup_from_fen(fen)
        print(self.board)

    def setup_from_fen(self, fen: str) -> None:
        # rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
        fen = fen.split()
        self.fullmove_number = int(fen.pop())
        self.halfmove_number = int(fen.pop())
        self.board = Board(fen)

    def _load_pieces(self) -> None:
        for rank in self.board.state:
            for square in rank:
                if square.piece is not None:
                    square.piece.piece_id = len(self.pieces[square.piece.type][square.piece.colour])
                    self.pieces[square.piece.type][square.piece.colour].append(square.piece)

    def undo_move(self) -> None:
        self.board.undo_move()

    def move_from_notation(self, from_position: str, to_position: str) -> None:
        from_rank, from_file = read_chess_notation(from_position)
        to_rank, to_file = read_chess_notation(to_position)
        self.move_from_position(from_rank, from_file, to_rank, to_file)

    def move_from_position(self, from_rank: int, from_file: int, to_rank: int, to_file: int) -> None:
        from_ = self.board.state[from_rank][from_file]
        to_ = self.board.state[to_rank][to_file]
        move = Move(from_, to_)
        # TODO: try piece_ty is PieceType.PAWN
        if self.board.en_passant_square == to_ and from_.piece.piece_type == PieceType.PAWN:
            self.board.encode_en_passant(move)
        self.board.try_move(move)
