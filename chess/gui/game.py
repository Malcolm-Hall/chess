from typing import Optional

import pyglet
from core.piece import ColourType
from gui.board import Board
from gui.layout import Layout
from gui.promotion_overlay import PromotionOverlay


class Game(pyglet.window.Window):
    """Constructs a game of chess and handles input from the player."""
    board: Board
    promotion_overlay: PromotionOverlay

    def __init__(self, layout: Layout, fen: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
        super().__init__(layout.board_size, layout.board_size, caption="Chess")
        self.board = Board(fen, layout)
        self.promotion_overlay = PromotionOverlay(layout)

    def on_draw(self):
        self.clear()
        self.board.draw()
        self.promotion_overlay.draw(self.board.promotion_colour)

    def on_mouse_press(self, x, y, button, modifiers):
        if button is pyglet.window.mouse.LEFT:
            self.board.input(x, y)

        if button is pyglet.window.mouse.RIGHT:
            self.board.undo_move()
