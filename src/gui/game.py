import pyglet
from typing import Union, Optional
from constants import PIECE_STRS, UNICODE_PIECE_SYMBOLS
from core.piece import Piece, PieceType, ColourType, CHESS_PIECES
import core.chess
from .piece import PieceSprite



class Main(pyglet.window.Window):
    auto_queen: bool = False
    size: int = 512
    square_size: int = size // 8
    x_offset, y_offset = -1, 7
    piece_size: int = 45
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
        super().__init__(self.size, self.size, caption="Chess")
        self.fpsDisplay = pyglet.window.FPSDisplay(window=self)
        self.game = core.chess.Game(fen)
        self.board_sprites = self._board_generator()
        self.piece_sprites = self._piece_generator()
        self.promotion_piece_sprites = self._promotion_piece_generator()


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
            clicked_file = int(x / self.size * 8)
            clicked_rank = int(y / self.size * 8)
            if self.selected_squares == [] and self.piece_sprites[clicked_rank][clicked_file] is not None:
                self.selected_squares.append((clicked_rank, clicked_file))
                return
            elif len(self.selected_squares) < 2:
                if self.selected_squares[0] == (clicked_rank, clicked_file):
                    self.selected_squares = []
                    return
                (piece_rank, piece_file) = self.selected_squares[0]
                piece = self.game.board.state[piece_rank][piece_file].piece
                if piece is not None and piece.piece_type == PieceType.PAWN and not self.auto_queen and self.game.board.is_pawn_promotion(clicked_rank, piece.colour_type):
                        if piece.colour_type == ColourType.WHITE:
                            self.white_promotion = True
                        else:
                            self.black_promotion = True
                        self.selected_squares.append((clicked_rank, clicked_file))
                        return
            self.selected_squares.append((clicked_rank, clicked_file))
            self.move()
        if button is pyglet.window.mouse.RIGHT:
            self.game.undo_move()
            self.brute_force_update()
            print(self.game.board)

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
        if self.game.move_from_position(from_rank, from_file, to_rank, to_file, promotion_piece):
            self.brute_force_update()
            print(self.game.board)
        self.selected_squares = []

    def _board_generator(self) -> list[pyglet.shapes.Rectangle]:
        return [pyglet.shapes.Rectangle(x=i*self.square_size, y=j*self.square_size,
                                        width=self.square_size, height=self.square_size,
                                        color=(240, 217, 181) if (i%2==0) != (j%2==0) else (148, 111, 81),
                                        batch=self.main_batch,
                                        group=self.board_group)
                for i in range(8) for j in range(8)]

    def _promotion_piece_generator(self) -> list[Union[PieceSprite, pyglet.shapes.Rectangle]]:
        promotion_backgrounds = [pyglet.shapes.Rectangle(x=2 * self.square_size,
                                                         y=(1 if colour.value else 6) * self.square_size,
                                                         width=4 * self.square_size, height=self.square_size,
                                                         color=(100, 100, 200),
                                                         batch=self.white_promotion_batch if colour == ColourType.WHITE else self.black_promotion_batch,
                                                         group=self.overlay_group)
                                 for colour in ColourType]

        promotion_pieces = [PieceSprite(str(piece_symbol),
                               (i+2) * self.square_size + self.x_offset,
                               (1 if colour else 6) * self.square_size + self.y_offset,
                               font_size=self.piece_size,
                               batch=self.white_promotion_batch if colour == ColourType.WHITE.value else self.black_promotion_batch,
                               group=self.promotion_group)
                           for i, piece_type in enumerate(UNICODE_PIECE_SYMBOLS[1:5]) for colour, piece_symbol in enumerate(piece_type)]

        return promotion_backgrounds + promotion_pieces

    
    def _piece_generator(self) -> list[list[Optional[PieceSprite]]]:
        return [[(PieceSprite(str(square.piece),
                              file * self.square_size + self.x_offset,
                              rank * self.square_size + self.y_offset,
                              font_size=self.piece_size,
                              batch=self.main_batch,
                              group=self.pieces_group)
                 if square.piece is not None else None)
                 for file, square in enumerate(squares)] for rank, squares in enumerate(self.game.board.state)]

    def brute_force_update(self):
        for rank in self.piece_sprites:
            for piece in rank:
                if piece is None:
                    continue
                piece.delete()
        self.piece_sprites = self._piece_generator()
