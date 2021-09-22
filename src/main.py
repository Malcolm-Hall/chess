import pyglet
import gui.game

if __name__ == '__main__':
    main = gui.game.Main("rnbqkbnr/pppppppp/PP6/PP6/8/PPPP4/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    # def update(dt):
    #     main.on_draw()
    #
    # pyglet.clock.schedule_interval(update, 1 / 1.0)
    pyglet.app.run()