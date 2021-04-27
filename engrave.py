from robodk import robodk
from robolink.robolink import Robolink
from svgpy import svg
from config import CaseConfig
from stock import Stock
from statistics import Statistics

import os


class Engrave:
    _APPROACH = 100
    IMAGE_SIZE_NONE = svg.Point(112, 58)  # size of the image in MM not including edge (2mm)
    IMAGE_SIZE_EDGE = svg.Point(104, 40)  # size of image in MM not including edge (??? mm)
    IMAGE_SIZE_CURVED = svg.Point(107, 58)  # size of image in MM not including edge (??? mm)
    RDK = Robolink()
    stock = Stock()
    stat = Statistics()

    def __init__(self):
        """
        Constructor
        Checks whether an .svg file exist at the given location, if not loads a default .svg file
        and collects information from the config file
        """
        if os.path.isfile(CaseConfig.file()):
            self.svg = svg.svg_load(CaseConfig.file())
        else:
            self.svg = svg.svg_load(CaseConfig.file('DEFAULT'))
        self.curve = CaseConfig.curve_style()
        self.color = CaseConfig.colour()

    @staticmethod
    def point2d_2_pose(point, tangent):
        """
        Translates a point and an angle to a point and orientation in 3D space
        :param point: Point object containing members x and y
        :param tangent: Tangent object containing method angle
        :return: Returns a 4 x 4 matrix of the point
        """
        return robodk.transl(point.x, point.y, 0) * robodk.rotz(tangent.angle())

    def begin_flat(self):
        """
        Engraving for flat covers

        Instructions sent to the robot in RoboDK for engraving the cover depending on the file given
        """
        robot = self.RDK.Item('cart_robot')
        home_trans = robot.JointsHome()
        item_frame = robot.Childs()
        tool_frame = self.RDK.Item('tool')
        pix_ref = self.RDK.Item('pixel')
        self.move_to_environment()
        stock_str = self.color + '_' + self.curve
        item = self.RDK.Item(f'cover_{self.color}_none_{self.stock.get(stock_str)}')

        # Set the necessary frame for controlling the engraving mechanism
        robot.setPoseFrame(robot.Childs())
        robot.setPoseTool('tool')

        if robot.item.Valid():
            self.svg.calc_polygon_fit(self.IMAGE_SIZE_NONE)
            # size_img = self.svg.size_poly() # Uncertain if needed
            for path in self.svg:
                # use the pixel reference to set the path color, set pixel width and copy as a reference
                print('Drawing %s, RGB color = [%.3f,%.3f,%.3f]' % (
                    path.idname, path.fill_color[0], path.fill_color[1], path.fill_color[2]))
                pix_ref.Recolor(path.fill_color)
                pix_ref.Copy()
                point_quantity = path.nPoints()
                point_0 = path.getPoint(0)
                orient_frame2tool = robodk.invH(item_frame.Pose()) * robot.SolveFK(home_trans) * tool_frame.Pose()
                orient_frame2tool[0:3, 3] = robodk.Mat([0, 0, 0])
                target0 = robodk.transl(point_0.x, point_0.y, 0) * orient_frame2tool
                target0_app = target0 * robodk.transl(0, 0, -self._APPROACH)
                robot.MoveL(target0_app)

                self.RDK.RunMessage('Drawing %s' % path.idname)
                self.RDK.RunProgram('SetColorRGB(%.3f,%.3f,%.3f)' % (
                    path.fill_color[0], path.fill_color[1], path.fill_color[2]))

                for point in range(point_quantity):
                    path_point = path.getPoint(point)
                    path_vector = path.getVector(point)
                    point_pose = self.point2d_2_pose(path_point, path_vector)
                    path_target = robodk.transl(path_point.x, path_point.y, 0) * orient_frame2tool
                    robot.MoveL(path_target)

                    # create a new pixel object with the calculated pixel pose
                    item.Paste().setPose(point_pose)
                    target_app = path_target * robodk.transl(0, 0, -self._APPROACH)
                    robot.MoveL(target_app)

            robot.MoveL(home_trans)
            self.move_from_environment()
            stat_str = self.color + '_' + self.curve + '_engraved'
            self.stat.add(stat_str, 1)

    def begin_edge(self):
        """
        Engraving for curved edges covers

        Instructions sent to the robot in RoboDK for engraving the cover depending on the file given
        """
        robot = self.RDK.Item('cart_robot')
        home_trans = robot.JointsHome()
        item_frame = robot.Childs()
        tool_frame = self.RDK.Item('tool')
        pix_ref = self.RDK.Item('pixel')
        self.move_to_environment()
        stock_str = f'{self.color}_{self.curve}'
        item = self.RDK.Item(f'cover_{self.color}_edge_{self.stock.get(stock_str)}')

        # Set the necessary frame for controlling the engraving mechanism
        robot.setPoseFrame(robot.Childs())
        robot.setPoseTool('tool')

        if robot.item.Valid():
            self.svg.calc_polygon_fit(self.IMAGE_SIZE_NONE)
            # size_img = self.svg.size_poly() # Uncertain if needed
            for path in self.svg:
                # use the pixel reference to set the path color, set pixel width and copy as a reference
                print('Drawing %s, RGB color = [%.3f,%.3f,%.3f]' % (
                    path.idname, path.fill_color[0], path.fill_color[1], path.fill_color[2]))
                pix_ref.Recolor(path.fill_color)
                pix_ref.Copy()
                point_quantity = path.nPoints()
                point_0 = path.getPoint(0)
                orient_frame2tool = robodk.invH(item_frame.Pose()) * robot.SolveFK(home_trans) * tool_frame.Pose()
                orient_frame2tool[0:3, 3] = robodk.Mat([0, 0, 0])
                target0 = robodk.transl(point_0.x, point_0.y, 0) * orient_frame2tool
                target0_app = target0 * robodk.transl(0, 0, -self._APPROACH)
                robot.MoveL(target0_app)

                self.RDK.RunMessage('Drawing %s' % path.idname)
                self.RDK.RunProgram('SetColorRGB(%.3f,%.3f,%.3f)' % (
                    path.fill_color[0], path.fill_color[1], path.fill_color[2]))

                for point in range(point_quantity):
                    path_point = path.getPoint(point)
                    path_vector = path.getVector(point)
                    point_pose = self.point2d_2_pose(path_point, path_vector)
                    path_target = robodk.transl(path_point.x, path_point.y, 0) * orient_frame2tool
                    robot.MoveL(path_target)

                    # create a new pixel object with the calculated pixel pose
                    item.Paste().setPose(point_pose)
                    target_app = path_target * robodk.transl(0, 0, -self._APPROACH)
                    robot.MoveL(target_app)

            robot.MoveL(home_trans)
            self.move_from_environment()
            stat_str = self.color + '_' + self.curve + '_engraved'
            self.stat.add(stat_str, 1)

    def begin_curved(self):
        """
        Engraving for curved covers

        Instructions sent to the robot in RoboDK for engraving the cover depending on the file given
        """
        robot = self.RDK.Item('cart_robot')
        home_trans = robot.JointsHome()
        item_frame = robot.Childs()
        tool_frame = self.RDK.Item('tool')
        pix_ref = self.RDK.Item('pixel')
        self.move_to_environment()
        stock_str = f'{self.color}_{self.curve}'
        item = self.RDK.Item(f'cover_{self.color}_curved_{self.stock.get(stock_str)}')

        # Set the necessary frame for controlling the engraving mechanism
        robot.setPoseFrame(robot.Childs())
        robot.setPoseTool('tool')

        if robot.item.Valid():
            self.svg.calc_polygon_fit(self.IMAGE_SIZE_NONE)
            # size_img = self.svg.size_poly() # Uncertain if needed
            for path in self.svg:
                # use the pixel reference to set the path color, set pixel width and copy as a reference
                print('Drawing %s, RGB color = [%.3f,%.3f,%.3f]' % (
                    path.idname, path.fill_color[0], path.fill_color[1], path.fill_color[2]))
                pix_ref.Recolor(path.fill_color)
                pix_ref.Copy()
                point_quantity = path.nPoints()
                point_0 = path.getPoint(0)
                orient_frame2tool = robodk.invH(item_frame.Pose()) * robot.SolveFK(home_trans) * tool_frame.Pose()
                orient_frame2tool[0:3, 3] = robodk.Mat([0, 0, 0])
                target0 = robodk.transl(point_0.x, point_0.y, 0) * orient_frame2tool
                target0_app = target0 * robodk.transl(0, 0, -self._APPROACH)
                robot.MoveL(target0_app)

                self.RDK.RunMessage('Drawing %s' % path.idname)
                self.RDK.RunProgram('SetColorRGB(%.3f,%.3f,%.3f)' % (
                    path.fill_color[0], path.fill_color[1], path.fill_color[2]))

                for point in range(point_quantity):
                    path_point = path.getPoint(point)
                    path_vector = path.getVector(point)
                    point_pose = self.point2d_2_pose(path_point, path_vector)
                    path_target = robodk.transl(path_point.x, path_point.y, 0) * orient_frame2tool
                    robot.MoveL(path_target)

                    # create a new pixel object with the calculated pixel pose
                    item.Paste().setPose(point_pose)
                    target_app = path_target * robodk.transl(0, 0, -self._APPROACH)
                    robot.MoveL(target_app)

            robot.MoveL(home_trans)
            self.move_from_environment()
            stat_str = self.color + '_' + self.curve + '_engraved'
            self.stat.add(stat_str, 1)

    def move_to_environment(self):
        """
        Moves the cover into the engraving environment
        """
        robot = self.RDK.Item('engraving_plate')
        position_engraving = 100

        if robot.item.Valid():
            robot.setPoseFrame('engraving')
            robot.MoveL(position_engraving)

    def move_from_environment(self):
        """
        Moves the cover from the engraving environment
        """
        robot = self.RDK.Item('engraving_plate')
        robot.setJointsHome(0)

        if robot.item.Valid():
            robot.setPoseFrame('engraving')
            robot.JointsHome()

    # Only needed if we do rotary engraving

    # if TCP_KEEP_TANGENCY:
    # moving the tool along the path (axis 6 may reach its limits)
    # target = pt_pose * orient_frame2tool
