from typing import Optional

import pyglet
from core.square import BoardSquare
from gui.layout import Layout


class PieceSprite(pyglet.text.Label):
    """Sprite for a chess piece. Rendered as text using unicode chess symbols."""

    def __init__(self, piece: str, x: int, y: int, piece_size: int, batch, group):
        super().__init__(text=piece, x=x, y=y,
                         font_size=piece_size,
                         batch=batch, group=group)


class RectangleSprite(pyglet.shapes.Rectangle):
    """Sprite for a rectangle."""

    def __init__(self, x: int, y: int, width: int, height: int, colour: tuple[int, int, int], batch, group):
        super().__init__(x=x, y=y, width=width, height=height,
                         color=colour, batch=batch, group=group)


def board_sprites_generator(square_size: int, main_batch, board_group) -> list[RectangleSprite]:
    """Generates board sprites of a given square size and assigns the render batch and group"""
    return [RectangleSprite(
        i * square_size,
        j * square_size,
        square_size,
        square_size,
        (157, 126, 104) if (i % 2 == 0) != (j % 2 == 0) else (85, 60, 42),
        main_batch,
        board_group)
        for i in range(8)
        for j in range(8)]


def piece_sprites_generator(board_state: list[list[BoardSquare]], layout: Layout, main_batch, pieces_group) -> list[list[Optional[PieceSprite]]]:
    "Generates piece sprites of a given Layout and assigns the render batch and group"
    return [[(PieceSprite(
        str(square.piece),
        file * layout.square_size + layout.piece_offset[0],
        rank * layout.square_size + layout.piece_offset[1],
        layout.piece_size,
        main_batch,
        pieces_group)
        if square.piece is not None else None)
        for file, square in enumerate(squares)]
        for rank, squares in enumerate(board_state)]
