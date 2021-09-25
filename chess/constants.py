
# [Piece, Colour]                                  WHITE, BLACK
UNICODE_PIECE_SYMBOLS: list[list[str]] = [["\u2654", "\u265A"], # King   |K
                                               ["\u2655", "\u265B"], # Queen  |Q
                                               ["\u2656", "\u265C"], # Rook   |R
                                               ["\u2657", "\u265D"], # Bishop |B
                                               ["\u2658", "\u265E"], # Knight |N
                                               ["\u2659", "\u265F"]] # Pawn   |P

# [Piece][Colour]
PIECE_STRS: list[list[str]] = [["k","K"],
                                    ["q","Q"],
                                    ["r","R"],
                                    ["b","B"],
                                    ["n","N"],
                                    ["p","P"]]

# Windows
# UNICODE_WHITE_SPACE: str = "\u3000"
# Linux
UNICODE_WHITE_SPACE: str = " "

# ['A'...'H': 0...7]
FILE_NOTATION: dict[str, int] = {chr(i) : int(i - ord('a')) for i in range(ord('a'), ord('i'))}
# ['1'...'8': 0...7]
RANK_NOTATION: dict[str, int] = {str(i+1) : i for i in range(8)}

