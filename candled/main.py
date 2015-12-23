import candled
import pyglet


# Pixels Per LED
PPL = 20
frame = 0

# Visualization
MIN_TEMP = 0.5
MAX_TEMP = 2.0
TEMP_DIFF = MAX_TEMP - MIN_TEMP


def build_vertex_list():
    num_vertices = candled.WIDTH * candled.HEIGHT * 6
    vertex_list = pyglet.graphics.vertex_list(
        num_vertices,
        ('v2i', (0,) * num_vertices * 2),
        ('c3B', (255, 255, 255,) * num_vertices)
    )

    vertices = []
    for x in range(candled.WIDTH):
        for y in range(candled.HEIGHT):
            left = x * PPL
            right = (x+1) * PPL - 1
            top = (candled.HEIGHT - y) * PPL - 1
            bottom = (candled.HEIGHT - y - 1) * PPL

            vertices.extend([
                left, top,
                right, top,
                right, bottom,
                left, top,
                right, bottom,
                left, bottom,
            ])

    vertex_list.vertices = vertices
    return vertex_list


vertices = build_vertex_list()
sim = candled.CandLED()


def tick_frame(time):
    sim.tick_frame(time)

    colors = []
    for x in range(candled.WIDTH):
        for y in range(candled.HEIGHT):
            temp = sim.temp_field[x + candled.EDGE][y + candled.EDGE]
            norm_temp = (temp - MIN_TEMP) / TEMP_DIFF
            color = int(norm_temp * 255)
            colors.extend(
                [
                    min(255, max(0, color)),
                    min(255, max(0, color - 60)),
                    min(255, max(0, color - 180))
                ] * 6
            )

    vertices.colors = colors


def main():
    window = pyglet.window.Window(candled.WIDTH * PPL, candled.HEIGHT * PPL, caption='CandLED')

    @window.event
    def on_draw():
        window.clear()
        vertices.draw(pyglet.gl.GL_TRIANGLES)

    pyglet.clock.schedule_interval(tick_frame, 1.0 / 20)
    pyglet.app.run()



if __name__ == '__main__':
    main()