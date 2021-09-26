
class Layout:
    """Defines the visual layout of the chess board and pieces."""
    board_size: int
    square_size: int
    piece_size: int
    piece_offset: tuple[int, int]
    def __init__(self, board_size: int, piece_size: int, piece_offset: tuple[int, int]):
        self.board_size = board_size
        self.square_size = board_size // 8
        self.piece_size = piece_size
        self.piece_offset = piece_offset