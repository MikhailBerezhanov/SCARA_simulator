import pyglet
import math



# Base:Joint1 - Link1 - Joint2 - Link2
# Joint -> Link
# Link (->) Joint 

class Joint:

    def __init__(self, start_point_x, start_point_y, batch, link = None):
        self.link = link

        self.shape = pyglet.shapes.Circle(
            start_point_x, start_point_y,
            4, 
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



class Link:
    LINK_WIDTH = 2
    ANGLE_ARC_RADIUS = 28
    ANGLE_VALUE_FMT = "{:.0f}"

    def __init__(self, start_joint, end_joint, batch, length, start_angle):
        self.angle_arc = None
        self.angle_arc_label = None
        self.angle = start_angle

        self.len = length
        self.batch = batch

        self.start_joint = start_joint
        self.end_joint = end_joint

        self.link = pyglet.shapes.Line(
            start_joint.shape.x, start_joint.shape.y,
            start_joint.shape.x + length * math.cos(math.radians(start_angle)),
            start_joint.shape.y + length * math.sin(math.radians(start_angle)),
            width=self.LINK_WIDTH, color=(120, 110, 50), batch=batch)

    def add_angle_arc(self):
        start_x = self.link.x
        start_y = self.link.y

        self.angle_arc = pyglet.shapes.Arc(
            start_x, start_y, 
            self.ANGLE_ARC_RADIUS, 
            segments=None, 
            angle=math.radians(self.link.rotation),
            start_angle=0, 
            closed=False, 
            color=(120, 120, 120, 200), 
            batch=self.batch)

        self.angle_arc_label = pyglet.text.Label(
            text=self.ANGLE_VALUE_FMT.format(math.degrees(self.angle_arc.angle)),
            font_size=10,
            color=(120, 120, 120, 200),
            x=start_x + self.ANGLE_ARC_RADIUS + 18,
            y=start_y + self.ANGLE_ARC_RADIUS - 8,
            anchor_x='center',
            anchor_y='center',
            batch=self.batch)

    def rotate(self, angle):
        # pass
        # TODO:
        # 1. update end joint position if any
        # 2. update angle arc

        rad = math.radians(angle)
        self.angle = angle

        self.link.x2 = self.start_joint.shape.x + self.len * math.cos(rad)
        self.link.y2 = self.start_joint.shape.y + self.len * math.sin(rad)

        if self.angle_arc and self.angle_arc_label:
            arc_angle_value = self.angle % 360
            self.angle_arc.angle = math.radians(arc_angle_value)
            self.angle_arc_label.text = self.ANGLE_VALUE_FMT.format(arc_angle_value)

        if self.end_joint:
            self.end_joint.move(self.link.x2, self.link.y2)

            # self.end_joint.x = self.link.x2
            # self.end_joint.y = self.link.y2

    def move(self, x, y):
        self.link.x = x
        self.link.y = y

        # update x2, y2 point
        rad = math.radians(self.angle)
        self.link.x2 = self.start_joint.shape.x + self.len * math.cos(rad)
        self.link.y2 = self.start_joint.shape.y + self.len * math.sin(rad)

        if self.angle_arc and self.angle_arc_label:
            self.angle_arc.x = x
            self.angle_arc.y = y
            self.angle_arc_label.x = x
            self.angle_arc_label.y = y

        if self.end_joint:
            self.end_joint.move(self.link.x2, self.link.y2)

# Base - Joint1 - Link1 - Joint2 - Link2
class Scara:
    BASE_LEN = 20
    JOINT_RADIUS = 4

    # TODO;
    # class Joint:

    #     def __init__(self, start_x, start_y, batch):
    #         self.joint = pyglet.shapes.Circle(
    #             start_point_x, start_point_y,
    #             self.JOINT_RADIUS, 
    #             segments=None, 
    #             color=(255, 255, 255, 255), 
    #             batch=batch)

    def __init__(self, origin_point=(0, 0)):
        self.batch = pyglet.graphics.Batch()

        self.base_x = origin_point[0] - self.BASE_LEN // 2
        self.base_y = origin_point[1] - self.BASE_LEN // 2
        self.base = None 

        self.joints = []
        self.links = []

        self.arc = None 
        self.arc_label = None 

    def draw(self):
        self.batch.draw()

    def add_base(self):
        self.base = pyglet.shapes.Box(
            self.base_x, self.base_y, 
            self.BASE_LEN, self.BASE_LEN, 
            thickness=1, color=(123, 255, 120), batch=self.batch)

    def add_joint(self):
        if not self.links:
            start_point_x = self.base_x + self.BASE_LEN // 2
            start_point_y = self.base_y + self.BASE_LEN // 2
        else:
            start_point_x = self.links[-1].link.x2
            start_point_y = self.links[-1].link.y2


        joint = Joint(start_point_x, start_point_y, self.batch)

        # joint = pyglet.shapes.Circle(
        #     start_point_x, start_point_y,
        #     self.JOINT_RADIUS, 
        #     segments=None, 
        #     color=(255, 255, 255, 255), 
        #     batch=self.batch)

        if self.links:
            self.links[-1].end_joint = joint

        self.joints.append(joint)

    def add_link(self, length, start_angle = 0):
        if not self.joints:
            raise Exception("Add link failed - no joints available")

        # start_x = self.joints[-1].x
        # start_y = self.joints[-1].y

        link = Link(self.joints[-1], None, self.batch, length, start_angle)

        self.joints[-1].connect_link(link)

        self.links.append(link)


    def update(self): 
        pass
            # arc1_angle_value = link1_angle % 360
            # link1_arc.angle = math.radians(arc1_angle_value)
            # link1_arc_label.text = angle_value_format.format(arc1_angle_value)
