import pyglet


class PieceSprite(pyglet.text.Label):
    """Sprite for a chess piece. Rendered as text using unicode chess symbols."""

    def __init__(self, piece: str, x: int, y: int, piece_size: int, batch, group):
        super().__init__(text=piece, x=x, y=y,
                         font_size=piece_size,
                         batch=batch, group=group)


class SquareSprite(pyglet.shapes.Rectangle):
    """Sprite for a square of a chess board"""

    def __init__(self, x: int, y: int, width: int, height: int, colour: tuple[int, int, int], batch, group):
        super().__init__(x=x, y=y, width=width, height=height,
                         color=colour, batch=batch, group=group)
