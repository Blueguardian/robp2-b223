import robodk.robodk
from robolink.robolink import Robolink
from svgpy import svg
from config import CaseConfig

import os
import sys

class Engrave:
    _APPROACH = 100
    IMAGE_SIZE_FLAT = svg.Point(112, 58)  # size of the image in MM not including edge (2mm)
    IMAGE_SIZE_EDGE = svg.Point(112, 58)  # size of image in MM not including edge (??? mm)
    IMAGE_SIZE_CURVED = svg.Point(112, 58)  # size of image in MM not including edge (??? mm)
    RDK = Robolink()

    def __init__(self):
        self.svg = svg.svg_load(CaseConfig.file())
        self.curve = CaseConfig.curve_style()
        self.color = CaseConfig.colour()

    def point2D_2_pose(self, point, tangent):
        """Converts a 2D point to a 3D pose in the XY plane including rotation being tangent to the path"""
        return robodk.robodk.transl(point.x, point.y, 0) * robodk.robodk.rotz(tangent.angle())

    def begin(self):
        robot = self.RDK.Item('cart_robot')
        position_cart_robot = [0, 0, 0, 0, 0, 0]
        home_trans = robot.JointsHome()
        item_frame = robot.Childs()
        tool_frame = self.RDK.Item('tool')
        pix_ref = self.RDK.Item('pixel')
        self.move_to_environment()
        item = self.RDK.Item(f'cover_{self.color}_{self.curve}')

        robot.setPoseFrame(robot.Childs())
        robot.setPoseTool('tool')

        if self.curve == 'none' and robot.item.Valid():
            self.svg.calc_polygon_fit(self.IMAGE_SIZE_FLAT)
            size_img = self.svg.size_poly()
            for path in self.svg:
                # use the pixel reference to set the path color, set pixel width and copy as a reference
                print('Drawing %s, RGB color = [%.3f,%.3f,%.3f]' % (
                    path.idname, path.fill_color[0], path.fill_color[1], path.fill_color[2]))
                pix_ref.Recolor(path.fill_color)
                pix_ref.Copy()
                np = path.nPoints()
                p_0 = path.getPoint(0)
                orient_frame2tool = robodk.robodk.invH(item_frame.Pose()) * robot.SolveFK(home_trans) * tool_frame.Pose()
                orient_frame2tool[0:3, 3] = robodk.robodk.Mat([0, 0, 0])
                target0 = robodk.robodk.transl(p_0.x, p_0.y, 0) * orient_frame2tool
                target0_app = target0 * robodk.robodk.transl(0, 0, -self._APPROACH)
                robot.MoveL(target0_app)
                target0_app = target0 * robodk.robodk.transl(0, 0, -self._APPROACH)
                robot.MoveL(target0_app)
                self.RDK.RunMessage('Drawing %s' % path.idname)
                self.RDK.RunProgram('SetColorRGB(%.3f,%.3f,%.3f)' % (path.fill_color[0], path.fill_color[1], path.fill_color[2]))
                for i in range(np):
                    p_i = path.getPoint(i)
                    v_i = path.getVector(i)

                    pt_pose = self.point2D_2_pose(p_i, v_i)
                    target = robodk.robodk.transl(p_i.x, p_i.y, 0) * orient_frame2tool
                    robot.MoveL(target)

                    # create a new pixel object with the calculated pixel pose
                    item.Paste().setPose(pt_pose)
                    target_app = target * robodk.robodk.transl(0, 0, -self._APPROACH)
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
            # Begin engraving here, but only if the object is present


if TCP_KEEP_TANGENCY:
    # moving the tool along the path (axis 6 may reach its limits)
    target = pt_pose * orient_frame2tool

board_draw = framedraw.Paste()
board_draw.setVisible(True, False)
board_draw.setName('Board & image')
board_draw.Scale([size_img.x / 250, size_img.y / 250, 1])  # adjust the board size to the image size (scale)