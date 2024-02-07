import pyglet
import math

# Chained objects:
# Joint has references on connected links:
#      [Link In]  <- (Joint) -> [Link Out]
#
# Link has referrences to which joints it's connected:
#    (Start Joint) <- [Link] -> (End Joint)

class Joint:
    JOINT_RADIUS = 4

    def __init__(self, start_point_x, start_point_y, link_in, link_out, batch):
        self.link_in = link_in
        self.link_out = link_out

        self.shape = pyglet.shapes.Circle(
            start_point_x, start_point_y,
            self.JOINT_RADIUS, 
            segments=None, 
            color=(255, 255, 255, 255), 
            batch=batch)

    def rotate(self, angle: int):
        if self.link_out:
            self.link_out.rotate(angle)

    def move(self, x: int, y: int):
        self.shape.x = x
        self.shape.y = y

        if self.link_out:
            self.link_out.move(x, y)

class EndEffector(Joint):
    def __init__(self, start_point_x: int, start_point_y: int, batch):
        super().__init__(start_point_x, start_point_y, None, None, batch)

        self.shape = pyglet.shapes.Arc(
            start_point_x, start_point_y, 
            self.JOINT_RADIUS + 2, 
            segments=None, 
            angle=math.radians(360), 
            start_angle=0, 
            closed=False, 
            color=(255, 255, 255, 255), 
            batch=batch)

    def rotate(self):
        pass

class Link:
    LINK_WIDTH = 3
    ANGLE_ARC_RADIUS = 28
    ANGLE_VALUE_FMT = "{:.0f}"
    ANGLE_VALUE_OFFSET_X = 10
    ANGLE_VALUE_OFFSET_Y = -8

    def __init__(self, start_joint, end_joint, length, start_angle, color, batch):
        self.angle_arc = None
        self.angle_arc_label = None
        
        self.start_joint = start_joint
        self.end_joint = end_joint
        self.parent_link = self.start_joint.link_in

        # absolute (in window coordinate system)
        self.abs_angle = start_angle 
        # relative (in previous link coordinate system)
        self.rel_angle = self.__relative_to_parent_angle(start_angle)     

        self.length = length
        self.batch = batch

        self.line = pyglet.shapes.Line(
            start_joint.shape.x, start_joint.shape.y,
            start_joint.shape.x + length * math.cos(math.radians(self.rel_angle)),
            start_joint.shape.y + length * math.sin(math.radians(self.rel_angle)),
            width=self.LINK_WIDTH, color=color, batch=batch)

        self.start_joint.link_out = self

    def __relative_to_parent_angle(self, angle: int):
        ''' Converting input angle to relative against parent link '''
        return self.parent_link.rel_angle + angle if self.parent_link else angle

    def __update_angle_arc(self, angle: int):
        if self.angle_arc and self.angle_arc_label:

            new_angle = angle % 360

            # changing arc side to negative half
            if new_angle > 180:
                new_angle -= 360

            self.angle_arc.angle = math.radians(new_angle)
            self.angle_arc_label.text = self.ANGLE_VALUE_FMT.format(new_angle)

    def __update_angle_arc_pos(self, x: int, y: int):
        if self.angle_arc and self.angle_arc_label:
            self.angle_arc.x = x
            self.angle_arc.y = y

            self.angle_arc.start_angle=math.radians(self.parent_link.rel_angle) if self.parent_link else 0

            self.angle_arc_label.x = x + self.ANGLE_ARC_RADIUS + self.ANGLE_VALUE_OFFSET_X
            self.angle_arc_label.y = y + self.ANGLE_ARC_RADIUS + self.ANGLE_VALUE_OFFSET_Y

    def __update_line_end_point(self, angle: int):
        ''' Updating the end point of the line based on the new angle '''
        rad = math.radians(angle)
        self.line.x2 = self.start_joint.shape.x + self.length * math.cos(rad)
        self.line.y2 = self.start_joint.shape.y + self.length * math.sin(rad)

    def __update_end_joint(self):
        ''' Move end joint to the line end '''
        if self.end_joint:
            self.end_joint.move(self.line.x2, self.line.y2)

    def add_angle_arc(self):
        start_x = self.line.x
        start_y = self.line.y

        self.angle_arc = pyglet.shapes.Arc(
            start_x, start_y, 
            self.ANGLE_ARC_RADIUS, 
            segments=None, 
            angle=math.radians(self.abs_angle),
            start_angle=math.radians(self.parent_link.rel_angle) if self.parent_link else 0, 
            closed=False, 
            color=(120, 120, 120, 200), 
            batch=self.batch)

        self.angle_arc_label = pyglet.text.Label(
            text=self.ANGLE_VALUE_FMT.format(math.degrees(self.angle_arc.angle)),
            font_size=10,
            color=(120, 120, 120, 200),
            x=start_x + self.ANGLE_ARC_RADIUS + self.ANGLE_VALUE_OFFSET_X,
            y=start_y + self.ANGLE_ARC_RADIUS + self.ANGLE_VALUE_OFFSET_Y,
            anchor_x='center',
            anchor_y='center',
            batch=self.batch)

    def rotate(self, angle: int):
        self.abs_angle = angle
        self.rel_angle = self.__relative_to_parent_angle(angle)

        self.__update_line_end_point(self.rel_angle)
        self.__update_angle_arc(self.abs_angle)
        self.__update_end_joint()

    def move(self, x: int, y: int):
        self.line.x = x
        self.line.y = y

        # parent_link angle was changed - recalculating relativeness
        self.rel_angle = self.__relative_to_parent_angle(self.abs_angle)

        self.__update_line_end_point(self.rel_angle)
        self.__update_angle_arc_pos(x, y)
        self.__update_end_joint()

class ScaraModel:
    BASE_LEN = 20
    GRIPPER_SIDE = 10

    def __init__(self):
        self.batch = pyglet.graphics.Batch()
        self.base = None 
        self.joints = []
        self.links = []
        self.end_effector = None

    def draw(self):
        self.batch.draw()

    def add_base(self, base_point: (int, int) = (0, 0)):
        base_x = base_point[0] - self.BASE_LEN // 2
        base_y = base_point[1] - self.BASE_LEN // 2

        self.base = pyglet.shapes.Rectangle(
            base_x, base_y, 
            self.BASE_LEN, self.BASE_LEN, 
            color=(120, 120, 120), batch=self.batch)

        joint = Joint(base_point[0], base_point[1], None, None, self.batch)
        self.joints.append(joint)

    def add_joint(self):
        if not self.links or self.links[-1].end_joint:
            raise Exception("Add joint failed - no free links available")

        start_x = self.links[-1].line.x2
        start_y = self.links[-1].line.y2

        joint = Joint(
            start_x, start_y,
            link_in=self.links[-1] if self.links else None,
            link_out=None,
            batch=self.batch)

        if self.links:
            self.links[-1].end_joint = joint

        self.joints.append(joint)

    def add_link(self, length: int, start_angle: int = 0):
        if not self.joints:
            raise Exception("Add link failed - no joints available")

        c = 20 * len(self.joints)
        color = (11 * c % 255, 123 * c % 255, 47 * c % 255)

        link = Link(
            start_joint = self.joints[-1], 
            end_joint = None,
            length= length, 
            start_angle = start_angle, 
            color = color,
            batch = self.batch)

        self.links.append(link)

    def add_end_effector(self):
        if not self.links or self.links[-1].end_joint:
            raise Exception("Add end_effector failed - no free links available")

        start_x = self.links[-1].line.x2
        start_y = self.links[-1].line.y2

        self.end_effector = EndEffector(start_x, start_y, self.batch)

        self.links[-1].end_joint = self.end_effector



class TargetPoint:
    def __init__(self, x: int, y: int, batch):
        self.item = pyglet.shapes.Circle(
            x, y,
            1, 
            segments=None, 
            color=(255, 255, 255, 255), 
            batch=batch)

# TODO:
class TwoJointScaraController:
    ''' 2-DOF Scara controller. Assuming model has 2 Joints and 2 Links'''

    def __init__(self, model: ScaraModel):
        self.model = model

        self.target_point = None

        # self.batch = 

    def add_target_point(self, origin_point, x: int, y: int):
        # TODO: add target point
        self.target_point = pyglet.shapes.Circle(
            origin_point[0] + x, 
            origin_point[1] + y,
            2,  
            color=(0, 0, 255, 255), 
            batch=self.model.batch)

    def inverse_kinematics(self, x: int, y: int) -> (int, int):
        L1 = self.model.links[0].length
        L2 = self.model.links[1].length

        arg2 = (x ** 2 + y ** 2 - L1 ** 2 - L2 ** 2) / (2 * L1 * L2)

        q2 = math.acos(arg2)

        # if (x < 0):
            # q2 *= -1

        print("q2: ", q2)


        arg1 = L2 * math.sin(q2) / (L1 + L2 * math.cos(q2))
        q1 = math.atan(y / x) - math.atan(arg1) 


        if (x < 0):
            q1 += math.pi

        print("q1: ", q1)


        

        return (math.degrees(q1), math.degrees(q2))

