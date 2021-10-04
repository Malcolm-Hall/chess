from typing import  Iterator
from itertools import permutations, product
from .piece import ColourType

class PotentialMove():
    rank_change: int
    file_change: int
    
    def __init__(self, rank_change: int, file_change: int):
        self.rank_change = rank_change
        self.file_change = file_change

    def get_rank_file_change(self, colour: ColourType) -> tuple[int, int]:
        rank_change = self.rank_change * (-1 if colour == ColourType.BLACK else 1)
        return rank_change, self.file_change
    
    def range(self) -> Iterator[int]:
        yield 1

class SlidingPotentialMove(PotentialMove):
    def range(self) -> Iterator[int]:
        output = 1
        while True:
            yield output
            output += 1


class PawnPotentialMove(PotentialMove):
    capture: bool
    def __init__(self, rank_change: int, file_change: int, capture: bool = False):
        super().__init__(rank_change, file_change)
        self.capture = capture
    
    def range(self) -> Iterator[int]:
        yield 1
        if not self.capture:
            yield 2


def generate_sliding_moves():
    perms = "ABC"
    conversion = {"A":-1,
                  "B":0,
                  "C":1}
    king_moves = []
    queen_moves = []
    rook_moves = []
    bishop_moves = []
    for val in product(perms, repeat=2):
        direction = conversion[val[0]], conversion[val[1]]
        if direction == (0,0):
            continue
        king_moves.append(PotentialMove(direction[0], direction[1]))
        queen_moves.append(SlidingPotentialMove(direction[0], direction[1]))
        if 0 in direction:
            rook_moves.append(SlidingPotentialMove(direction[0], direction[1]))
        else:
            bishop_moves.append(SlidingPotentialMove(direction[0], direction[1]))
    return [king_moves, queen_moves, rook_moves, bishop_moves]

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

def generate_pawn_moves():
    PPM = PawnPotentialMove
    return [PPM(1,0), PPM(1,-1,True), PPM(1,1,True)]

sliding_moves = generate_sliding_moves()
knight_moves = generate_knight_moves()
pawn_moves = generate_pawn_moves()
# [K,Q,R,B,N,P]
POTENTIAL_MOVES = [sliding_moves[0],  # K
                   sliding_moves[1],  # Q
                   sliding_moves[2],  # R
                   sliding_moves[3],  # B
                   knight_moves    ,  # N
                   pawn_moves       ] # P