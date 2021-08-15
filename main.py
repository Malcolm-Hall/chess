import pyglet
from typing import List
from chess import Board

class Main(pyglet.window.Window):
    size = 400
    selected_piece = None
    main_batch = pyglet.graphics.Batch()
    board_to_draw = pyglet.graphics.OrderedGroup(0)
    pieces_to_draw = pyglet.graphics.OrderedGroup(1)
    def __init__(self, fen: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
        super().__init__(self.size, self.size, caption="Chess")
        self.fpsDisplay = pyglet.window.FPSDisplay(window=self)
        self.board_shapes = self.board_generator()

        self.board = Board(fen)
        # self.board.make_move("A2", "A4")
        #         # self.board.make_move("B7", "B5")
        #         # self.board.make_move("A4", "B5")

    def on_draw(self):
        self.clear()
        self.main_batch.draw()
        self.fpsDisplay.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if button is pyglet.window.mouse.LEFT:
            clicked_file = int(x / self.size * 8)
            clicked_rank = int(y / self.size * 8)
            print(f"clicked file {clicked_file}, rank {clicked_rank}")
            if self.selected_piece is None:
                self.selected_piece = self.board.board[clicked_rank][clicked_file]
                return
            # self.board.make_move(, clicked_rank)

    def board_generator(self) -> List[pyglet.shapes.Rectangle]:
        shapes = []
        square_size = self.size // 8
        flag = True
        for i in range(8):
            for j in range(8):
                colour = (148, 111, 81) if flag else (240, 217, 181)
                shapes.append(pyglet.shapes.Rectangle(x=j * square_size, y=i * square_size,
                                                      width=square_size, height=square_size,
                                                      color=colour,
                                                      batch=self.main_batch,
                                                      group=self.board_to_draw))
                flag = not (flag)
            flag = not (flag)
        return shapes

if __name__ == '__main__':
    # board = Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    # board.make_move("A2", "A4")
    # board.make_move("B7", "B5")
    # board.make_move("A4", "B5")

    main = Main()

    # def update(dt):
    #     pass
    #
    # pyglet.clock.schedule_interval(update, 1 / 10.0)
    pyglet.app.run()