import gui.game
import gui.layout
import pyglet

if __name__ == '__main__':
    layout = gui.layout.Layout(512, 45, (5, 10))
    fen = input("Enter FEN to start from a position or leave empty for a new game: ")
    # TODO: validate FEN
    if fen:
        main = gui.game.Game(layout, fen)
    else:
        main = gui.game.Game(layout)
    # test = gui.game.Game(layout, "8/8/8/8/8/8/1ppp4/8 w KQkq - 0 1")
    pyglet.app.run()
