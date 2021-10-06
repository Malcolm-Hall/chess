import pyglet
import gui.game

if __name__ == '__main__':
    # test = gui.game.Game("8/8/8/8/8/8/1ppp4/8 w KQkq - 0 1")
    fen = input("Enter FEN to start from a position or leave empty for a new game: ")
    # TODO: validate FEN
    if fen:
    	main = gui.game.Game(fen)
    else:
    	main = gui.game.Game()
    pyglet.app.run()
