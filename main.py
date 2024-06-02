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
my_scara.add_link(length = 80, start_angle = 0)
my_scara.add_joint()
my_scara.add_link(length = 40, start_angle = 0)
my_scara.add_end_effector()

for link in my_scara.links:
    link.add_angle_arc()

controller = controller.TwoJointScaraController(my_scara)

# Demo target point
target_point = ax.Point(x = -30, y = -30)
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

def update_scara_motion(dt):
    controller.update(queues)

@window.event
def on_draw():
    window.clear()
    axes.draw()
    my_scara.draw()
    trajectory.draw()
    fps_display.draw()

pyglet.clock.schedule_interval(update_scara_motion, 1 / 60.0)  # Update at 60 FPS
pyglet.app.run()
