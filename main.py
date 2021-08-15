import pyglet
from chess import Board
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
        self.board = Board(fen)
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
            self.move(clicked_rank, clicked_file)

    def move(self, to_rank, to_file):
        from_rank, from_file = self.selected_piece.rank, self.selected_piece.file
        try:
            self.board.move(from_rank, from_file, to_rank, to_file)
            # update piece
            self.selected_piece.x = to_file * self.square_size + self.x_offset
            self.selected_piece.y = to_rank * self.square_size + self.y_offset
            self.selected_piece.rank = to_rank
            self.selected_piece.file = to_file
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


if __name__ == '__main__':
    main = Main()
    # def update(dt):
    #     pass
    #
    # pyglet.clock.schedule_interval(update, 1 / 10.0)
    pyglet.app.run()