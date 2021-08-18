import copy
from typing import Optional
from chessExceptions import *
from piece import PieceType, ColourType, CHESS_PIECES
from move import Move, PotentialMove, PawnPotentialMove, POTENTIAL_MOVES, Square
from constants import UNICODE_WHITE_SPACE, FILE_NOTATION, RANK_NOTATION

def read_chess_notation(position: str) -> tuple[int,int]:
    return RANK_NOTATION[position[1:2]], FILE_NOTATION[position[:1]]

class Board:
    # [Rank][File]
    state: list[list[Square]] = [[None for _ in range(8)] for _ in range(8)]
    valid_moves: list[Move] = []
    legal_moves: list[Move] = []
    en_passant_square: Optional[Square] = None
    castling_rights = "KQkq"
    turn: ColourType = ColourType.WHITE
    move_log: list[Move] = []
    def __init__(self, fen: list[str]):
        fen.reverse()
        board_state_fen = fen.pop()
        self._set_board_state(board_state_fen)

        turn_fen = fen.pop()
        self.turn = ColourType.WHITE if turn_fen == "w" else ColourType.BLACK

        # TODO: handle castling
        self.castling_rights = fen.pop()

        en_passant_fen = fen.pop()
        if en_passant_fen != "-":
            en_passant_rank, en_passant_file = read_chess_notation(en_passant_fen)
            self.en_passant_square = self.state[en_passant_rank][en_passant_file]

    def __repr__(self) -> str:
        board_str = ""
        for rank in reversed(self.state):
            for square in rank:
                board_str += "|" + (str(square.piece) if square.piece is not None else UNICODE_WHITE_SPACE)
            board_str += "|\n"
        return board_str

    def _set_board_state(self, board_state_fen: str) -> None:
        ranks = board_state_fen.split("/")
        for rank, pieces in enumerate(ranks):
            file = 0
            for char in pieces:
                if char in [str(i) for i in range(1, 9)]:
                    self._setup_blank_squares(rank, file, int(char))
                    file += int(char)
                else:
                    self._setup_square(rank, file, char)
                    file += 1

    def _setup_blank_squares(self, rank: int, file: int, number: int) -> None:
        for _ in range(number):
            self._setup_square(rank, file)
            file += 1

    def _setup_square(self, rank: int, file: int, piece_fen: str = None) -> None:
        piece = None
        if piece_fen is not None:
            piece = copy.deepcopy(CHESS_PIECES[piece_fen])
        self.state[rank][file] = Square(rank, file, piece)

    def try_move(self, move: Move):
        try:
            self._check_move_is_legal(move)
            self._make_move(move)
            self.move_log.append(move)
            self.turn = ColourType.WHITE if self.turn == ColourType.BLACK else ColourType.BLACK
            self.legal_moves = []
            print(self)
        except InvalidMoveException as exc:
            print("Invalid Move")

    def undo_move(self) -> None:
        move = self.move_log.pop()
        move.from_.piece = move.to_.piece
        move.to_.piece = None
        move.capture_square.piece = move.captured_piece
        self.turn = move.from_.piece.colour_type
        print(self)

    def _check_move_is_legal(self, move: Move) -> None:
        # check the move makes sense
        if move.from_.piece is None:
            raise PieceIsNoneException()
        if move.from_.piece.colour_type != self.turn:
            raise NotYourTurnException()
        if move.to_.piece is not None and move.to_.piece.colour_type == self.turn:
            raise SameColourCaptureException()
        # generate legal moves
        if self.legal_moves == []:
            self._generate_legal_moves()
        # check if the move is legal
        if move not in self.legal_moves:
            print(self.legal_moves)
            raise IllegalMoveException()

    def _generate_legal_moves(self) -> None:
        self.legal_moves = [Move(self.state[1][0],self.state[2][0]), Move(self.state[0][1],self.state[2][2]), Move(self.state[7][1],self.state[5][2])]
        self.valid_moves = self._get_valid_moves()
        # TODO: Generate legal moves
        self.legal_moves = self.valid_moves

    def _make_move(self, move: Move) -> None:
        # handle double pawn moves
        if move.from_.piece.piece_type == PieceType.PAWN and (move.to_.rank - move.from_.rank) == 2:
            en_passant_rank = move.to_.rank - 1 if self.turn == ColourType.WHITE else move.to_.rank + 1
            self.en_passant_square = self.state[en_passant_rank][move.to_.file]
        move.to_.piece = move.from_.piece
        move.from_.piece = None
        # handle capture
        if move.capture_square != move.to_:
            print("en-passant!")
            move.capture_square.piece = None

    def _get_valid_moves(self) -> list[Move]:
        valid_moves = []
        for rank in self.state:
            for square in rank:
                if square.piece is not None and square.piece.colour_type == self.turn:
                    valid_moves += self._get_valid_moves_for_square(square)
        return valid_moves

    def _get_valid_moves_for_square(self, square: Square):
        valid_moves = []
        for potential_move in POTENTIAL_MOVES[square.piece.type]:
            # check pawn for en-passant and capture
            if square.piece.piece_type == PieceType.PAWN:
                valid_moves += self._handle_pawn_moves(square, potential_move)
            else:
                valid_moves += self._handle_other_moves(square, potential_move)
        return valid_moves

    def _handle_pawn_moves(self, square: Square, potential_move: PawnPotentialMove):
        rank_change, file_change = potential_move.get_rank_file_change(square.piece.colour_type)
        new_rank, new_file = square.rank + rank_change, square.file + file_change
        if self._off_board(new_rank, new_file):
            return []
        new_square = self.state[new_rank][new_file]
        move = Move(square, new_square)
        # capture moves
        if potential_move.capture:
            # en-passant
            if new_square == self.en_passant_square:
                self.encode_en_passant(move)
                return [move]
            # capture move but no capture piece
            if move.captured_piece is None:
                return []
        # non-capture moves
        else:
            # check for blocking piece
            blocking_piece = self.state[new_rank][new_file].piece
            if blocking_piece is not None:
                return []
            # check if double move allowed
            if abs(rank_change) > 1:
                moved = (square.rank != 1) if square.piece.colour_type == ColourType.WHITE else (square.rank != 6)
                if moved:
                    return []
        return [move]

    def _handle_other_moves(self, square: Square, potential_move: PotentialMove):
        valid_moves = []
        rank_change, file_change = potential_move.get_rank_file_change(square.piece.colour_type)
        # if arbitrary range: loop till hit piece
        for i in potential_move.range():
            new_rank, new_file = square.rank + i * rank_change, square.file + i * file_change
            # check if off board
            if self._off_board(new_rank, new_file):
                break
            # check for blocking piece
            blocking_piece = self.state[new_rank][new_file].piece
            if blocking_piece is not None and blocking_piece.colour_type == square.piece.colour_type:
                break
            new_square = self.state[new_rank][new_file]
            valid_moves.append(Move(square, new_square))
        return valid_moves

    def _off_board(self, rank, file):
        return rank < 0 or rank > len(self.state)-1 or file < 0 or file > len(self.state[0])-1

    def encode_en_passant(self, move: Move):
        if move.from_.piece.colour_type == ColourType.WHITE:
            move.capture_square = self.state[move.to_.rank-1][move.to_.file]
        else:
            move.capture_square = self.state[move.to_.rank+1][move.to_.file]
        move.captured_piece = move.capture_square.piece
