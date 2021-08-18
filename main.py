import pyglet
import chess
from chessExceptions import InvalidMoveException

class Piece(pyglet.text.Label):
    def __init__(self, piece: str, x: int, y: int, rank: int, file: int, batch=None, group=None):
        super().__init__(str(piece),
                         x=x, y=y,
                         font_size=35,
                         batch=batch,
                         group=group)
        self.rank = rank
        self.file = file


class Main(pyglet.window.Window):
    size = 400
    square_size = size // 8
    x_offset, y_offset = -1, 5
    selected_piece = None

    main_batch = pyglet.graphics.Batch()
    board_to_draw = pyglet.graphics.OrderedGroup(0)
    pieces_to_draw = pyglet.graphics.OrderedGroup(1)

    def __init__(self, fen: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
        super().__init__(self.size, self.size, caption="Chess")
        self.fpsDisplay = pyglet.window.FPSDisplay(window=self)
        self.board = chess.Board(fen)
        self.board_shapes = self._board_generator()
        self.piece_shapes = self._piece_generator()

    def on_draw(self):
        self.clear()
        self.main_batch.draw()
        self.fpsDisplay.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if button is pyglet.window.mouse.LEFT:
            clicked_file = int(x / self.size * 8)
            clicked_rank = int(y / self.size * 8)
            if self.selected_piece is not None and self.selected_piece.rank == clicked_rank and self.selected_piece.file == clicked_file:
                return
            if self.selected_piece is None:
                self.selected_piece = self.piece_shapes[clicked_rank][clicked_file]
                return
            self.move((clicked_rank, clicked_file))

    def move(self, to_):
        from_ = (self.selected_piece.rank, self.selected_piece.file)
        try:
            self.board.move(from_, to_)
            # update piece
            self.selected_piece.x = to_[1] * self.square_size + self.x_offset
            self.selected_piece.y = to_[0] * self.square_size + self.y_offset
            self.selected_piece.rank = to_[0]
            self.selected_piece.file = to_[1]
            # check capture
            capture_piece = self.piece_shapes[to_rank][to_file]
            if capture_piece is not None:
                capture_piece.delete()
            # move reference
            self.piece_shapes[to_rank][to_file] = self.selected_piece
            self.piece_shapes[from_rank][from_file] = None
        except InvalidMoveException as err:
            print(f"Invalid Move: {err}")
        finally:
            self.selected_piece = None

    def _board_generator(self) -> list[pyglet.shapes.Rectangle]:
        return [pyglet.shapes.Rectangle(x=j*self.square_size, y=i*self.square_size,
                                        width=self.square_size, height=self.square_size,
                                        color=(240, 217, 181) if (j%2==0) != (i%2==0) else (148, 111, 81),
                                        batch=self.main_batch,
                                        group=self.board_to_draw)
                for j in range(8) for i in range(8)]
    
    def _piece_generator(self):
        return [[(Piece(str(piece),
                        j * self.square_size + self.x_offset,
                        i * self.square_size + self.y_offset,
                        i, j,
                        batch=self.main_batch,
                        group=self.pieces_to_draw)
               if piece is not None else None)
               for j, piece in enumerate(rank)] for i, rank in enumerate(self.board.board)]

def move(chessNotation):
    return game.move_from_notation(chessNotation[:2], chessNotation[2:4])

if __name__ == '__main__':
    game = chess.Game("rnbqkbnr/pppppppp/2P5/1P6/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    move("a2a4")
    move("b4a3")
    move("b2b4")
    move("c3d2")
    move("b1a3")
    game.undo_move()
    game.undo_move()
    game.undo_move()
    game.undo_move()
    game.undo_move()

    # main = Main()
    # # def update(dt):
    # #     pass
    # #
    # # pyglet.clock.schedule_interval(update, 1 / 10.0)
    # pyglet.app.run()