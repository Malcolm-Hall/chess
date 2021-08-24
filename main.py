import os

import pyglet
from typing import Union, Optional
import chess
from piece import Piece


class PieceSprite(pyglet.text.Label):
    def __init__(self, piece: str, x: int, y: int, rank: int, file: int, font_size=35, batch=None, group=None):
        super().__init__(str(piece),
                         x=x, y=y,
                         font_size=font_size,
                         batch=batch,
                         group=group)
        self.rank = rank
        self.file = file

    def update(self, rank, file):
        self.rank = rank
        self.file = file



class Main(pyglet.window.Window):
    size = 512
    square_size = size // 8
    x_offset, y_offset = -1, 7
    piece_size = 45
    selected_square = None
    main_batch = pyglet.graphics.Batch()
    board_to_draw = pyglet.graphics.OrderedGroup(0)
    pieces_to_draw = pyglet.graphics.OrderedGroup(1)
    board_sprites: list[pyglet.shapes.Rectangle]
    piece_sprites: list[list[Optional[PieceSprite]]]
    def __init__(self, fen: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
        super().__init__(self.size, self.size, caption="Chess")
        self.fpsDisplay = pyglet.window.FPSDisplay(window=self)
        self.game = chess.Game(fen)
        self.board_sprites = self._board_generator()
        self.piece_sprites = self._piece_generator()

    def on_draw(self):
        self.clear()
        self.main_batch.draw()
        self.fpsDisplay.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if button is pyglet.window.mouse.LEFT:
            clicked_file = int(x / self.size * 8)
            clicked_rank = int(y / self.size * 8)
            if self.selected_square is not None and self.selected_square == (clicked_rank, clicked_file):
                self.selected_square = None
                return
            if self.selected_square is None:
                if self.piece_sprites[clicked_rank][clicked_file] is not None:
                    self.selected_square = (clicked_rank, clicked_file)
                return
            self.move(clicked_rank, clicked_file)
        if button is pyglet.window.mouse.RIGHT:
            self.game.undo_move()
            self.brute_force_update()

    def move(self, to_rank, to_file):
        from_rank, from_file = self.selected_square
        if self.game.move_from_position(from_rank, from_file, to_rank, to_file):
            self.brute_force_update()
            print(self.game.board)
        self.selected_square = None

    def _board_generator(self) -> list[pyglet.shapes.Rectangle]:
        return [pyglet.shapes.Rectangle(x=j*self.square_size, y=i*self.square_size,
                                        width=self.square_size, height=self.square_size,
                                        color=(240, 217, 181) if (j%2==0) != (i%2==0) else (148, 111, 81),
                                        batch=self.main_batch,
                                        group=self.board_to_draw)
                for j in range(8) for i in range(8)]
    
    def _piece_generator(self):
        return [[(PieceSprite(str(square.piece),
                              rank * self.square_size + self.x_offset,
                              file * self.square_size + self.y_offset,
                              rank, file,
                              font_size=self.piece_size,
                              batch=self.main_batch,
                              group=self.pieces_to_draw)
                 if square.piece is not None else None)
                 for rank, square in enumerate(squares)] for file, squares in enumerate(self.game.board.state)]

    def brute_force_update(self):
        for rank in self.piece_sprites:
            for sprite in rank:
                if sprite is None:
                    continue
                sprite.delete()
        self.piece_sprites = self._piece_generator()


if __name__ == '__main__':
    main = Main("rnbqkbnr/pppppppp/PP6/PP6/8/PPPP4/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    # def update(dt):
    #     main.on_draw()
    #
    # pyglet.clock.schedule_interval(update, 1 / 1.0)
    pyglet.app.run()