import pyglet
import math

# Chained classes:
# Joint -> Link
# Link (->) Joint 

class Joint:
    JOINT_RADIUS = 4

    def __init__(self, start_point_x, start_point_y, batch, link = None):
        self.link = link

        self.shape = pyglet.shapes.Circle(
            start_point_x, start_point_y,
            self.JOINT_RADIUS, 
            segments=None, 
            color=(255, 255, 255, 255), 
            batch=batch)

    def connect_link(self, link):
        self.link = link

    def rotate(self, angle):
        if self.link:
            self.link.rotate(angle)

    def move(self, x, y):
        self.shape.x = x
        self.shape.y = y

        if self.link:
            self.link.move(x, y)

class Gripper(Joint):
    def __init__(self, start_point_x, start_point_y, batch):
        super().__init__(start_point_x, start_point_y, batch)

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

    def __init__(self, start_joint, end_joint, batch, length, start_angle, color):
        self.angle_arc = None
        self.angle_arc_label = None
        self.angle = start_angle

        self.len = length
        self.batch = batch

        self.start_joint = start_joint
        self.end_joint = end_joint

        self.line = pyglet.shapes.Line(
            start_joint.shape.x, start_joint.shape.y,
            start_joint.shape.x + length * math.cos(math.radians(start_angle)),
            start_joint.shape.y + length * math.sin(math.radians(start_angle)),
            width=self.LINK_WIDTH, color=color, batch=batch)

        self.start_joint.connect_link(self)

    def add_angle_arc(self):
        start_x = self.line.x
        start_y = self.line.y

        self.angle_arc = pyglet.shapes.Arc(
            start_x, start_y, 
            self.ANGLE_ARC_RADIUS, 
            segments=None, 
            angle=math.radians(self.line.rotation),
            start_angle=0, 
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

    def rotate(self, angle):
        rad = math.radians(angle)
        self.angle = angle

        # Update the end point of the line based on the new angle
        self.line.x2 = self.start_joint.shape.x + self.len * math.cos(rad)
        self.line.y2 = self.start_joint.shape.y + self.len * math.sin(rad)

        if self.angle_arc and self.angle_arc_label:
            arc_angle_value = self.angle % 360
            self.angle_arc.angle = math.radians(arc_angle_value)
            self.angle_arc_label.text = self.ANGLE_VALUE_FMT.format(arc_angle_value)

        if self.end_joint:
            self.end_joint.move(self.line.x2, self.line.y2)

    def move(self, x, y):
        self.line.x = x
        self.line.y = y

        # Update the end point
        rad = math.radians(self.angle)
        self.line.x2 = self.start_joint.shape.x + self.len * math.cos(rad)
        self.line.y2 = self.start_joint.shape.y + self.len * math.sin(rad)

        if self.angle_arc and self.angle_arc_label:
            self.angle_arc.x = x
            self.angle_arc.y = y
            self.angle_arc_label.x = x + self.ANGLE_ARC_RADIUS + self.ANGLE_VALUE_OFFSET_X
            self.angle_arc_label.y = y + self.ANGLE_ARC_RADIUS + self.ANGLE_VALUE_OFFSET_Y

        if self.end_joint:
            self.end_joint.move(self.line.x2, self.line.y2)

class ScaraModel:
    BASE_LEN = 20
    GRIPPER_SIDE = 10

    def __init__(self):
        self.batch = pyglet.graphics.Batch()
        self.base = None 
        self.joints = []
        self.links = []
        self.gripper = None

    def draw(self):
        self.batch.draw()

    def add_base(self, base_point=(0, 0)):
        base_x = base_point[0] - self.BASE_LEN // 2
        base_y = base_point[1] - self.BASE_LEN // 2

        self.base = pyglet.shapes.Rectangle(
            base_x, base_y, 
            self.BASE_LEN, self.BASE_LEN, 
            color=(120, 120, 120), batch=self.batch)

        joint = Joint(base_point[0], base_point[1], self.batch)
        self.joints.append(joint)

    def add_joint(self):
        if not self.links or self.links[-1].end_joint:
            raise Exception("Add joint failed - no free links available")

        start_x = self.links[-1].line.x2
        start_y = self.links[-1].line.y2

        joint = Joint(start_x, start_y, self.batch)

        if self.links:
            self.links[-1].end_joint = joint

        self.joints.append(joint)

    def add_link(self, length, start_angle = 0):
        if not self.joints:
            raise Exception("Add link failed - no joints available")

        c = 20 * len(self.joints)
        color = (11 * c % 255, 123 * c % 255, 47 * c % 255)

        link = Link(self.joints[-1], None, self.batch, length, start_angle, color)

        self.links.append(link)

    def add_gripper(self):
        if not self.links or self.links[-1].end_joint:
            raise Exception("Add gripper failed - no free links available")

        start_x = self.links[-1].line.x2
        start_y = self.links[-1].line.y2

        self.gripper = Gripper(start_x, start_y, self.batch)

        self.links[-1].end_joint = self.gripper

# TODO:
class ScaraController:
    pass