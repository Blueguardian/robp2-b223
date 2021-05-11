# The following file contains code written by ROB2 - B223
# 2. Semester AAU 2021.

# Imports for class
import robolink.robolink
from robodk import *
from robolink import *
from robolink.robolink import Robolink
from config import CaseConfig
from stock import Stock
from statistics import Statistics


class Cover:
    # Global class variables
    # Distances in mm
    _OFFSETZ_NONE = 50
    _OFFSETZ_EDGE = 25
    _OFFSETZ_CURVED = 0.4
    _OFFSETX_COVER_DIST = 70
    _OFFSETY_COVER_DIST = 73
    _OFFSETZ_COVER_FLAT_DIST = 11.7
    _OFFSETZ_COVER_EDGE_DIST = 14.7
    _OFFSETZ_COVER_CURVED_DIST = 17.2
    _BOTTOM_COVER_HEIGHT = 13
    _TOP_COVER_INDENT_OFFSET = 5
    _COVER_CAPACITY = Stock.get_init()
    _APPROACH = 100
    _ROBOT_HOME = [0, 0, 0, 90, 0, 0, ]


    def __init__(self, color, curve_type, stock: Stock):
        """
        Constructor:
        Assigns the fields to the given parameters and corrects the position of the cover based on the parameters
        :param color: The color given in the config file
        :param curve_type: The curve type given in the config file
        :param stock: Stock Stock controlling object with type hint Stock
        """
        self.RDK = Robolink()
        self.color = color
        self.color = color
        self.curve = curve_type
        self.stock = stock
        self.stat = Statistics(self.RDK)
        self.position = Pose(45.5, self._OFFSETY_COVER_DIST, 0, -180, 0, 0)
        self.correct_pos(self.stock)
        self.stat = Statistics(self.RDK)

    # Define dictionary with the different types and give them an identifier
    def correct_pos(self, stock: Stock):
        """
        Corrects the position of the cover relative to the stock container, depending on the type of cover.
        Instead of giving each cover a static position
        :param stock: Stock controlling object with type hint Stock
        :return: The position of the specific cover
        """

        curve_types = {
            'black_none': 0,
            'black_edge': 3,
            'black_curved': 6,
            'white_none': 1,
            'white_edge': 4,
            'white_curved': 7,
            'blue_none': 2,
            'blue_edge': 5,
            'blue_curved': 8
        }

        case_types = {
            'black_none': 0,
            'black_edge': 1,
            'black_curved': 2,
            'white_none': 3,
            'white_edge': 4,
            'white_curved': 5,
            'blue_none': 6,
            'blue_edge': 7,
            'blue_curved': 8
        }

        case_curve = {
            'curved': 0,
            'edge': 1,
            'none': 2
        }

        curvature = case_curve[f'{self.curve}']
        print(curvature)
        if curvature == 1:
            self.position[2, 3] = self.position[2, 3] + self._OFFSETZ_EDGE + 1
        if curvature == 2:
            self.position[2, 3] = self.position[2, 3] + self._OFFSETZ_NONE + 1
        if curvature == 0:
            self.position[2, 3] = self.position[2, 3] + self._OFFSETZ_CURVED + 1

        identifier = case_types[f'{self.color}_{self.curve}']
        self.position[0, 3] = self.position[0, 3] + identifier * self._OFFSETX_COVER_DIST

        # Depending on the remaining stock and type of curve, calculate the Z-offset to compensate for the empty space
        identifier_curve = curve_types[f'{self.color}_{self.curve}']
        if identifier_curve in range(0, 3):
            self.position[2, 3] = self.position[2, 3] + stock.get(
                f'{self.color}_none') * self._OFFSETZ_COVER_FLAT_DIST
        if identifier_curve in range(3, 6):
            print(self.position)
            self.position[2, 3] = self.position[2, 3] + stock.get(
                f'{self.color}_edge') * self._OFFSETZ_COVER_EDGE_DIST
            print(self.position)
        if identifier_curve in range(6, 9):
            print(self.position)
            self.position[2, 3] = self.position[2, 3] + stock.get(
                f'{self.color}_curved') * self._OFFSETZ_COVER_CURVED_DIST
        print(self.position)

    def __str__(self):
        """
        String representation of the class
        :return: Prints the color, curve type and position of the cover
        """
        print(f'{self.color} curve_{self.curve} cover at {self.position}')

    def get_pos(self):
        """
        Debugging method
        :return:  Returns the position of the cover
        """
        return self.position

    def grab(self, robot):
        """
        Method that sends instructions to the robot in RoboDK to grab the cover from the stock container
        :param robot: Robot object representing the robot in RoboDK
        """
        frame = self.RDK.Item('storage', 3)
        robot.setPoseFrame(frame)
        position_copy = self.position
        if self.curve == 'none':
            position_copy[2, 3] = position_copy[2, 3] + self._APPROACH
        elif self.curve == 'edge':
            position_copy[2, 3] = position_copy[2, 3] + self._APPROACH
        elif self.curve == 'curved':
            position_copy[2, 3] = position_copy[2, 3] + self._APPROACH + 1
        robot.MoveJ(position_copy)

        robot.setSpeed(150)
        robot.MoveJ(position_copy)
        if self.curve == 'none':
            position_copy[2, 3] = position_copy[2, 3] - self._APPROACH
        elif self.curve == 'edge':
            position_copy[2, 3] = position_copy[2, 3] - self._APPROACH - 1
        elif self.curve == 'curved':
            position_copy[2, 3] = position_copy[2, 3] - self._APPROACH - 2.5
        robot.MoveL(position_copy)
        self.RDK.RunProgram('Prog6')

        position_copy[2, 3] = position_copy[2, 3] + self._APPROACH
        robot.MoveL(position_copy)
        robot.setSpeed(150)
        self.stock.sub(f'{self.color}_{self.curve}', 1)

    def give_top(self):
        """
        Sends instructions to RoboDK to grab a cover, place it on top of the bottom cover
        if the cover needs to be engraved, places it on the engraving plate.
        """
        carrier_offsetx = 88.7  # (Carrier length / 2)
        carrier_offsety = 55.3  # (Carrier width / 2)
        carrier_offsetz = 42.3  # (Carrier depth)


        carrier_position_app = Pose(carrier_offsetx, carrier_offsety, carrier_offsetz, -180, 0, -90)

        if self.curve == 'none':
            carrier_position_app[2, 3] = carrier_position_app[2, 3] + self._APPROACH
        if self.curve == 'edge':
            carrier_position_app[2, 3] = carrier_position_app[2, 3] + self._APPROACH
        if self.curve == 'curved':
            carrier_position_app[2, 3] = carrier_position_app[2, 3] + self._APPROACH

        self.RDK.Connect()
        robot = self.RDK.Item('fanuc', 2)
        robot.setTool(Pose(0, 0, 225.75, 0, 0, 0))
        self.grab(robot)

        carrier_ = self.RDK.Item('carrier', 3)
        robot.setPoseFrame(carrier_)
        robot.MoveJ(carrier_position_app)

        position_withoffset = carrier_position_app

        # Check the type of cover again and subtract the approach offset,
        # while considering that a cover is attached to the tool
        if self.curve == 'none':
            position_withoffset[2, 3] = position_withoffset[2, 3] - self._APPROACH + self._OFFSETZ_COVER_FLAT_DIST + 0.25
        if self.curve == 'edge':
            position_withoffset[2, 3] = position_withoffset[2, 3] - self._APPROACH + self._OFFSETZ_COVER_EDGE_DIST - 1.47
        if self.curve == 'curved':
            position_withoffset[2, 3] = position_withoffset[
                                            2, 3] - self._APPROACH + self._OFFSETZ_COVER_CURVED_DIST - 2.1

        # Take into account that it is now a whole phone
        position_withoffset[2, 3] = position_withoffset[
                                        2, 3] - self._TOP_COVER_INDENT_OFFSET + self._BOTTOM_COVER_HEIGHT

        robot.setSpeed(150)
        robot.MoveL(position_withoffset)
        str_cover = f'{self.color}_{self.curve}'
        cover = self.RDK.Item(f'cover_{self.color}_{self.curve}_{self.stock.get(str_cover)}')
        self.RDK.RunProgram('Prog7')
        carrier_position_app[2, 3] = carrier_position_app[2, 3] + self._APPROACH
        robot.MoveL(carrier_position_app)
        robot.setSpeed(150)
        engrave_check = CaseConfig.engrave()

        if engrave_check:
            engrave_plate_ref = self.RDK.Item('engraving_plate_ref', 3)
            robot.setPoseFrame(engrave_plate_ref)
            engrave_plate_pos_app = Pose(145.29, 0.05, 42.6, -180, 0, 90)

            # Check for type of cover an apply an approach to the z value
            if self.curve == 'none':
                engrave_plate_pos_app[2, 3] = engrave_plate_pos_app[2, 3] + self._APPROACH
            if self.curve == 'edge':
                engrave_plate_pos_app[2, 3] = engrave_plate_pos_app[2, 3] + self._APPROACH + 3
            if self.curve == 'curved':
                engrave_plate_pos_app[2, 3] = engrave_plate_pos_app[2, 3] + self._APPROACH + 5

            robot.MoveJ(engrave_plate_pos_app)
            engrave_plate_pos = engrave_plate_pos_app

            # Check for cover type and subtract the approach while taking into account carrying a phone
            if self.curve == 'none':
                engrave_plate_pos[2, 3] = engrave_plate_pos[2, 3] - self._APPROACH
            elif self.curve == 'edge':
                engrave_plate_pos[2, 3] = engrave_plate_pos[2, 3] - self._APPROACH - 2
            else:
                engrave_plate_pos[2, 3] = engrave_plate_pos[2, 3] - self._APPROACH - 2.5

            robot.setSpeed(150)
            robot.MoveL(engrave_plate_pos)
            tool_suction_ = self.RDK.Item('tool_suction', 4)
            tool_suction_.DetachAll()  # Detach all objects from the robot
            robot.MoveJ(robot.JointsHome())
            self.RDK.RunProgram('Prog8')

    def retrieve(self):
        """
        Retrieves the cover from the engraving plate and places it on the pallette
        """
        move_plate_tool = self.RDK.Item('engraving_plate', 4)
        move_plate_tool.DetachAll()
        engrave_plate_ref = self.RDK.Item('engraving_plate_ref', 3)
        robot = self.RDK.Item('fanuc', 3)
        robot.setPoseFrame(engrave_plate_ref)

        engrave_plate_pos_app = Pose(145, 0, 42.5, -180, 0, 90)
        robot.setSpeed(50)
        engraving_plate_pos = engrave_plate_pos_app

        if self.curve == 'none':
            engrave_plate_pos_app[2, 3] = engrave_plate_pos_app[2, 3] + self._APPROACH
        elif self.curve == 'edge':
            engrave_plate_pos_app[2, 3] = engrave_plate_pos_app[2, 3] + self._APPROACH
        else:
            engrave_plate_pos_app[2, 3] = engrave_plate_pos_app[2, 3] + self._APPROACH


        robot.MoveJ(engrave_plate_pos_app)

        engrave_plate_pos = engrave_plate_pos_app

        if self.curve == 'none':
            engrave_plate_pos[2, 3] = engrave_plate_pos[2, 3] - self._APPROACH
        elif self.curve == 'edge':
            engrave_plate_pos[2, 3] = engrave_plate_pos[2, 3] - self._APPROACH
        else:
            engrave_plate_pos[2, 3] = engrave_plate_pos[2, 3] - self._APPROACH

        robot.setSpeed(50)
        robot.MoveL(engrave_plate_pos)
        self.RDK.RunProgram('Prog6')
        self.RDK.RunProgram('Prog7')

        if self.curve == 'none':
            engrave_plate_pos_app[2, 3] = engrave_plate_pos_app[2, 3] + self._APPROACH
        elif self.curve == 'edge':
            engrave_plate_pos_app[2, 3] = engrave_plate_pos_app[2, 3] + self._APPROACH
        else:
            engrave_plate_pos_app[2, 3] = engrave_plate_pos_app[2, 3] + self._APPROACH

        robot.MoveJ(engrave_plate_pos_app)
        carrier_offsetx = 88.7  # (Carrier length / 2)
        carrier_offsety = 55.3  # (Carrier width / 2)
        carrier_offsetz = 42.3  # (Carrier depth)


        carrier_position_app = Pose(carrier_offsetx, carrier_offsety, carrier_offsetz, -180, 0, -90)
        carrier_ = self.RDK.Item('carrier', 3)
        robot.setPoseFrame(carrier_)

        if self.curve == 'none':
            carrier_position_app[2, 3] = carrier_position_app[2, 3] + self._APPROACH
        if self.curve == 'edge':
            carrier_position_app[2, 3] = carrier_position_app[2, 3] + self._APPROACH
        if self.curve == 'curved':
            carrier_position_app[2, 3] = carrier_position_app[2, 3] + self._APPROACH

        robot.MoveJ(carrier_position_app)
        position_withoffset = carrier_position_app

        # Check the type of cover again and subtract the approach offset,
        # while considering that a cover is attached to the tool
        if self.curve == 'none':
            position_withoffset[2, 3] = position_withoffset[2, 3] - self._APPROACH + self._OFFSETZ_COVER_FLAT_DIST
        if self.curve == 'edge':
            position_withoffset[2, 3] = position_withoffset[2, 3] - self._APPROACH + self._OFFSETZ_COVER_EDGE_DIST -1.5
        if self.curve == 'curved':
            position_withoffset[2, 3] = position_withoffset[
                                            2, 3] - self._APPROACH + self._OFFSETZ_COVER_CURVED_DIST

        # Take into account that it is now a whole phone
        position_withoffset[2, 3] = position_withoffset[
                                        2, 3] - self._TOP_COVER_INDENT_OFFSET + self._BOTTOM_COVER_HEIGHT

        robot.setSpeed(150)
        robot.MoveL(position_withoffset)
        robot.setSpeed(500)
        tool_suction_ = self.RDK.Item('tool_suction', 4)
        tool_suction_.DetachAll()  # Detach all objects from the robot
        robot.MoveJ(robot.JointsHome())
