import copy
from typing import Optional

from constants import UNICODE_WHITE_SPACE
from core.move import EnPassantMove
from core.move import Move
from core.move import PromotionMove
from core.piece import CHESS_PIECES
from core.piece import ColourType
from core.piece import Piece
from core.piece import PieceType
from core.potential_move import PawnCapturePotentialMove
from core.potential_move import PawnStepPotentialMove
from core.potential_move import POTENTIAL_MOVES
from core.potential_move import PotentialMove
from core.square import Square
from util import is_en_passant
from util import is_pawn_promotion
from util import read_chess_notation


def get_board_state(board_state_fen: str) -> list[list[Square]]:
    state = [[Square(rank, file) for file in range(8)] for rank in range(8)]
    ranks = board_state_fen.split("/")
    for rank, pieces in enumerate(ranks):
        file = 0
        for char in pieces:
            if char in [str(i) for i in range(1, 9)]:
                file += int(char)
            else:
                piece = copy.deepcopy(CHESS_PIECES[char])
                state[rank][file].piece = piece
                file += 1
    return state


def is_off_board(rank: int, file: int) -> bool:
    return rank < 0 or rank > 7 or file < 0 or file > 7


def is_pawn_double_step(piece_type: PieceType, from_rank: int, to_rank: int) -> bool:
    return piece_type == PieceType.PAWN and abs(from_rank - to_rank) == 2


def pawn_has_moved(from_rank: int, colour: ColourType) -> bool:
    """
    Returns whether a pawn of a given colour has moved from the starting rank.
    Used to determine if a double-step move is allowed.
    """
    if colour == ColourType.WHITE:
        return from_rank != 1
    else:
        return from_rank != 6


def en_passant_capture_rank(colour: ColourType) -> int:
    """
    The rank in which en-passant capture occurs given the colour of the capturing piece.
    White captures black on rank 4
    Black captures white on rank 3
    """
    if colour == ColourType.WHITE:
        return 4
    else:
        return 3


def en_passant_square_rank(colour: ColourType) -> int:
    """
    The rank in which the next en-passant square exists given the colour of the moving piece.
    White double-stepping produces an en-passant square on rank 2
    Black double-stepping produces an en-passant square on rank 5
    """
    if colour == ColourType.WHITE:
        return 2
    else:
        return 5


class Board:
    # [Rank][File]
    state: list[list[Square]]
    valid_moves: list[Move] = []
    legal_moves: list[Move] = []
    en_passant_square: Optional[Square] = None
    castling_rights = "KQkq"
    turn: ColourType = ColourType.WHITE
    move_log: list[Move] = []

    def __init__(self, fen: list[str]):
        fen.reverse()
        board_state_fen = fen.pop()
        self.state = get_board_state(board_state_fen)

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
                board_str += "|" + (str(square.piece)
                                    if square.piece is not None else
                                    UNICODE_WHITE_SPACE)
            board_str += "|\n"
        return board_str

    def try_move(self, move: Move) -> bool:
        if self._move_is_legal(move):
            self._make_move(move)
            self.valid_moves = []
            self.legal_moves = []
            return True
        else:
            print("Illegal Move")
            # TODO: fix bug where can get stuck after inputing weird moves/ undoing moves
            # Regenerate legal moves as a temp fix
            self.legal_moves = []
            return False

    def _move_is_legal(self, move: Move) -> bool:
        if self.legal_moves == []:
            self._generate_legal_moves()
            # TODO: check for checkmate/stalemate
        return (move in self.legal_moves)

    def _make_move(self, move: Move) -> None:
        move.make()
        # Update en-passant square
        if is_pawn_double_step(move.moved_piece.piece_type, move.to_.rank, move.from_.rank):
            en_passant_rank = en_passant_square_rank(move.moved_piece.colour_type)
            self.en_passant_square = self.state[en_passant_rank][move.to_.file]
        else:
            self.en_passant_square = None
        # Mark move as made and update the turn
        self.move_log.append(move)
        self.turn = ColourType.WHITE if self.turn == ColourType.BLACK else ColourType.BLACK

    def undo_move(self) -> None:
        try:
            move = self.move_log.pop()
        except IndexError as idx_err:
            print("No moves to undo!")
        else:
            move.undo()
            # Revert the en-passant square
            self.en_passant_square = move.previous_en_passant_square
            # Update the turn
            self.turn = ColourType.WHITE if self.turn == ColourType.BLACK else ColourType.BLACK

    def _generate_legal_moves(self) -> None:
        self.valid_moves = self._get_valid_moves()
        # TODO: Generate legal moves more efficiently
        self.legal_moves = self._brute_force_legal_moves()

    def _get_valid_moves(self) -> list[Move]:
        valid_moves = []
        for rank in self.state:
            for square in rank:
                if square.piece is not None and square.piece.colour_type == self.turn:
                    valid_moves += self._get_valid_moves_for_square(square)
        return valid_moves

    def _get_valid_moves_for_square(self, square: Square) -> list[Move]:
        assert square.piece is not None
        valid_moves: list[Move] = []
        for potential_move in POTENTIAL_MOVES[square.piece.type_value]:
            # check pawn for en-passant and capture
            valid_moves += self._check_move(square, potential_move)
        return valid_moves

    def _check_move(self, from_square: Square, potential_move: PotentialMove) -> list[Move]:
        assert from_square.piece is not None
        valid_moves: list[Move] = []
        rank_change, file_change = potential_move.get_rank_file_change(from_square.piece.colour_type)
        # loop till off board, hit piece or max range
        for i in potential_move:
            to_rank, to_file = (from_square.rank + i * rank_change,
                                from_square.file + i * file_change)
            if is_off_board(to_rank, to_file):
                # TODO: use this to check if castling is legal
                break
            to_square = self.state[to_rank][to_file]
            if is_en_passant(from_square.piece.piece_type, to_square, self.en_passant_square):
                captured_piece = self.get_en_passant_captured_piece()
            else:
                captured_piece = to_square.piece

            if captured_piece is not None:
                # moves must not make a capture of the same colour
                if captured_piece.colour_type == self.turn:
                    break
                # pawn step moves must not make a capture
                if isinstance(potential_move, PawnStepPotentialMove):
                    break
            else:
                # pawn capture moves must make a capture
                if isinstance(potential_move, PawnCapturePotentialMove):
                    break

            # can't double-step if pawn has moved
            if is_pawn_double_step(from_square.piece.piece_type, from_square.rank, to_rank) and pawn_has_moved(from_square.rank, from_square.piece.colour_type):
                break
            move: Move
            if is_pawn_promotion(to_rank, from_square.piece):
                for piece_type in PieceType:
                    if piece_type == PieceType.KING or piece_type == PieceType.PAWN:
                        continue
                    move = PromotionMove(
                        from_square, to_square,
                        self.en_passant_square, piece_type)
                    valid_moves.append(move)
            elif is_en_passant(from_square.piece.piece_type, to_square, self.en_passant_square):
                move = EnPassantMove(
                    from_square, to_square, self.en_passant_square,
                    self.get_en_passant_capture_square())
                valid_moves.append(move)
            else:
                move = Move(from_square, to_square, self.en_passant_square)
                valid_moves.append(move)

            # break after appending the move if a capture occurs
            if captured_piece is not None and captured_piece.colour_type != self.turn:
                break

        return valid_moves

    def _brute_force_legal_moves(self) -> list[Move]:
        legal_moves = []
        for move in self.valid_moves:
            self._make_move(move)
            next_moves = self._get_valid_moves()
            legal = True
            for next_move in next_moves:
                if next_move.captured_piece is None or next_move.captured_piece.piece_type != PieceType.KING:
                    continue
                legal = False
                break
            if legal:
                legal_moves.append(move)
            self.undo_move()
        return legal_moves

    def get_en_passant_captured_piece(self) -> Optional[Piece]:
        """Returns the piece to be captured in an en-passant move, determined from which colours' turn it is."""
        assert self.en_passant_square is not None, "Function should only be called when there is an en-passant square"
        if self.turn == ColourType.WHITE:
            return self.state[self.en_passant_square.rank - 1][self.en_passant_square.file].piece
        else:
            return self.state[self.en_passant_square.rank + 1][self.en_passant_square.file].piece

    def get_en_passant_capture_square(self) -> Square:
        """Returns the square which contains the captured piece in an en-passant move, determined from which colours' turn it is."""
        assert self.en_passant_square is not None, "Function should only be called when there is an en-passant square"
        if self.turn == ColourType.WHITE:
            return self.state[self.en_passant_square.rank - 1][self.en_passant_square.file]
        else:
            return self.state[self.en_passant_square.rank + 1][self.en_passant_square.file]
