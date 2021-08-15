from chess import Board

if __name__ == '__main__':
    board = Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    board.make_move("A2", "A4")
    board.make_move("B7", "B5")
    board.make_move("A4", "B5")


