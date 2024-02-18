import pyglet
import math

import axes

# Chained objects:
# Joint has references on connected links:
#      [Link In]  <- (Joint) -> [Link Out]
#
# Link has referrences to which joints it's connected:
#    (Start Joint) <- [Link] -> (End Joint)

class Joint:
    JOINT_RADIUS = 4

    def __init__(self, start_point: axes.Point, link_in, link_out, batch):
        self.link_in = link_in
        self.link_out = link_out

        self.shape = pyglet.shapes.Circle(
            start_point.x, start_point.y,
            self.JOINT_RADIUS, 
            segments=None, 
            color=(255, 255, 255, 255), 
            batch=batch)

    def rotate(self, angle: float):
        if self.link_out:
            self.link_out.rotate(angle)

    def move(self, target_point: axes.Point):
        self.shape.x = target_point.x
        self.shape.y = target_point.y

        if self.link_out:
            self.link_out.move(target_point)

class EndEffector(Joint):
    def __init__(self, start_point: axes.Point, batch):
        super().__init__(start_point, None, None, batch)

        self.shape = pyglet.shapes.Arc(
            start_point.x, start_point.y, 
            self.JOINT_RADIUS + 2, 
            segments = None, 
            angle = math.radians(360), 
            start_angle = 0, 
            closed = False, 
            color = (255, 255, 255, 255), 
            batch = batch)

    def rotate(self):
        pass

class Link:
    LINK_WIDTH = 3
    ANGLE_ARC_RADIUS = 28
    ANGLE_VALUE_FMT = "{:.1f}"
    ANGLE_VALUE_OFFSET_X = 10
    ANGLE_VALUE_OFFSET_Y = -8

    def __init__(self, start_joint: Joint, end_joint: Joint, length: int, start_angle: float, color, batch):
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

    def __relative_to_parent_angle(self, angle: float):
        ''' Converting input angle to relative against parent link '''
        return self.parent_link.rel_angle + angle if self.parent_link else angle

    def __update_angle_arc(self, angle: float):
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

            self.angle_arc.start_angle = math.radians(self.parent_link.rel_angle) if self.parent_link else 0

            self.angle_arc_label.x = x + self.ANGLE_ARC_RADIUS + self.ANGLE_VALUE_OFFSET_X
            self.angle_arc_label.y = y + self.ANGLE_ARC_RADIUS + self.ANGLE_VALUE_OFFSET_Y

    def __update_line_end_point(self, angle: float):
        ''' Updating the end point of the line based on the new angle '''
        rad = math.radians(angle)
        self.line.x2 = self.start_joint.shape.x + self.length * math.cos(rad)
        self.line.y2 = self.start_joint.shape.y + self.length * math.sin(rad)

    def __update_end_joint(self):
        ''' Move end joint to the line end '''
        if self.end_joint:
            self.end_joint.move(axes.Point(self.line.x2, self.line.y2))

    def add_angle_arc(self):
        start_x = self.line.x
        start_y = self.line.y

        self.angle_arc = pyglet.shapes.Arc(
            start_x, start_y, 
            self.ANGLE_ARC_RADIUS, 
            segments = None, 
            angle = math.radians(self.abs_angle),
            start_angle = math.radians(self.parent_link.rel_angle) if self.parent_link else 0, 
            closed = False, 
            color = (120, 120, 120, 200), 
            batch = self.batch)

        self.angle_arc_label = pyglet.text.Label(
            text = self.ANGLE_VALUE_FMT.format(math.degrees(self.angle_arc.angle)),
            font_size = 10,
            color = (120, 120, 120, 200),
            x=start_x + self.ANGLE_ARC_RADIUS + self.ANGLE_VALUE_OFFSET_X,
            y=start_y + self.ANGLE_ARC_RADIUS + self.ANGLE_VALUE_OFFSET_Y,
            anchor_x = 'center',
            anchor_y = 'center',
            batch = self.batch)

    def rotate(self, angle: float):
        self.abs_angle = angle
        self.rel_angle = self.__relative_to_parent_angle(angle)

        self.__update_line_end_point(self.rel_angle)
        self.__update_angle_arc(self.abs_angle)
        self.__update_end_joint()

    def move(self, target_point: axes.Point):
        self.line.x = target_point.x
        self.line.y = target_point.y

        # parent_link angle was changed - recalculating relativeness
        self.rel_angle = self.__relative_to_parent_angle(self.abs_angle)

        self.__update_line_end_point(self.rel_angle)
        self.__update_angle_arc_pos(target_point.x, target_point.y)
        self.__update_end_joint()

class ScaraModel:
    BASE_LEN = 20

    def __init__(self):
        self.batch = pyglet.graphics.Batch()
        self.base = None 
        self.joints = []
        self.links = []
        self.end_effector = None

    def draw(self):
        self.batch.draw()

    def add_base(self, base_point: axes.Point = axes.Point(0, 0)):
        base_x = base_point.x - self.BASE_LEN // 2
        base_y = base_point.y - self.BASE_LEN // 2

        self.base = pyglet.shapes.Rectangle(
            base_x, base_y, 
            self.BASE_LEN, self.BASE_LEN, 
            color=(120, 120, 120), batch=self.batch)

        joint = Joint(base_point, None, None, self.batch)
        self.joints.append(joint)

    def add_joint(self):
        if not self.links or self.links[-1].end_joint:
            raise Exception("Add joint failed - no free links available")

        start_point = axes.Point(x = self.links[-1].line.x2, y = self.links[-1].line.y2)

        joint = Joint(
            start_point = start_point,
            link_in = self.links[-1] if self.links else None,
            link_out = None,
            batch = self.batch)

        if self.links:
            self.links[-1].end_joint = joint

        self.joints.append(joint)

    def add_link(self, length: int, start_angle: float = 0.0):
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

        start_point = axes.Point(x = self.links[-1].line.x2, y = self.links[-1].line.y2)

        self.end_effector = EndEffector(start_point, self.batch)

        self.links[-1].end_joint = self.end_effector



### TODO ###

class TargetPoint:
    def __init__(self, target: axes.Point, batch):
        self.item = pyglet.shapes.Circle(
            target.x, target.y,
            1, 
            segments=None, 
            color=(255, 255, 255, 255), 
            batch=batch)

class Trajectory:
    def __init__(self, origin_point, start_point: axes.Point, target_point: axes.Point):
        self.batch = pyglet.graphics.Batch()

        self.origin_point = origin_point
        
        self.add_start_point(start_point)
        self.add_target_point(target_point)

    def remove_start_point(self):
        self.start_point = None

    def remove_target_point(self):
        self.target_point = None

    def add_start_point(self, point: axes.Point):
        self.start_point = pyglet.shapes.Circle(
            point.x, #self.origin_point[0] + x, 
            point.y, #self.origin_point[1] + y,
            radius = 3,  
            color = (122, 200, 120, 255), 
            batch = self.batch)

    # TODO: remove origin point influence
    def add_target_point(self, point: axes.Point):
        self.target_point = pyglet.shapes.Circle(
            self.origin_point.x + point.x, 
            self.origin_point.y + point.y,
            radius = 4,  
            color = (202, 0, 220, 255), 
            batch = self.batch)

    def draw(self):
        self.batch.draw()

class WorkZone:
    def __init__(self):
        self.batch = pyglet.graphics.Batch()

    def draw():
        self.batch.draw()

    def hide(self):
        pass