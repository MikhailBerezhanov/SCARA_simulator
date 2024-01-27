import pyglet
import math

# Base - Joint1 - Link1 - Joint2 - Link2
class Scara:
    BASE_LEN = 20
    JOINT_RADIUS = 4

    # TODO;
    # class Joint:

    class Link:
        LINK_WIDTH = 2
        ANGLE_ARC_RADIUS = 28
        ANGLE_VALUE_FMT = "{:.1f}"

        def __init__(self, start_x, start_y, batch, length, start_angle = 0):
            self.angle_arc = None
            self.angle_arc_label = None

            self.len = length
            self.batch = batch

            # TODO: add start + end joints

            self.link = pyglet.shapes.Line(
                start_x, start_y,
                start_x + length * math.cos(math.radians(start_angle)),
                start_y + length * math.sin(math.radians(start_angle)),
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
            pass
            # TODO:
            # 1. update end joint position if any
            # 2. update angle arc





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

        joint = pyglet.shapes.Circle(
            start_point_x, start_point_y,
            self.JOINT_RADIUS, 
            segments=None, 
            color=(255, 255, 255, 255), 
            batch=self.batch)

        self.joints.append(joint)

    def add_link(self, length, start_angle = 0):
        if not self.joints:
            raise Exception("Add link failed - no joints available")

        start_x = self.joints[-1].x
        start_y = self.joints[-1].y

        link = self.Link(start_x, start_y, self.batch, length, start_angle)

        self.links.append(link)


    def update(self): 
        pass
            # arc1_angle_value = link1_angle % 360
            # link1_arc.angle = math.radians(arc1_angle_value)
            # link1_arc_label.text = angle_value_format.format(arc1_angle_value)
