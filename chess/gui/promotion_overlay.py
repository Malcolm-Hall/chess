import pyglet
from typing import Union, Optional
from constants import UNICODE_PIECE_SYMBOLS
from .sprites import PieceSprite, SquareSprite
from .layout import Layout
from core.piece import ColourType

def promotion_overlay_generator(layout: Layout, white_promotion_batch, black_promotion_batch, background_group, promotion_group) -> list[Union[PieceSprite, SquareSprite]]:
    """Generates the sprites used by the PromotionOverlay"""
    promotion_backgrounds = [SquareSprite(2 * layout.square_size, (1 if colour.value else 6) * layout.square_size,
                                            4 * layout.square_size, layout.square_size,
                                            (100, 100, 200),
                                            white_promotion_batch if colour == ColourType.WHITE else black_promotion_batch,
                                            background_group)
                                for colour in ColourType]
    promotion_pieces = [PieceSprite(str(piece_symbol),
                                    (i+2) * layout.square_size + layout.piece_offset[0],
                                    (1 if colour else 6) * layout.square_size + layout.piece_offset[1],
                                    layout.piece_size,
                                    white_promotion_batch if colour == ColourType.WHITE.value else black_promotion_batch,
                                    promotion_group)
                        for i, piece_type in enumerate(UNICODE_PIECE_SYMBOLS[1:5]) for colour, piece_symbol in enumerate(piece_type)]
    return promotion_backgrounds + promotion_pieces

class PromotionOverlay:
    """Pawn promotion overlay which draws the selectable promotion pieces"""
    background_group = pyglet.graphics.OrderedGroup(0)
    promotion_group = pyglet.graphics.OrderedGroup(1)
    white_promotion_batch = pyglet.graphics.Batch()
    black_promotion_batch = pyglet.graphics.Batch()
    promotion_overlay_sprites: list[Union[PieceSprite, SquareSprite]]

    def __init__(self, layout: Layout):
        self.promotion_overlay_sprites = promotion_overlay_generator(layout, self.white_promotion_batch, self.black_promotion_batch, self.background_group, self.promotion_group)

    def draw(self, promotion_colour: ColourType):
        if promotion_colour is None:
            return
        elif promotion_colour == ColourType.WHITE:
            self.white_promotion_batch.draw()
        else:
            self.black_promotion_batch.draw()