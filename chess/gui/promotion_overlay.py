from typing import Optional
from typing import Union

import pyglet
from constants import UNICODE_PIECE_SYMBOLS
from core.piece import ColourType
from gui.layout import Layout
from gui.sprites import PieceSprite
from gui.sprites import RectangleSprite

PromotionSprites = Union[PieceSprite, RectangleSprite]


def promotion_sprites_generator(layout: Layout, white_promotion_batch, black_promotion_batch, background_group, promotion_group) -> list[PromotionSprites]:
    """Generates the sprites used by the PromotionOverlay"""
    promotion_backgrounds: list[PromotionSprites] = [RectangleSprite(2 * layout.square_size,
                                                                     (1 if colour.value else 6) * layout.square_size,
                                                                     4 * layout.square_size,
                                                                     layout.square_size,
                                                                     (100, 100, 200),
                                                                     white_promotion_batch if colour == ColourType.WHITE else black_promotion_batch,
                                                                     background_group)
                                                     for colour in ColourType]

    promotion_pieces: list[PromotionSprites] = [PieceSprite(str(piece_symbol),
                                                            (i + 2) * layout.square_size + layout.piece_offset[0],
                                                            (1 if colour else 6) * layout.square_size + layout.piece_offset[1],
                                                            layout.piece_size,
                                                            white_promotion_batch if colour == ColourType.WHITE.value else black_promotion_batch,
                                                            promotion_group)
                                                for i, piece_type in enumerate(UNICODE_PIECE_SYMBOLS[1:5])
                                                for colour, piece_symbol in enumerate(piece_type)]
    return promotion_backgrounds + promotion_pieces


class PromotionOverlay:
    """Pawn promotion overlay which draws the selectable promotion pieces"""
    background_group = pyglet.graphics.OrderedGroup(0)
    promotion_group = pyglet.graphics.OrderedGroup(1)
    white_promotion_batch = pyglet.graphics.Batch()
    black_promotion_batch = pyglet.graphics.Batch()
    promotion_overlay_sprites: list[PromotionSprites]

    def __init__(self, layout: Layout):
        self.promotion_overlay_sprites = promotion_sprites_generator(
            layout, self.white_promotion_batch, self.black_promotion_batch, self.background_group, self.promotion_group)

    def draw(self, promotion_colour: Optional[ColourType]):
        if promotion_colour is None:
            return
        elif promotion_colour == ColourType.WHITE:
            self.white_promotion_batch.draw()
        else:
            self.black_promotion_batch.draw()
