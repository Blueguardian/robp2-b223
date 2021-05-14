from robodk import *
from svgpy import svg
from config import CaseConfig
from stock import Stock
from statistics import Statistics
from math import sqrt, pow, fabs

import os


class Engrave:
    _APPROACH = 100
    IMAGE_SIZE_NONE = svg.Point(50, 104)  # size of the image in MM not including edge (2mm)
    IMAGE_SIZE_EDGE = svg.Point(40, 104)  # size of image in MM not including edge (??? mm)
    IMAGE_SIZE_CURVED = svg.Point(56, 108)  # size of image in MM not including edge (??? mm)
    stock = Stock()
    _PIXEL_SIZE = 0.5

    def __init__(self, rdk):
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
        self.RDK = rdk
        self.stat = Statistics()

    @staticmethod
    def point2d_2_pose(point, tangent):
        """
        Translates a point to a point in 3D space
        :param point: Point object containing members x and y
        :param tangent: Tangent object containing method angle
        :return: Returns a 4 x 4 matrix of the point
        """
        return transl(point.x, point.y, 0)* rotz(tangent.angle())

    @staticmethod
    def curved_add_z(x):
        y = pow(57, 2)-pow(x, 2)
        z = (8/57)*sqrt(y)
        return z

    def begin_flat(self):
        """
        Engraving for flat covers

        Instructions sent to the robot in RoboDK for engraving the cover depending on the file given
        """
        robot = self.RDK.Item('engraver', 2)
        item_frame = self.RDK.Item('engrave_flat', 3)
        tool_frame = self.RDK.Item('laser_tool', 4)
        pix_ref = self.RDK.Item('pixel', 5)
        self.move_to_environment()
        stock_int = self.stock.get(f'{self.color}_{self.curve}')
        stock_int = stock_int + 1
        item = self.RDK.Item(f'cover_{self.color}_none_{stock_int}', 5)
        robot.setSpeed(500)

        # Set the necessary frame for controlling the engraving mechanism



        self.svg.calc_polygon_fit(self.IMAGE_SIZE_NONE, self._PIXEL_SIZE)
        # size_img = self.svg.size_poly() # Uncertain if needed
        for path in self.svg:
            path.polygon_move(-27, 0)
            # use the pixel reference to set the path color, set pixel width and copy as a reference
            print('Drawing %s, RGB color = [%.3f,%.3f,%.3f]' % (
                path.idname, path.fill_color[0], path.fill_color[1], path.fill_color[2]))
            pix_ref.Recolor(path.fill_color)
            pix_ref.Copy()
            point_quantity = path.nPoints()
            point_0 = path.getPoint(0)
            point_0.switchXY()
            orient_frame2tool = invH(item_frame.Pose()) * robot.SolveFK(robot.JointsHome()) * tool_frame.Pose()
            orient_frame2tool[0:3, 3] = Mat([0, 0, 0])
            target0 = transl(point_0.x, point_0.y, -299) * orient_frame2tool * Pose(0, 0, 0, -180, 0, 270)
            target0_app = target0
            robot.MoveL(target0_app)

            self.RDK.RunMessage('Drawing %s' % path.idname)
            self.RDK.RunProgram('SetColorRGB(%.3f,%.3f,%.3f)' % (
                path.fill_color[0], path.fill_color[1], path.fill_color[2]))

            for point in range(point_quantity):
                path_point = path.getPoint(point)
                path_point.switchXY()
                path_vector = path.getVector(point)
                point_pose = self.point2d_2_pose(path_point, path_vector)
                path_target = transl(path_point.x, path_point.y, -299) * orient_frame2tool * Pose(0, 0, 0, -180, 0, 270)
                print(path_target)
                robot.MoveL(path_target)

                # create a new pixel object with the calculated pixel pose
                point_pose = transl(path_point.x + 5.2, 12, -path_point.y+67.55) * orient_frame2tool * Pose(0, 0, 0, 90, 0, 0)
                item.AddGeometry(pix_ref, point_pose)
            target_app = path_target
            robot.MoveL(target_app)

        robot.MoveJ(robot.JointsHome())
        self.move_from_environment()
        stat_str = self.color + '_' + self.curve + '_engraved'
        self.stat.add(stat_str, 1)

    def begin_edge(self):
        """
        Engraving for curved edges covers

        Instructions sent to the robot in RoboDK for engraving the cover depending on the file given
        """
        robot = self.RDK.Item('engraver', 2)
        item_frame = self.RDK.Item('engrave_flat', 3)
        tool_frame = self.RDK.Item('laser_tool', 4)
        pix_ref = self.RDK.Item('pixel', 5)
        self.move_to_environment()
        stock_str = self.color + '_' + self.curve
        stock_int = self.stock.get(f'{self.color}_{self.curve}')
        stock_int = stock_int + 1
        item = self.RDK.Item(f'cover_{self.color}_edge_{stock_int}', 5)

        self.svg.calc_polygon_fit(self.IMAGE_SIZE_EDGE, self._PIXEL_SIZE)
        # size_img = self.svg.size_poly() # Uncertain if needed
        for path in self.svg:
            path.polygon_move(-30, 20)
            # use the pixel reference to set the path color, set pixel width and copy as a reference
            print('Drawing %s, RGB color = [%.3f,%.3f,%.3f]' % (
                path.idname, path.fill_color[0], path.fill_color[1], path.fill_color[2]))
            pix_ref.Recolor(path.fill_color)
            pix_ref.Copy()
            point_quantity = path.nPoints()
            point_0 = path.getPoint(0)
            point_0.switchXY()
            orient_frame2tool = invH(item_frame.Pose()) * robot.SolveFK(robot.JointsHome()) * tool_frame.Pose()
            orient_frame2tool[0:3, 3] = Mat([0, 0, 0])
            target0 = transl(point_0.x, point_0.y, -296.38) * orient_frame2tool * Pose(0, 0, 0, -180, 0, 270)
            target0_app = target0
            robot.MoveL(target0_app)

            self.RDK.RunMessage('Drawing %s' % path.idname)
            self.RDK.RunProgram('SetColorRGB(%.3f,%.3f,%.3f)' % (
                path.fill_color[0], path.fill_color[1], path.fill_color[2]))

            for point in range(point_quantity):
                path_point = path.getPoint(point)
                path_point.switchXY()
                path_vector = path.getVector(point)
                point_pose = self.point2d_2_pose(path_point, path_vector)
                path_target = transl(path_point.x, path_point.y, -296.38) * orient_frame2tool * Pose(0, 0, 0, -180, 0, 270)
                print(path_target)
                robot.MoveL(path_target)

                # create a new pixel object with the calculated pixel pose
                point_pose = transl(path_point.x + 5.2, 14.75, -path_point.y + 67.55) * orient_frame2tool * Pose(0, 0, 0, 90, 0, 0)
                item.AddGeometry(pix_ref, point_pose)
            target_app = path_target
            robot.MoveL(target_app)

        robot.MoveJ(robot.JointsHome())
        self.move_from_environment()
        stat_str = self.color + '_' + self.curve + '_engraved'
        self.stat.add(stat_str, 1)

    def begin_curved(self):
        """
        Engraving for curved covers

        Instructions sent to the robot in RoboDK for engraving the cover depending on the file given
        """
        robot = self.RDK.Item('engraver', 2)
        item_frame = self.RDK.Item('engrave_flat', 3)
        tool_frame = self.RDK.Item('laser_tool', 4)
        pix_ref = self.RDK.Item('pixel', 5)
        self.move_to_environment()
        stock_str = self.color + '_' + self.curve
        stock_int = self.stock.get(f'{self.color}_{self.curve}')
        stock_int = stock_int + 1
        item = self.RDK.Item(f'cover_{self.color}_curved_{stock_int}', 5)
        robot.setSpeed(1000)

        self.svg.calc_polygon_fit(self.IMAGE_SIZE_CURVED, self._PIXEL_SIZE)
        # size_img = self.svg.size_poly() # Uncertain if needed
        for path in self.svg:
            path.polygon_move(-23, 19)
            # use the pixel reference to set the path color, set pixel width and copy as a reference
            print('Drawing %s, RGB color = [%.3f,%.3f,%.3f]' % (
                path.idname, path.fill_color[0], path.fill_color[1], path.fill_color[2]))
            pix_ref.Recolor(path.fill_color)
            pix_ref.Copy()
            point_quantity = path.nPoints()
            point_0 = path.getPoint(0)
            point_0.switchXY()
            orient_frame2tool = invH(item_frame.Pose()) * robot.SolveFK(robot.JointsHome()) * tool_frame.Pose()
            orient_frame2tool[0:3, 3] = Mat([0, 0, 0])
            target0 = transl(point_0.x, point_0.y, -302.8+self.curved_add_z(fabs(point_0.y)-23.3)) * orient_frame2tool * Pose(0, 0, 0, -180, 0, 270)
            target0_app = target0
            robot.MoveL(target0_app)

            self.RDK.RunMessage('Drawing %s' % path.idname)
            self.RDK.RunProgram('SetColorRGB(%.3f,%.3f,%.3f)' % (
                path.fill_color[0], path.fill_color[1], path.fill_color[2]))

            for point in range(point_quantity):
                path_point = path.getPoint(point)
                path_point.switchXY()
                path_vector = path.getVector(point)
                point_pose = self.point2d_2_pose(path_point, path_vector)
                path_target = transl(path_point.x, path_point.y, -302.8 + self.curved_add_z(fabs(path_point.y)-23.3)) * orient_frame2tool * Pose(0, 0, 0, -180, 0, 270)

                robot.MoveL(path_target)

                # create a new pixel object with the calculated pixel pose 20.67
                point_pose = transl(path_point.x + 5.2, 12+self.curved_add_z(fabs(path_point.y)-23.3), -path_point.y +67.55) * orient_frame2tool * Pose(0, 0, 0, 90, 0, 0)
                print(point_pose)
                item.AddGeometry(pix_ref, point_pose)
            target_app = path_target
            robot.MoveL(target_app)

        robot.MoveJ(robot.JointsHome())
        self.move_from_environment()
        stat_str = self.color + '_' + self.curve + '_engraved'
        self.stat.add(stat_str, 1)

    def move_to_environment(self):
        """
        Moves the cover into the engraving environment
        """
        robot = self.RDK.Item('moving_plate')
        plate_ref = self.RDK.Item('engraving_plate_ref', 3)
        position_engraving = Pose(318, 0, 16.3, 0, 0, 0)
        robot.setPoseFrame(plate_ref)
        robot.MoveL(position_engraving)

    def move_from_environment(self):
        """
        Moves the cover from the engraving environment
        """
        robot = self.RDK.Item('moving_plate')
        plate_ref = self.RDK.Item('engraving_plate_ref', 3)
        position_engraving_out = Pose(145, 0, 16.3, 0, 0, 0)
        robot.setPoseFrame(plate_ref)
        robot.MoveL(position_engraving_out)

