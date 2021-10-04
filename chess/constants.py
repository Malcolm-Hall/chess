# [Piece][Colour]                             WHITE, BLACK
UNICODE_PIECE_SYMBOLS: list[list[str]] = [["\u265A", "\u2654"], # King   |K
                                          ["\u265B", "\u2655"], # Queen  |Q
                                          ["\u265C", "\u2656"], # Rook   |R
                                          ["\u265D", "\u2657"], # Bishop |B
                                          ["\u265E", "\u2658"], # Knight |N
                                          ["\u265F", "\u2659"]] # Pawn   |P

piece_str = str
# [Piece][Colour]
PIECE_STRS: list[list[piece_str]] = [["k","K"],
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

