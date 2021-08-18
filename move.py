from typing import  Iterator, Optional
from itertools import permutations, product
from piece import Piece, ColourType

class PotentialMove():
    rank_change: list[int]
    file_change: int
    infinite_range: bool
    def __init__(self, rank_change: int, file_change: int, infinite_range: bool = False):
        self.rank_change = [rank_change, -rank_change]
        self.file_change = file_change
        self.infinite_range = infinite_range

    def get_rank_file_change(self, colour: ColourType) -> tuple[int, int]:
        return self.rank_change[colour.value], self.file_change

    def range(self) -> Iterator[int]:
        output = 1
        yield output
        while self.infinite_range:
            output += 1
            yield output


class PawnPotentialMove(PotentialMove):
    capture: bool
    def __init__(self, rank_change: int, file_change: int, capture: bool = False):
        super().__init__(rank_change, file_change)
        self.capture = capture


def generate_knight_moves():
    perms = "ABCD"
    conversion = {"A": -1,
                  "B": 1,
                  "C": -2,
                  "D": 2}
    knight_moves = []
    for val in permutations(perms, 2):
        direction = conversion[val[0]], conversion[val[1]]
        if abs(direction[0]) == abs(direction[1]):
            continue
        knight_moves.append(PotentialMove(direction[0], direction[1]))
    return knight_moves

def generate_moves():
    perms = "ABC"
    conversion = {"A":-1,
                  "B":0,
                  "C":1}
    king_moves = []
    queen_moves = []
    rook_moves = []
    bishop_moves = []
    knight_moves = generate_knight_moves()
    for val in product(perms, repeat=2):
        direction = conversion[val[0]], conversion[val[1]]
        if direction == (0,0):
            continue
        king_moves.append(PotentialMove(direction[0], direction[1]))
        queen_moves.append(PotentialMove(direction[0], direction[1], True))
        if 0 in direction:
            rook_moves.append(PotentialMove(direction[0], direction[1], True))
        else:
            bishop_moves.append(PotentialMove(direction[0], direction[1], True))
    return [king_moves, queen_moves, rook_moves, bishop_moves,knight_moves]

PPM = PawnPotentialMove
generated_moves = generate_moves()
# [K,Q,R,B,N,P]
POTENTIAL_MOVES = [generated_moves[0],  # K
                   generated_moves[1],  # Q
                   generated_moves[2],  # R
                   generated_moves[3],  # B
                   generated_moves[4],  # N
                   [PPM(1,0), PPM(2,0), PPM(1,-1,True), PPM(1,1,True)]] # P

class Square:
    rank: int
    file: int
    piece: Optional[Piece]
    def __init__(self, rank: int, file: int, piece: Piece = None):
        self.rank = rank
        self.file = file
        self.piece = piece

    def __repr__(self) -> str:
        return f"Rank {self.rank} File {self.file} {str(self.piece)}"

    def __eq__(self, other: 'Square') -> bool:
        if isinstance(other, Square):
            return (self.rank == other.rank) and (self.file == other.file) and (self.piece == other.piece)
        return False


class Move:
    from_: Square
    to_: Square
    capture_square: Square
    captured_piece: Piece
    def __init__(self, from_: Square, to_: Square, capture_square: Square = None):
        self.from_ = from_
        self.to_ = to_
        if capture_square is None:
            self.capture_square = to_
            self.captured_piece = to_.piece
        else:
            # specify different capture square. Used for en-passant.
            self.capture_square = capture_square
            self.captured_piece = capture_square.piece

    def __repr__(self) -> str:
        move_str = f"From {str(self.from_)} To {str(self.to_)}\n"
        if self.capture_square != self.to_:
            move_str += f"Captured {self.captured_piece}"
        return move_str

    def __eq__(self, other: 'Move') -> bool:
        if isinstance(other, Move):
            return (self.from_ == other.from_) and (self.to_ == other.to_)
        return False

