import pyglet
import math

window = pyglet.window.Window(width=600, height=400, caption='Animated Line')
# label = pyglet.text.Label('Hello, world!',
#                           font_size=36,
#                           x=window.width // 2,
#                           y=window.height // 2,
#                           anchor_x='center',
#                           anchor_y='center')


# Axis scheme

base_width = 20
base_point_x = window.width // 2 - base_width // 2
base_point_y = 60

axis_batch = pyglet.graphics.Batch()

base_box = pyglet.shapes.Box(base_point_x, base_point_y, base_width, base_width, thickness=1, color=(123, 255, 120), batch=axis_batch)


origin_point_x = base_point_x + base_box.width // 2
origin_point_y = base_point_y + base_box.height // 2
x_axis_length = 200

x_axis = pyglet.shapes.Line(origin_point_x, origin_point_y,
                          origin_point_x + x_axis_length, origin_point_y,
                          width=1, color=(255, 0, 0), batch=axis_batch)



# Initial line coordinates and rotation angle
start_x = base_point_x + base_box.width // 2
start_y = base_point_y + base_box.height // 2
length = 100
angle = 0

line_batch = pyglet.graphics.Batch()

line = pyglet.shapes.Line(start_x, start_y,
                          start_x + length * math.cos(math.radians(angle)),
                          start_y + length * math.sin(math.radians(angle)),
                          width=2, color=(255, 0, 0), batch=line_batch)


# Clockwise rotation of the shape in degrees
# It will be rotated about its (anchor_x, anchor_y) position, 
# which defaults to the first vertex point of the shape.
# Can be used to rotate line
line.rotation = -90 

def update(dt):
    global angle
    angle += dt  # Increment the rotation angle over time

    # Update the end point of the line based on the new angle
    line.x2 = start_x + length * math.cos(angle)
    line.y2 = start_y + length * math.sin(angle)

@window.event
def on_draw():
    window.clear()
    # label.draw()
    line_batch.draw()

    axis_batch.draw()






pyglet.clock.schedule_interval(update, 1 / 60.0)  # Update at 60 FPS

pyglet.app.run()