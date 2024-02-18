import pyglet
import math
import sys

import axes as ax
import model
import controller

window = pyglet.window.Window(width=800, height=600, caption='SCARA simulator')
# pyglet.gl.glClearColor(0.8, 1, 1, 1)
fps_display = pyglet.window.FPSDisplay(window)

# Axes setup
x_axis_length = 200
axes = ax.Axes(window)
axes.create_x_axis(x_axis_length)

y_axis_length = 200
axes.create_y_axis(y_axis_length)

# SCARA nodel:
# Base - Joint1 - Link1 - Joint2 - Link2 - EndEffector
my_scara = model.ScaraModel()

origin_point = axes.get_origin_point()

my_scara.add_base(origin_point)
my_scara.add_link(length = 80, start_angle = 45)
my_scara.add_joint()
my_scara.add_link(length = 40, start_angle = 60)
# my_scara.add_joint()
# my_scara.add_link(length = 40, start_angle = 90)

my_scara.add_end_effector()


for link in my_scara.links:
    link.add_angle_arc()


controller = controller.TwoJointScaraController(my_scara)



target_point = ax.Point(x = 70, y = -55)


# start_point = axes.point(x = 200, y = 200)

start_point = ax.Point(x = my_scara.end_effector.shape.x, y = my_scara.end_effector.shape.y)

trajectory = model.Trajectory(
    origin_point, 
    start_point,
    target_point)

degrees = controller.inverse_kinematics(target_point.x, target_point.y)


theta1 = degrees[0]
theta2 = degrees[1]

print("theta1: ", theta1, " theta2: ", theta2)

queues = controller.movement_planner(theta1, theta2)

my_scara.joints[0].rotate(theta1)
my_scara.joints[1].rotate(theta2)


link1_angle = my_scara.links[0].abs_angle
link2_angle = my_scara.links[1].abs_angle


def update_link1(dt):
    pass
    # global link1_angle
    # global link2_angle

    # link1_angle += step1 #* dt
    # link2_angle -= step2 #* dt

    # my_scara.joints[0].rotate(my_scara.links[0].abs_angle + 30 * dt)
    # my_scara.joints[1].rotate(my_scara.links[1].abs_angle + 100 * dt)

    # my_scara.joints[2].rotate(-link2_angle)

    # if controller.update(queues):
        # trajectory.add_start_point(target_point)


@window.event
def on_draw():
    window.clear()
    axes.draw()
    my_scara.draw()

    trajectory.draw()

    # fps_display.draw()

pyglet.clock.schedule_interval(update_link1, 1 / 60.0)  # Update at 60 FPS
pyglet.app.run()
