from robodk import robodk
from robolink.robolink import Robolink
from svgpy import svg
from config import CaseConfig

import os
import sys


class Engrave:
    _APPROACH = 100  # Approach distance to objects
    IMAGE_SIZE_FLAT = svg.Point(112, 58)  # size of the image in MM not including edge (2mm)
    IMAGE_SIZE_EDGE = svg.Point(104, 40)  # size of image in MM not including edge (??? mm)
    IMAGE_SIZE_CURVED = svg.Point(112, 58)  # size of image in MM not including edge (??? mm)
    RDK = Robolink()  # Establish contact with RoboDK

    # Constructor definition
    # Always called __init__
    # Defined to independently to collect data from the
    # config file.

    def __init__(self):
        if os.path.isfile(CaseConfig.file()):  # If the given path is a file
            self.svg = svg.svg_load(CaseConfig.file())  # Load that file
        else:
            self.svg = svg.svg_load(CaseConfig.file('DEFAULT'))  # Else load a default file
        self.curve = CaseConfig.curve_style()  # Load the curve from the customer
        self.color = CaseConfig.colour()  # Load the color from the customer

    def point2D_2_pose(self, point, tangent):
        return robodk.transl(point.x, point.y, 0) * robodk.rotz(tangent.angle())

    def begin_flat(self):
        robot = self.RDK.Item('cart_robot')
        home_trans = robot.JointsHome()
        item_frame = robot.Childs()
        tool_frame = self.RDK.Item('tool')
        pix_ref = self.RDK.Item('pixel')
        self.move_to_environment()
        item = self.RDK.Item(f'cover_{self.color}_none')

        robot.setPoseFrame(robot.Childs())
        robot.setPoseTool('tool')

        if robot.item.Valid():
            self.svg.calc_polygon_fit(self.IMAGE_SIZE_FLAT)
            # size_img = self.svg.size_poly() # Uncertain if needed
            for path in self.svg:
                # use the pixel reference to set the path color, set pixel width and copy as a reference
                print('Drawing %s, RGB color = [%.3f,%.3f,%.3f]' % (path.idname, path.fill_color[0], path.fill_color[1], path.fill_color[2]))
                pix_ref.Recolor(path.fill_color)
                pix_ref.Copy()
                np = path.nPoints()
                p_0 = path.getPoint(0)
                orient_frame2tool = robodk.invH(item_frame.Pose()) * robot.SolveFK(home_trans) * tool_frame.Pose()
                orient_frame2tool[0:3, 3] = robodk.Mat([0, 0, 0])
                target0 = robodk.transl(p_0.x, p_0.y, 0) * orient_frame2tool
                target0_app = target0 * robodk.transl(0, 0, -self._APPROACH)
                robot.MoveL(target0_app)

                self.RDK.RunMessage('Drawing %s' % path.idname)
                self.RDK.RunProgram('SetColorRGB(%.3f,%.3f,%.3f)' % (path.fill_color[0], path.fill_color[1], path.fill_color[2]))
                for i in range(np):
                    p_i = path.getPoint(i)
                    v_i = path.getVector(i)

                    pt_pose = self.point2D_2_pose(p_i, v_i)
                    target = robodk.transl(p_i.x, p_i.y, 0) * orient_frame2tool
                    robot.MoveL(target)

                    # create a new pixel object with the calculated pixel pose
                    item.Paste().setPose(pt_pose)
                    target_app = target * robodk.transl(0, 0, -self._APPROACH)
                    robot.MoveL(target_app)

                robot.MoveL(home_trans)

    def begin_edge(self):
        robot = self.RDK.Item('cart_robot')
        home_trans = robot.JointsHome()
        item_frame = robot.Childs()
        tool_frame = self.RDK.Item('tool')
        pix_ref = self.RDK.Item('pixel')
        self.move_to_environment()
        item = self.RDK.Item(f'cover_{self.color}_edge')

        robot.setPoseFrame(robot.Childs())
        robot.setPoseTool('tool')

        if robot.item.Valid():
            self.svg.calc_polygon_fit(self.IMAGE_SIZE_EDGE)
            # size_img = self.svg.size_poly() # Uncertain if needed
            for path in self.svg:
                # use the pixel reference to set the path color, set pixel width and copy as a reference
                print('Drawing %s, RGB color = [%.3f,%.3f,%.3f]' % (path.idname, path.fill_color[0], path.fill_color[1], path.fill_color[2]))
                pix_ref.Recolor(path.fill_color)
                pix_ref.Copy()
                np = path.nPoints()
                p_0 = path.getPoint(0)
                orient_frame2tool = robodk.invH(item_frame.Pose()) * robot.SolveFK(home_trans) * tool_frame.Pose()
                orient_frame2tool[0:3, 3] = robodk.Mat([0, 0, 0])
                target0 = robodk.transl(p_0.x, p_0.y, 0) * orient_frame2tool
                target0_app = target0 * robodk.transl(0, 0, -self._APPROACH)
                robot.MoveL(target0_app)

                self.RDK.RunMessage('Drawing %s' % path.idname)
                self.RDK.RunProgram('SetColorRGB(%.3f,%.3f,%.3f)' % (path.fill_color[0], path.fill_color[1], path.fill_color[2]))
                for i in range(np):
                    p_i = path.getPoint(i)
                    v_i = path.getVector(i)

                    pt_pose = self.point2D_2_pose(p_i, v_i)
                    target = robodk.transl(p_i.x, p_i.y, 0) * orient_frame2tool
                    robot.MoveL(target)

                    # create a new pixel object with the calculated pixel pose
                    item.Paste().setPose(pt_pose)
                    target_app = target * robodk.transl(0, 0, -self._APPROACH)
                    robot.MoveL(target_app)

                robot.MoveL(home_trans)

    def begin_curved(self):
        robot = self.RDK.Item('cart_robot')
        home_trans = robot.JointsHome()
        item_frame = robot.Childs()
        tool_frame = self.RDK.Item('tool')
        pix_ref = self.RDK.Item('pixel')
        self.move_to_environment()
        item = self.RDK.Item(f'cover_{self.color}_curved')

        robot.setPoseFrame(robot.Childs())
        robot.setPoseTool('tool')

        if robot.item.Valid():
            self.svg.calc_polygon_fit(self.IMAGE_SIZE_EDGE)
            # size_img = self.svg.size_poly() # Uncertain if needed
            for path in self.svg:
                # use the pixel reference to set the path color, set pixel width and copy as a reference
                print('Drawing %s, RGB color = [%.3f,%.3f,%.3f]' % (path.idname, path.fill_color[0], path.fill_color[1], path.fill_color[2]))
                pix_ref.Recolor(path.fill_color)
                pix_ref.Copy()
                np = path.nPoints()

                p_0 = path.getPoint(0)
                orient_frame2tool = robodk.invH(item_frame.Pose()) * robot.SolveFK(home_trans) * tool_frame.Pose()
                orient_frame2tool[0:3, 3] = robodk.Mat([0, 0, 0])
                target0 = robodk.transl(p_0.x, p_0.y, 0) * orient_frame2tool
                target0_app = target0 * robodk.transl(0, 0, -self._APPROACH)
                robot.MoveL(target0_app)

                self.RDK.RunMessage('Drawing %s' % path.idname)
                self.RDK.RunProgram('SetColorRGB(%.3f,%.3f,%.3f)' % (path.fill_color[0], path.fill_color[1], path.fill_color[2]))
                for i in range(np):
                    p_i = path.getPoint(i)
                    v_i = path.getVector(i)

                    pt_pose = self.point2D_2_pose(p_i, v_i)
                    target = robodk.transl(p_i.x, p_i.y, 0) * orient_frame2tool
                    robot.MoveL(target)

                    # create a new pixel object with the calculated pixel pose
                    item.Paste().setPose(pt_pose)
                    target_app = target * robodk.transl(0, 0, -self._APPROACH)
                    robot.MoveL(target_app)

                robot.MoveL(home_trans)

    def move_to_environment(self):
        robot = self.RDK.Item('cart_robot')
        position_cart_robot = [0, 0, 0, 0, 0, 0]

        if robot.item.Valid():
            robot.setPoseFrame('cart_robot')
            robot.MoveL(position_cart_robot)
            robot.setPoseFrame(robot.Childs())
            robot.setPoseTool('tool')


    # Only needed if we do rotary engraving

    # if TCP_KEEP_TANGENCY:
    # moving the tool along the path (axis 6 may reach its limits)
    # target = pt_pose * orient_frame2tool
