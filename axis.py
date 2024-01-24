import pyglet

class Axis:
    def __init__(self, window):
        self.batch = pyglet.graphics.Batch()

        self.origin_point_x = window.width // 2
        self.origin_point_y = 100

        self.size_factor = 1.0

        self.transparency = 100
        self.arrow_len = 10

        self.x_axis = None
        self.x_axis_arrow = None
        self.x_axis_label = None

        self.y_axis = None
        self.y_axis_arrow = None
        self.y_axis_label = None

    def get_origin(self):
        return (self.origin_point_x, self.origin_point_y)

    def draw(self):
        self.batch.draw()

    def create_x_axis(self, length):
        axis_len = self.size_factor * length

        self.x_axis = pyglet.shapes.Line(
            self.origin_point_x, self.origin_point_y,
            self.origin_point_x + axis_len, self.origin_point_y,
            width=1, color=(255, 0, 0, self.transparency), batch=self.batch)

        self.x_axis_arrow = pyglet.shapes.Triangle(
            self.origin_point_x + axis_len, self.origin_point_y - self.arrow_len // 2, 
            self.origin_point_x + axis_len, self.origin_point_y + self.arrow_len // 2, 
            self.origin_point_x + axis_len + self.arrow_len, self.origin_point_y, 
            color=(255, 0, 0), batch=self.batch)

        self.x_axis_label = pyglet.text.Label(
            'X',
            font_size=10,
            color=(255, 0, 0, 255),
            x=self.origin_point_x + axis_len + self.arrow_len + 8,
            y=self.origin_point_y + 2,
            anchor_x='center',
            anchor_y='center',
            batch=self.batch)

    def create_y_axis(self, length):
        axis_len = self.size_factor * length

        self.y_axis = pyglet.shapes.Line(
            self.origin_point_x, self.origin_point_y,
            self.origin_point_x , self.origin_point_y + axis_len,
            width=1, color=(0, 255, 0, self.transparency), batch=self.batch)

        self.y_axis_arrow = pyglet.shapes.Triangle(
            self.origin_point_x + self.arrow_len // 2, self.origin_point_y + axis_len, 
            self.origin_point_x - self.arrow_len // 2, self.origin_point_y + axis_len, 
            self.origin_point_x, self.origin_point_y + axis_len + self.arrow_len, 
            color=(0, 255, 0), batch=self.batch)

        self.y_axis_label = pyglet.text.Label(
            'Y',
            font_size=10,
            color=(0, 255, 0, 255),
            x=self.origin_point_x,
            y=self.origin_point_y + axis_len + self.arrow_len + 10,
            anchor_x='center',
            anchor_y='center',
            batch=self.batch)

