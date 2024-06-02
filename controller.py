import model
import math

from collections import deque

class TwoJointScaraController:
    ''' 2-DOF Scara controller. Assuming model has 2 Joints and 2 Links'''

    def __init__(self, model: model.ScaraModel):
        self.model = model

    def inverse_kinematics(self, x: int, y: int) -> (float, float):
        L1 = self.model.links[0].length
        L2 = self.model.links[1].length

        # Cosinus Theoreme
        arg2 = (x ** 2 + y ** 2 - L1 ** 2 - L2 ** 2) / (2 * L1 * L2)

        # TODO: Choosing positive cosinus angle (?) 
        # The return value lies in interval [0, pi] radians.
        theta2 = -math.acos(arg2)

        beta = math.atan(L2 * math.sin(theta2) / (L1 + L2 * math.cos(theta2)))
        gama = math.atan(y / x) # TODO: x == 0
        theta1 = gama - beta

        if (x < 0):
            theta1 += math.pi

        print("theta1: ", theta1)
        print("theta2: ", theta2)

        return (math.degrees(theta1), math.degrees(theta2))

    # constant velocity planner
    def movement_planner(self, theta1 = float, theta2 = float, dt = 0):
        q1 = deque()
        q2 = deque()

        joint1_step = 0.5
        joint2_step = 0.5

        link1_angle = self.model.links[0].abs_angle
        link2_angle = self.model.links[1].abs_angle

        steps_todo1 = int(abs(theta1 - link1_angle) // joint1_step)
        steps_todo2 = int(abs(theta2 - link2_angle) // joint2_step)

        # Fill the queues
        # TODO: determine directions of rotation
        for i in range(steps_todo1):
            link1_angle += joint1_step
            q1.append(link1_angle)

        for j in range(steps_todo2):
            link2_angle -= joint2_step
            q2.append(link2_angle)
        
        return (q1, q2)


    def update(self, queue_list):
        q1 = queue_list[0]
        q2 = queue_list[1]

        if len(q1) != 0:
            new_joint_angle = q1.popleft()
            self.model.joints[0].rotate(new_joint_angle)

        if len(q2) != 0:
            new_joint_angle = q2.popleft()
            self.model.joints[1].rotate(new_joint_angle)

        # True if finished
        return len(q1) == 0 and len(q2) == 0