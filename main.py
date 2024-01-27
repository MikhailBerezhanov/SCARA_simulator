import pyglet
import math

import axes
import scara

window = pyglet.window.Window(width=800, height=600, caption='SCARA simulator')
# pyglet.gl.glClearColor(0.8, 1, 1, 1)

# Axes setup
x_axis_length = 200
axes = axes.Axes(window)
axes.create_x_axis(x_axis_length)

y_axis_length = 200
axes.create_y_axis(y_axis_length)


origin_point = axes.get_origin()

origin_point_x = origin_point[0]
origin_point_y = origin_point[1]


# SCARA scheme
# BaseLink - Joint1 - Link1 - Joint2 - Link2

my_scara = scara.Scara(origin_point)

my_scara.add_base()
my_scara.add_joint()
my_scara.add_link(length = 80, start_angle = 30)
my_scara.add_joint()
my_scara.add_link(length = 80, start_angle = 120)
my_scara.add_joint()
my_scara.add_link(length = 40, start_angle = 200)

# my_scara.add_joint()
# my_scara.add_link(length = 120, start_angle = 30)

# my_scara.add_joint()
# my_scara.add_link(length = 80, start_angle = 170)

for link in my_scara.links:
    link.add_angle_arc()

# my_scara.links[0].add_angle_arc()
# my_scara.links[1].add_angle_arc()

# my_scara.add_angle_arc(link_index = 0)
# my_scara.add_angle_arc(link_index = 1)
# my_scara.add_angle_arc(link_index = 2)

# scara_batch = pyglet.graphics.Batch()

# base_side_len = 20
# base_point_x = origin_point_x - base_side_len // 2
# base_point_y = origin_point_y - base_side_len // 2

# base_link = pyglet.shapes.Box(base_point_x, base_point_y, 
#                               base_side_len, base_side_len, 
#                               thickness=1, color=(123, 255, 120), batch=scara_batch)

# joint_radius = 4

# joint1 = pyglet.shapes.Circle(origin_point_x, origin_point_y,
#                               joint_radius, 
#                               segments=None, 
#                               color=(255, 255, 255, 255), 
#                               batch=scara_batch)


# link_width = 2

# link1_start_x = joint1.x
# link1_start_y = joint1.y
# link1_len = 80
link1_angle = 0
link2_angle = 0
# link1 = pyglet.shapes.Line(link1_start_x, link1_start_y,
#                            link1_start_x + link1_len * math.cos(math.radians(link1_angle)),
#                            link1_start_y + link1_len * math.sin(math.radians(link1_angle)),
#                            width=link_width, color=(120, 110, 50), batch=scara_batch)

# angle_arc_radius = 28
# angle_value_format = "{:.1f}"

# link1_arc = pyglet.shapes.Arc(link1_start_x, link1_start_y, 
#                               angle_arc_radius, 
#                               segments=None, 
#                               angle=math.radians(link1.rotation), 
#                               start_angle=0, 
#                               closed=False, 
#                               color=(120, 120, 120, 200), 
#                               batch=scara_batch)

# link1_arc_label = pyglet.text.Label(text=angle_value_format.format(link1_arc.angle),
#                                  font_size=10,
#                                  color=(120, 120, 120, 200),
#                                  x=link1_start_x + angle_arc_radius + 18,
#                                  y=link1_start_y + angle_arc_radius - 8,
#                                  anchor_x='center',
#                                  anchor_y='center',
#                                  batch=scara_batch)


# joint2 = pyglet.shapes.Circle(link1.x2, link1.y2,
#                               joint_radius, 
#                               segments=None, 
#                               color=(255, 255, 255, 255), 
#                               batch=scara_batch)

# link2 = pyglet.shapes.Line(joint2.x, joint2.y,
#                            343, 123,
#                            width=link_width, color=(20, 200, 100), batch=scara_batch)

# Clockwise rotation of the shape in degrees
# It will be rotated about its (anchor_x, anchor_y) position, 
# which defaults to the first vertex point of the shape.
# Can be used to rotate line
#  line.rotation = -90 

def update_link1(dt):
    global link1_angle
    global link2_angle

    # Update the end point of the line based on the new angle
    link1_angle += 30 * dt
    link2_angle += 90 * dt

    my_scara.joints[0].rotate(link1_angle)
    my_scara.joints[1].rotate(link2_angle)


    # rad = math.radians(link1_angle)

    # # link1.rotation = -link1_angle

    # link1.x2 = link1_start_x + link1_len * math.cos(rad)
    # link1.y2 = link1_start_y + link1_len * math.sin(rad)

    # arc1_angle_value = link1_angle % 360
    # link1_arc.angle = math.radians(arc1_angle_value)
    # link1_arc_label.text = angle_value_format.format(arc1_angle_value)

    # joint2.x = link1.x2
    # joint2.y = link1.y2

    # link2.x = joint2.x
    # link2.y = joint2.y

@window.event
def on_draw():
    window.clear()
    axes.draw()
    # scara_batch.draw()
    my_scara.draw()
    


pyglet.clock.schedule_interval(update_link1, 1 / 60.0)  # Update at 60 FPS
pyglet.app.run()
