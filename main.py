import pyglet
import math

window = pyglet.window.Window(width=600, height=400, caption='SCARA simulator')


# Axis scheme
axis_batch = pyglet.graphics.Batch()

origin_point_x = window.width // 2
origin_point_y = 100

axis_transparency = 100
arrow_side_len = 10

x_axis_length = 200
x_axis = pyglet.shapes.Line(origin_point_x, origin_point_y,
                            origin_point_x + x_axis_length, origin_point_y,
                            width=1, color=(255, 0, 0, axis_transparency), batch=axis_batch)

x_axis_arrow = pyglet.shapes.Triangle(origin_point_x + x_axis_length, origin_point_y - arrow_side_len // 2, 
                                      origin_point_x + x_axis_length, origin_point_y + arrow_side_len // 2, 
                                      origin_point_x + x_axis_length + arrow_side_len, origin_point_y, 
                                      color=(255, 0, 0), batch=axis_batch)
x_axis_label = pyglet.text.Label('X',
                                 font_size=10,
                                 color=(255, 0, 0, 255),
                                 x=origin_point_x + x_axis_length + arrow_side_len + 8,
                                 y=origin_point_y + 3,
                                 anchor_x='center',
                                 anchor_y='center',
                                 batch=axis_batch)

y_axis_length = 200
y_axis = pyglet.shapes.Line(origin_point_x, origin_point_y,
                            origin_point_x , origin_point_y + y_axis_length,
                            width=1, color=(0, 255, 0, axis_transparency), batch=axis_batch)

y_axis_arrow = pyglet.shapes.Triangle(origin_point_x + arrow_side_len // 2, origin_point_y + y_axis_length, 
                                      origin_point_x - arrow_side_len // 2, origin_point_y + y_axis_length, 
                                      origin_point_x, origin_point_y + y_axis_length + arrow_side_len, 
                                      color=(0, 255, 0), batch=axis_batch)
y_axis_label = pyglet.text.Label('Y',
                                 font_size=10,
                                 color=(0, 255, 0, 255),
                                 x=origin_point_x,
                                 y=origin_point_y + y_axis_length + arrow_side_len + 10,
                                 anchor_x='center',
                                 anchor_y='center',
                                 batch=axis_batch)



# SCARA scheme
# BaseLink - Joint1 - Link1 - Joint2 - Link2

scara_batch = pyglet.graphics.Batch()

base_side_len = 20
base_point_x = origin_point_x - base_side_len // 2
base_point_y = origin_point_y - base_side_len // 2

base_link = pyglet.shapes.Box(base_point_x, base_point_y, 
                              base_side_len, base_side_len, 
                              thickness=1, color=(123, 255, 120), batch=scara_batch)

joint_radius = 4

joint1 = pyglet.shapes.Circle(origin_point_x, origin_point_y,
                              joint_radius, 
                              segments=None, 
                              color=(255, 255, 255, 255), 
                              batch=scara_batch)


link_width = 2

link1_start_x = joint1.x
link1_start_y = joint1.y
link1_len = 80
link1_angle = 0
link1 = pyglet.shapes.Line(link1_start_x, link1_start_y,
                           link1_start_x + link1_len * math.cos(math.radians(link1_angle)),
                           link1_start_y + link1_len * math.sin(math.radians(link1_angle)),
                           width=link_width, color=(120, 110, 50), batch=scara_batch)

joint2 = pyglet.shapes.Circle(link1.x2, link1.y2,
                              joint_radius, 
                              segments=None, 
                              color=(255, 255, 255, 255), 
                              batch=scara_batch)

link2 = pyglet.shapes.Line(joint2.x, joint2.y,
                           343, 123,
                           width=link_width, color=(20, 200, 100), batch=scara_batch)

# Clockwise rotation of the shape in degrees
# It will be rotated about its (anchor_x, anchor_y) position, 
# which defaults to the first vertex point of the shape.
# Can be used to rotate line
#  line.rotation = -90 

def update_link1(dt):
    global link1_angle

    # Update the end point of the line based on the new angle
    link1_angle += 20 * dt
    rad = math.radians(link1_angle)
    link1.x2 = link1_start_x + link1_len * math.cos(rad)
    link1.y2 = link1_start_y + link1_len * math.sin(rad)

    joint2.x = link1.x2
    joint2.y = link1.y2

    link2.x = joint2.x
    link2.y = joint2.y

@window.event
def on_draw():
    window.clear()
    axis_batch.draw()
    scara_batch.draw()


pyglet.clock.schedule_interval(update_link1, 1 / 60.0)  # Update at 60 FPS
pyglet.app.run()
