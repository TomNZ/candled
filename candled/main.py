import candled
import pyglet


# Pixels Per LED
PPL = 20

frame = 0


def main():
    window = pyglet.window.Window(candled.WIDTH * PPL, candled.HEIGHT * PPL, caption='CandLED')


    @window.event
    def on_draw():
        window.clear()

    pyglet.app.run()



if __name__ == '__main__':
    main()