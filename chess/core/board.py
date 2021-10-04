import copy
from typing import Optional
from constants import UNICODE_WHITE_SPACE, FILE_NOTATION, RANK_NOTATION, PIECE_STRS
from core.util import is_en_passant
from core.piece import PieceType, ColourType, CHESS_PIECES
from core.move import Move, Square, PawnMove
from core.potential_move import PotentialMove, PawnPotentialMove, POTENTIAL_MOVES

def read_chess_notation(position: str) -> tuple[int,int]:
    return RANK_NOTATION[position[1:2]], FILE_NOTATION[position[:1]]

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

def is_pawn_promotion(to_rank: int, pawn_colour: ColourType) -> bool:
    if pawn_colour == ColourType.WHITE:
        return to_rank == 7
    else:
        return to_rank == 0

def is_double_step(from_rank: int, to_rank: int) -> bool:
    return abs(from_rank - to_rank) == 2

def encode_pawn_promotion(move: PawnMove, promotion_piece_type: PieceType) -> None:
    piece_str = PIECE_STRS[promotion_piece_type.value][move.moved_piece.colour_value]
    move.promotion_piece = copy.deepcopy(CHESS_PIECES[piece_str])

def en_passant_capture_rank(colour: ColourType) -> int:
    if colour == ColourType.WHITE:
        return 4
    else:
        return 3

def en_passant_square_rank(colour: ColourType) -> int:
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
                board_str += "|" + (str(square.piece) if square.piece is not None else UNICODE_WHITE_SPACE)
            board_str += "|\n"
        return board_str
    
    # todo: add to PawnMove class or separate out
    def encode_en_passant(self, move: PawnMove) -> None:
        if move.moved_piece.colour_type == ColourType.WHITE:
            move.capture_square = self.state[move.to_.rank-1][move.to_.file]
        else:
            move.capture_square = self.state[move.to_.rank+1][move.to_.file]
        move.captured_piece = move.capture_square.piece

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
        # move is assumed to be legal
        if isinstance(move, PawnMove):
            if is_pawn_promotion(move.to_.rank, move.moved_piece.colour_type):
                move.to_.piece = move.promotion_piece
                move.from_.piece = None
            elif is_en_passant(move.to_, self.en_passant_square):
                move.to_.piece = move.moved_piece
                capture_rank = en_passant_capture_rank(move.moved_piece.colour_type)
                capture_square = self.state[capture_rank][move.to_.file]
                capture_square.piece = None
                move.from_.piece = None
            else:
                move.to_.piece = move.moved_piece
                move.from_.piece = None
        else:
            move.to_.piece = move.moved_piece
            move.from_.piece = None
        # Update en-passant square
        if isinstance(move, PawnMove) and is_double_step(move.to_.rank, move.from_.rank):
                en_passant_rank = en_passant_square_rank(move.moved_piece.colour_type)
                self.en_passant_square = self.state[en_passant_rank][move.to_.file]
        else:
            self.en_passant_square = None
        # Mark move as made and update the turn
        self.move_log.append(move)
        self.turn = ColourType.WHITE if move.moved_piece.colour_type == ColourType.BLACK else ColourType.BLACK

    def undo_move(self) -> None:
        try:
            move = self.move_log.pop()
        except IndexError as idx_err:
            print("No moves to undo!")
        else:
            if isinstance(move, PawnMove):
                if is_pawn_promotion(move.to_.rank, move.moved_piece.colour_type):
                    move.from_.piece = move.moved_piece
                    move.to_.piece = move.captured_piece
                elif is_en_passant(move.to_, move.previous_en_passant_square):
                    move.from_.piece = move.moved_piece
                    capture_rank = en_passant_capture_rank(move.moved_piece.colour_type)
                    capture_square = self.state[capture_rank][move.to_.file]
                    capture_square.piece = move.captured_piece
                    move.to_.piece = None
                else:
                    move.from_.piece = move.moved_piece
                    move.to_.piece = move.captured_piece
            else:
                move.from_.piece = move.moved_piece
                move.to_.piece = move.captured_piece
            # Revert the en-passant square
            self.en_passant_square = move.previous_en_passant_square
            # Update the turn
            self.turn = ColourType.WHITE if move.moved_piece.colour_type == ColourType.WHITE else ColourType.BLACK


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
        valid_moves: list[Move] = []
        for potential_move in POTENTIAL_MOVES[square.piece.type_value]:
            # check pawn for en-passant and capture
            if square.piece.piece_type == PieceType.PAWN:
                valid_moves += self._handle_pawn_moves(square, potential_move)
            else:
                valid_moves += self._handle_non_pawn_moves(square, potential_move)
        return valid_moves

    def _handle_pawn_moves(self, from_square: Square, potential_move: PawnPotentialMove) -> list[PawnMove]:
        valid_moves = []
        rank_change, file_change = potential_move.get_rank_file_change(from_square.piece.colour_type)
        # loop till off board, hit piece or max range
        for i in potential_move.range():
            to_rank, to_file = from_square.rank + i * rank_change, from_square.file + i * file_change
            if is_off_board(to_rank, to_file):
                break
            to_square = self.state[to_rank][to_file]
            if is_pawn_promotion(to_rank, from_square.piece.colour_type):
                for piece_type in PieceType:
                    if piece_type == PieceType.KING or piece_type == PieceType.PAWN:
                        continue
                    move = PawnMove(from_square, to_square, self.en_passant_square)
                    encode_pawn_promotion(move, piece_type)
                    valid_moves += self._check_pawn_move(move, potential_move)
            elif is_en_passant(to_square, self.en_passant_square):
                move = PawnMove(from_square, to_square, self.en_passant_square)
                self.encode_en_passant(move)
                valid_moves += self._check_pawn_move(move, potential_move)
            else:
                move = PawnMove(from_square, to_square, self.en_passant_square)
                valid_moves += self._check_pawn_move(move, potential_move)
        return valid_moves

    def _check_pawn_move(self, move: PawnMove, potential_move: PawnPotentialMove) -> list[PawnMove]:
        # check capture moves make a capture of opponent piece
        if potential_move.capture and (move.captured_piece is None or move.captured_piece.colour_type == self.turn):
                return []
        # non-capture moves
        if not potential_move.capture:
            # check for blocking piece
            blocking_piece = move.to_.piece
            if blocking_piece is not None:
                return []
            # check if double move allowed
            if is_double_step(move.from_.rank, move.to_.rank):
                moved = (move.from_.rank != 1) if move.moved_piece.colour_type == ColourType.WHITE else (move.from_.rank != 6)
                if moved:
                    return []
        return [move]

    def _handle_non_pawn_moves(self, square: Square, potential_move: PotentialMove) -> list[Move]:
        valid_moves = []
        rank_change, file_change = potential_move.get_rank_file_change(square.piece.colour_type)
        # loop till off board, hit piece or max range
        for i in potential_move.range():
            new_rank, new_file = square.rank + i * rank_change, square.file + i * file_change
            if is_off_board(new_rank, new_file):
                break
            # check for blocking piece
            blocking_piece = self.state[new_rank][new_file].piece
            if blocking_piece is not None and blocking_piece.colour_type == square.piece.colour_type:
                # break immediately if same ColourType
                break
            new_square = self.state[new_rank][new_file]
            valid_moves.append(Move(square, new_square, self.en_passant_square))
            if blocking_piece is not None and blocking_piece.colour_type != square.piece.colour_type:
                # break after appending the move if opposite ColourType
                break
        return valid_moves

    def _brute_force_legal_moves(self):
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
