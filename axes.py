import pyglet

class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class Axes:
    TRANSPARENCY = 100
    ARROW_LEN = 10

    def __init__(self, window: pyglet.window, size_factor: float = 1.0):
        self.batch = pyglet.graphics.Batch()

        self.origin_point = Point(x = window.width // 2, y = window.height // 2 - 50)

        self.size_factor = size_factor

        self.x_axis = None
        self.x_axis_arrow = None
        self.x_axis_label = None

        self.y_axis = None
        self.y_axis_arrow = None
        self.y_axis_label = None

    def get_origin_point(self) -> Point:
        return self.origin_point

    def point(self, x: int, y: int) -> Point:
        ''' Creates a point in relative to axes coordinate system '''
        return Point(x = self.origin_point.x + x, y = self.origin_point.y + y)

    def draw(self):
        self.batch.draw()

    def create_x_axis(self, length: int):
        axis_len = self.size_factor * length

        self.x_axis = pyglet.shapes.Line(
            self.origin_point.x, self.origin_point.y,
            self.origin_point.x + axis_len, self.origin_point.y,
            width=1, color=(255, 0, 0, self.TRANSPARENCY), batch=self.batch)

        self.x_axis_arrow = pyglet.shapes.Triangle(
            self.origin_point.x + axis_len, self.origin_point.y - self.ARROW_LEN // 2, 
            self.origin_point.x + axis_len, self.origin_point.y + self.ARROW_LEN // 2, 
            self.origin_point.x + axis_len + self.ARROW_LEN, self.origin_point.y, 
            color=(255, 0, 0), batch=self.batch)

        self.x_axis_label = pyglet.text.Label(
            'X',
            font_size=10,
            color=(255, 0, 0, 255),
            x=self.origin_point.x + axis_len + self.ARROW_LEN + 8,
            y=self.origin_point.y + 2,
            anchor_x='center',
            anchor_y='center',
            batch=self.batch)

    def create_y_axis(self, length: int):
        axis_len = self.size_factor * length

        self.y_axis = pyglet.shapes.Line(
            self.origin_point.x, self.origin_point.y,
            self.origin_point.x , self.origin_point.y + axis_len,
            width=1, color=(0, 255, 0, self.TRANSPARENCY), batch=self.batch)

        self.y_axis_arrow = pyglet.shapes.Triangle(
            self.origin_point.x + self.ARROW_LEN // 2, self.origin_point.y + axis_len, 
            self.origin_point.x - self.ARROW_LEN // 2, self.origin_point.y + axis_len, 
            self.origin_point.x, self.origin_point.y + axis_len + self.ARROW_LEN, 
            color=(0, 255, 0), batch=self.batch)

        self.y_axis_label = pyglet.text.Label(
            'Y',
            font_size=10,
            color=(0, 255, 0, 255),
            x=self.origin_point.x,
            y=self.origin_point.y + axis_len + self.ARROW_LEN + 10,
            anchor_x='center',
            anchor_y='center',
            batch=self.batch)


# TODO:
class Legend:
    # def __init__(self, window: pyglet.window, size_factor: float = 1.0):
    pass