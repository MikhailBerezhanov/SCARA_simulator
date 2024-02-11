import pyglet
import math
import sys

import axes
import model
import controller

window = pyglet.window.Window(width=800, height=600, caption='SCARA simulator')
# pyglet.gl.glClearColor(0.8, 1, 1, 1)
fps_display = pyglet.window.FPSDisplay(window)

# Axes setup
x_axis_length = 200
axes = axes.Axes(window)
axes.create_x_axis(x_axis_length)

y_axis_length = 200
axes.create_y_axis(y_axis_length)

# SCARA nodel:
# Base - Joint1 - Link1 - Joint2 - Link2 - EndEffector
my_scara = model.ScaraModel()

origin = axes.get_origin()

my_scara.add_base(axes.get_origin())
my_scara.add_link(length = 80, start_angle = 0)
my_scara.add_joint()
my_scara.add_link(length = 40, start_angle = 0)
# my_scara.add_joint()
# my_scara.add_link(length = 40, start_angle = 90)

my_scara.add_end_effector()


for link in my_scara.links:
    link.add_angle_arc()


controller = controller.TwoJointScaraController(my_scara)

target_point_x = 64
target_point_y = 56

controller.add_target_point(axes.get_origin(), target_point_x, target_point_y)

degrees = controller.inverse_kinematics(target_point_x, target_point_y)


theta1 = degrees[0]
theta2 = degrees[1]

print("theta1: ", theta1, " theta2: ", theta2)

queues = controller.movement_planner(theta1, theta2)

# my_scara.joints[0].rotate(theta1)
# my_scara.joints[1].rotate(theta2)

step1 = 0.2

step2 = 0.2

link1_angle = my_scara.links[0].abs_angle
link2_angle = my_scara.links[1].abs_angle


steps_todo1 = abs(theta1 - link1_angle) // step1
print("steps_todo1: ", steps_todo1)
steps_todo2 = abs(theta2 - link2_angle) // step2

def update_link1(dt):
    # global link1_angle
    # global link2_angle

    # global steps_todo1
    # global steps_todo2

    # link1_angle += step1 #* dt
    # link2_angle -= step2 #* dt

    # print("link1_angle: ", link1_angle, " link2_angle: ", link2_angle)

    # if steps_todo1 > 0:
    #     my_scara.joints[0].rotate(link1_angle)
    #     steps_todo1 -= 1
    #     # print("steps_todo1: ", steps_todo1)

    # if steps_todo2 > 0:
    #     my_scara.joints[1].rotate(link2_angle)
    #     steps_todo2 -= 1


    # if steps_todo1 <= 0 and steps_todo2 <= 0:
    #     pyglet.clock.unschedule(update_link1)
    #     print("unscheduled")

    # my_scara.joints[0].rotate(-link1_angle)
    # my_scara.joints[1].rotate(link2_angle)

    # my_scara.joints[2].rotate(-link2_angle)

    controller.update(queues)


@window.event
def on_draw():
    window.clear()
    axes.draw()
    my_scara.draw()

    # fps_display.draw()

pyglet.clock.schedule_interval(update_link1, 1 / 60.0)  # Update at 60 FPS
pyglet.app.run()
