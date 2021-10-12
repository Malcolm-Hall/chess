from typing import Optional

import pyglet
from core.chess import Chess
from core.piece import ColourType
from core.piece import PieceType
from core.square import Square
from gui.layout import Layout
from gui.sprites import board_sprites_generator
from gui.sprites import piece_sprites_generator
from gui.sprites import PieceSprite
from gui.sprites import RectangleSprite
from util import is_pawn_promotion


class Board:
    """The graphical board of the game, which interfaces with the chess core."""
    main_batch = pyglet.graphics.Batch()
    board_group = pyglet.graphics.OrderedGroup(0)
    pieces_group = pyglet.graphics.OrderedGroup(1)
    board_sprites: list[RectangleSprite]
    piece_sprites: list[list[Optional[PieceSprite]]]
    layout: Layout
    selected_squares: list[Square] = []
    auto_queen: bool = False
    promotion_colour: Optional[ColourType] = None

    def __init__(self, fen: str, layout: Layout):
        self.chess = Chess(fen)
        self.layout = layout
        self.board_sprites = board_sprites_generator(
            self.layout.square_size,
            self.main_batch,
            self.board_group
        )
        self.piece_sprites = piece_sprites_generator(
            self.chess.board.state,
            self.layout,
            self.main_batch,
            self.pieces_group
        )

    def draw(self):
        self.main_batch.draw()

    def brute_force_update(self):
        """Brute force updates the piece sprites."""
        # TODO: implement more efficient update method for the piece sprites
        for rank in self.piece_sprites:
            for piece in rank:
                if piece is None:
                    continue
                piece.delete()
        self.piece_sprites = piece_sprites_generator(
            self.chess.board.state,
            self.layout,
            self.main_batch,
            self.pieces_group
        )
        print(self.chess.board)

    def input(self, x: int, y: int):
        """Recieves input from the player, selecting the square and making a move when necessary."""
        self.select_square(x, y)
        if self.can_move():
            self.move()
            self.selected_squares = []

    def select_square(self, x: int, y: int):
        """Select a square on the chess board, appending it to the list of selected squares."""
        clicked_rank, clicked_file = int(y / self.layout.square_size), int(x / self.layout.square_size)
        square = Square(clicked_rank, clicked_file)
        self.selected_squares.append(square)

    def update_promotion_colour(self):
        """Updates the promotion colour if pawn promotion, returning a bool to indicate if the next move should be made."""
        piece_to_move = self.chess.get_piece_at(self.selected_squares[0])
        to_square = self.selected_squares[1]
        if is_pawn_promotion(to_square.rank, piece_to_move):
            self.promotion_colour = piece_to_move.colour_type
            return False
        return True

    def can_move(self) -> bool:
        """Returns a bool indicating if the next move should be made."""
        if len(self.selected_squares) < 2:
            return False
        if not self.auto_queen and len(self.selected_squares) == 2:
            return self.update_promotion_colour()
        self.promotion_colour = None
        return True

    def move(self, promotion_piece: PieceType = PieceType.QUEEN):
        """Make a move using the selected squares and update the GUI."""
        from_square = self.selected_squares[0]
        to_square = self.selected_squares[1]
        if len(self.selected_squares) > 2:
            choice = self.selected_squares.pop()
            if not promotion_piece_selected(choice, from_square.rank):
                return
            promotion_piece = PieceType(choice.file - 1)
        if self.chess.move_from_position(from_square, to_square, promotion_piece):
            self.brute_force_update()

    def undo_move(self):
        """Undo the last legal move and update the GUI."""
        self.chess.undo_move()
        self.brute_force_update()


def promotion_piece_selected(choice: Square, from_rank: int) -> bool:
    """Returns a bool indicating if a promotion piece was selected by the player."""
    return (choice.file in range(2, 6)) and (choice.rank == from_rank)
