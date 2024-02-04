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

# SCARA nodel:
# Base - Joint1 - Link1 - Joint2 - Link2 - EndEffector
my_scara = scara.ScaraModel()

my_scara.add_base(axes.get_origin())
my_scara.add_link(length = 80, start_angle = 50)
my_scara.add_joint()
my_scara.add_link(length = 80, start_angle = 30)
my_scara.add_joint()
my_scara.add_link(length = 40, start_angle = 90)

my_scara.add_end_effector()


for link in my_scara.links:
    link.add_angle_arc()


link1_angle = 0
link2_angle = 0

def update_link1(dt):
    global link1_angle
    global link2_angle

    link1_angle += 20 * dt
    link2_angle += 90 * dt

    my_scara.joints[0].rotate(-link1_angle)
    # my_scara.joints[1].rotate(link2_angle)

    # my_scara.joints[2].rotate(-link2_angle)


@window.event
def on_draw():
    window.clear()
    axes.draw()
    my_scara.draw()
    

pyglet.clock.schedule_interval(update_link1, 1 / 60.0)  # Update at 60 FPS
pyglet.app.run()
