import pyglet
import gui.game

if __name__ == '__main__':
    #main = gui.game.Main("rnbqkbnr/pppppppp/PP6/PP6/8/PPPP4/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    fen = input("Enter FEN to start from a position or leave empty for a new game: ")
    if fen:
    	main = gui.game.Main(fen)
    else:
    	main = gui.game.Main()
    pyglet.app.run()
