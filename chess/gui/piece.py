import pyglet

class PieceSprite(pyglet.text.Label):
    def __init__(self, piece: str, x: int, y: int, font_size=35, batch=None, group=None):
        super().__init__(piece,
                         x=x, y=y,
                         font_size=font_size,
                         batch=batch,
                         group=group)