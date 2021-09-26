from core.square import Square
import pyglet
from typing import Union, Optional
from constants import PIECE_STRS, UNICODE_PIECE_SYMBOLS
from core.piece import Piece, PieceType, ColourType, CHESS_PIECES
import core.chess
from core.board import is_pawn_promotion
from .piece import PieceSprite
from .layout import Layout

def board_generator(square_size, main_batch, board_group) -> list[pyglet.shapes.Rectangle]:
    return [pyglet.shapes.Rectangle(x=i*square_size, y=j*square_size,
                                    width=square_size, height=square_size,
                                    color=(240, 217, 181) if (i%2==0) != (j%2==0) else (148, 111, 81),
                                    batch=main_batch,
                                    group=board_group)
            for i in range(8) for j in range(8)]

def promotion_piece_generator(layout: Layout, white_promotion_batch, black_promotion_batch, overlay_group, promotion_group) -> list[Union[PieceSprite, pyglet.shapes.Rectangle]]:
    promotion_backgrounds = [pyglet.shapes.Rectangle(x=2 * layout.square_size,
                                                        y=(1 if colour.value else 6) * layout.square_size,
                                                        width=4 * layout.square_size, height=layout.square_size,
                                                        color=(100, 100, 200),
                                                        batch=white_promotion_batch if colour == ColourType.WHITE else black_promotion_batch,
                                                        group=overlay_group)
                                for colour in ColourType]
    promotion_pieces = [PieceSprite(str(piece_symbol),
                                    (i+2) * layout.square_size + layout.piece_offset[0],
                                    (1 if colour else 6) * layout.square_size + layout.piece_offset[1],
                                    font_size=layout.piece_size,
                                    batch=white_promotion_batch if colour == ColourType.WHITE.value else black_promotion_batch,
                                    group=promotion_group)
                        for i, piece_type in enumerate(UNICODE_PIECE_SYMBOLS[1:5]) for colour, piece_symbol in enumerate(piece_type)]
    return promotion_backgrounds + promotion_pieces

def piece_generator(board_state: list[list[Square]], layout: Layout, main_batch, pieces_group) -> list[list[Optional[PieceSprite]]]:
    return [[(PieceSprite(str(square.piece),
                            file * layout.square_size + layout.piece_offset[0],
                            rank * layout.square_size + layout.piece_offset[1],
                            font_size=layout.piece_size,
                            batch=main_batch,
                            group=pieces_group)
                if square.piece is not None else None)
                for file, square in enumerate(squares)] for rank, squares in enumerate(board_state)]


class Game(pyglet.window.Window):
    auto_queen: bool = False
    layout = Layout(512, 45, (5, 10))
    selected_squares: list[tuple[int, int]] = []
    main_batch = pyglet.graphics.Batch()
    board_group = pyglet.graphics.OrderedGroup(0)
    pieces_group = pyglet.graphics.OrderedGroup(1)
    white_promotion_batch = pyglet.graphics.Batch()
    black_promotion_batch = pyglet.graphics.Batch()
    overlay_group = pyglet.graphics.OrderedGroup(2)
    promotion_group = pyglet.graphics.OrderedGroup(3)
    board_sprites: list[pyglet.shapes.Rectangle]
    piece_sprites: list[list[Optional[PieceSprite]]]
    promotion_piece_sprites: list[PieceSprite]
    white_promotion: bool = False
    black_promotion: bool = False
    def __init__(self, fen: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
        super().__init__(self.layout.board_size, self.layout.board_size, caption="Chess")
        self.fpsDisplay = pyglet.window.FPSDisplay(window=self)
        self.chess = core.chess.Chess(fen)
        self.board_sprites = board_generator(self.layout.square_size, self.main_batch, self.board_group)
        self.piece_sprites = piece_generator(self.chess.board.state, self.layout, self.main_batch, self.pieces_group)
        self.promotion_piece_sprites = promotion_piece_generator(self.layout, self.white_promotion_batch, self.black_promotion_batch, self.overlay_group, self.promotion_group)

    def on_draw(self):
        self.clear()
        self.main_batch.draw()
        self.fpsDisplay.draw()
        if self.white_promotion:
            self.white_promotion_batch.draw()
            self.white_promotion = False
        elif self.black_promotion:
            self.black_promotion_batch.draw()
            self.black_promotion = False

    def on_mouse_press(self, x, y, button, modifiers):
        if button is pyglet.window.mouse.LEFT:
            clicked_file = int(x / self.layout.square_size)
            clicked_rank = int(y / self.layout.square_size)
            if self.selected_squares == []:
                if self.piece_sprites[clicked_rank][clicked_file] is not None:
                    self.selected_squares.append((clicked_rank, clicked_file))
                return
            elif len(self.selected_squares) < 2:
                if self.selected_squares[0] == (clicked_rank, clicked_file):
                    self.selected_squares = []
                    return
                (piece_rank, piece_file) = self.selected_squares[0]
                piece = self.chess.board.state[piece_rank][piece_file].piece
                if piece is not None and piece.piece_type == PieceType.PAWN and not self.auto_queen and is_pawn_promotion(clicked_rank, piece.colour_type):
                        if piece.colour_type == ColourType.WHITE:
                            self.white_promotion = True
                        else:
                            self.black_promotion = True
                        self.selected_squares.append((clicked_rank, clicked_file))
                        return
            self.selected_squares.append((clicked_rank, clicked_file))
            self.move()
        if button is pyglet.window.mouse.RIGHT:
            self.chess.undo_move()
            self.brute_force_update()
            print(self.chess.board)

    def move(self):
        (from_rank, from_file) = self.selected_squares[0]
        (to_rank, to_file) = self.selected_squares[1]
        promotion_piece = PieceType.QUEEN
        if len(self.selected_squares) > 2:
            selected_rank, selected_file = self.selected_squares.pop()
            if selected_file in range(2,6) and from_rank == selected_rank:
                promotion_piece = PieceType(selected_file - 1)
            else:
                self.selected_squares = []
                return
        if self.chess.move_from_position(from_rank, from_file, to_rank, to_file, promotion_piece):
            self.brute_force_update()
            print(self.chess.board)
        self.selected_squares = []

    def brute_force_update(self):
        for rank in self.piece_sprites:
            for piece in rank:
                if piece is None:
                    continue
                piece.delete()
        self.piece_sprites = piece_generator(self.chess.board.state, self.layout, self.main_batch, self.pieces_group)
