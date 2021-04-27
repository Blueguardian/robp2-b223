# The following file contains code written by ROB2 - B223
# 2. Semester AAU 2021.

# Imports for class
from robolink.robolink import Robolink, ITEM_TYPE_ROBOT

from config import CaseConfig
from statistics import Statistics
from stock import Stock


class Cover:
    # Global class variables
    # Distances in mm
    _OFFSETX_COVER_DIST = 70
    _OFFSETY_COVER_DIST = 73
    _OFFSETZ_COVER_FLAT_DIST = 11.7
    _OFFSETZ_COVER_EDGE_DIST = 14.7
    _OFFSETZ_COVER_CURVED_DIST = 16.7
    _BOTTOM_COVER_HEIGHT = 13
    _TOP_COVER_INDENT_OFFSET = 5
    _COVER_CAPACITY = Stock.get_init()
    _APPROACH_FLAT = 100
    _APPROACH_EDGE = _APPROACH_FLAT + 30
    _APPROACH_CURVE = _APPROACH_FLAT + 50
    _ROBOT_HOME = [0, 0, 0, 90, 0, 0, ]
    RDK = Robolink()

    def __init__(self, color, curve_type, stock: Stock):
        """
        Constructor:
        Assigns the fields to the given parameters and corrects the position of the cover based on the parameters
        :param color: The color given in the config file
        :param curve_type: The curve type given in the config file
        :param stock: Stock Stock controlling object with type hint Stock
        """
        self.color = color
        self.curve = curve_type
        self.stock = stock
        self.stat = Statistics()
        self.position = [73, self._OFFSETY_COVER_DIST, 175, 0, 0, 0]
        self.correct_pos(self.stock)

    # Define dictionary with the different types and give them an identifier
    def correct_pos(self, stock: Stock):
        """
        Corrects the position of the cover relative to the stock container, depending on the type of cover.
        Instead of giving each cover a static position
        :param stock: Stock controlling object with type hint Stock
        :return: The position of the specific cover
        """

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

        identifier = case_types[f'{self.color}_{self.curve}']
        self.position[0] = self.position[0] + identifier * self._OFFSETX_COVER_DIST

        # Depending on the remaining stock and type of curve, calculate the Z-offset to compensate for the empty space
        if identifier in range(3):
            self.position[2] = self.position[2] - stock.get(
                f'{self.color}_{self.curve}') * self._OFFSETZ_COVER_FLAT_DIST
        if identifier in range(4, 6):
            self.position[2] = self.position[2] - stock.get(
                f'{self.color}_{self.curve}') * self._OFFSETZ_COVER_EDGE_DIST
        if identifier in range(6, 9):
            self.position[2] = self.position[2] - stock.get(
                f'{self.color}_{self.curve}') * self._OFFSETZ_COVER_CURVED_DIST

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
        robot.setPoseFrame('stock_container')
        robot.setPoseTool('suction')

        position_copy = self.position
        position_copy[2] = position_copy[2] + self._APPROACH_FLAT
        robot.MoveJ(position_copy)
        robot.setSpeed(50)
        robot.MoveL(self.position)
        robot.AttachClosest(f'cover_{self.color}_{self.curve}')
        robot.MoveL(position_copy)
        robot.setSpeed()
        self.stock.sub(f'{self.color}_{self.curve}', 1)

    def give_top(self):
        """
        Sends instructions to RoboDK to grab a cover, place it on top of the bottom cover
        if the cover needs to be engraved, places it on the engraving plate.
        """
        carrier_offsetx = 90  # (Carrier length / 2)
        carrier_offsety = 55  # (Carrier width / 2)
        carrier_offsetz = 41.5  # (Carrier depth)

        carrier_position_app = [carrier_offsetx, carrier_offsety, carrier_offsetz, 0, 0, 0]

        if self.curve == 'none':
            carrier_position_app[2] = carrier_position_app[2] + self._APPROACH_FLAT
        if self.curve == 'edge':
            carrier_position_app[2] = carrier_position_app[2] + self._APPROACH_EDGE
        if self.curve == 'curved':
            carrier_position_app[2] = carrier_position_app[2] + self._APPROACH_CURVE

        robot = self.RDK.Item('fanuc', ITEM_TYPE_ROBOT)
        self.grab(robot)
        if not robot.item.Valid():
            self.grab(robot)

        robot.setPoseFrame('carrier')
        robot.setPoseTool('suction')
        robot.MoveJ(carrier_position_app)

        position_withoffset = carrier_position_app

        # Check the type of cover again and subtract the approach offset,
        # while considering that a cover is attached to the tool
        if self.curve == 'none':
            position_withoffset[2] = position_withoffset[2] - self._APPROACH_FLAT + self._OFFSETZ_COVER_FLAT_DIST
        if self.curve == 'edge':
            position_withoffset[2] = position_withoffset[2] - self._APPROACH_EDGE + self._OFFSETZ_COVER_EDGE_DIST
        if self.curve == 'curved':
            position_withoffset[2] = position_withoffset[2] - self._APPROACH_CURVE + self._OFFSETZ_COVER_CURVED_DIST

        # Take into account that it is now a whole phone
        position_withoffset[2] = position_withoffset[2] - self._TOP_COVER_INDENT_OFFSET + self._BOTTOM_COVER_HEIGHT

        robot.setSpeed(50)
        robot.MoveL(position_withoffset)
        str_cover = f'{self.color}_{self.curve}'
        cover = self.RDK.Item(f'cover_{self.color}_{self.curve}_{self.stock.get(str_cover)}')
        cover.AttachClosest('bottom')
        robot.MoveL(carrier_position_app)
        robot.setSpeed()
        engrave_check = CaseConfig.engrave()

        if engrave_check:
            engrave_plate_pos_app = [0, 0, 0, 0, 0, 0]

            # Check for type of cover an apply an approach to the z value
            if self.curve == 'none':
                engrave_plate_pos_app[2] = engrave_plate_pos_app[2] + self._APPROACH_FLAT
            elif self.curve == 'edge':
                engrave_plate_pos_app[2] = engrave_plate_pos_app[2] + self._APPROACH_EDGE
            else:
                engrave_plate_pos_app[2] = engrave_plate_pos_app[2] + self._APPROACH_CURVE

            robot.setPoseFrame('cart_robot')
            robot.MoveJ(engrave_plate_pos_app)
            engrave_plate_pos = engrave_plate_pos_app

            # Check for cover type and subtract the approach while taking into account carrying a phone
            if self.curve == 'none':
                engrave_plate_pos[2] = engrave_plate_pos[2] + self._OFFSETZ_COVER_FLAT_DIST - self._APPROACH_FLAT
            elif self.curve == 'edge':
                engrave_plate_pos[2] = engrave_plate_pos[2] + self._OFFSETZ_COVER_EDGE_DIST - self._APPROACH_EDGE
            else:
                engrave_plate_pos[2] = engrave_plate_pos[2] + self._OFFSETZ_COVER_CURVED_DIST - self._APPROACH_CURVE
            engrave_plate_pos[2] = engrave_plate_pos[2] + self._BOTTOM_COVER_HEIGHT - self._TOP_COVER_INDENT_OFFSET

            robot.setSpeed(50)
            robot.MoveL(engrave_plate_pos)
            robot.DetachAll()  # Detach all objects from the robot
            cart_robot = self.RDK.Item('cart_robot')
            cart_robot.AttachClosest(f'cover_{self.color}_{self.curve}')
            robot_home = robot.setJointsHome(self._ROBOT_HOME)
            robot.MoveJ(robot_home)

    def retrieve(self):
        """
        Retrieves the cover from the engraving plate and places it on the pallette
        """
        _OFFSET_PLATE = 50
        _CURVED_PHONE_HEIGHT = self._OFFSETZ_COVER_CURVED_DIST + self._BOTTOM_COVER_HEIGHT - self._TOP_COVER_INDENT_OFFSET
        _EDGE_PHONE_HEIGHT = self._OFFSETZ_COVER_EDGE_DIST + self._BOTTOM_COVER_HEIGHT - self._TOP_COVER_INDENT_OFFSET
        _FLAT_PHONE_HEIGHT = self._OFFSETZ_COVER_FLAT_DIST + self._BOTTOM_COVER_HEIGHT - self._TOP_COVER_INDENT_OFFSET

        carrier_offsetx = 90  # (Carrier length / 2)
        carrier_offsety = 55  # (Carrier width / 2)
        carrier_offsetz = 41.5  # (Carrier depth)

        carrier_position_app = [carrier_offsetx, carrier_offsety, carrier_offsetz + self._APPROACH_FLAT, 0, 0, 0]

        robot = self.RDK.Item('fanuc')
        robot.setPoseFrame('engraving_plate')
        engraving_plate_app = [0, 0, self._APPROACH_FLAT, 0, 0, 0]
        robot.MoveJ(engraving_plate_app)
        robot.setSpeed(50)
        engraving_plate_pos = engraving_plate_app
        if self.curve == 'none':
            engraving_plate_pos[2] = engraving_plate_pos[2] - self._APPROACH_FLAT + _FLAT_PHONE_HEIGHT
        if self.curve == 'edge':
            engraving_plate_pos[2] = engraving_plate_pos[2] - self._APPROACH_FLAT + _EDGE_PHONE_HEIGHT
        if self.curve == 'curved':
            engraving_plate_pos[2] = engraving_plate_pos[2] - self._APPROACH_FLAT + _CURVED_PHONE_HEIGHT
        robot.MoveL(engraving_plate_pos)
        engraving_plate = self.RDK.Item('cart_robot')
        engraving_plate.DetachAll()
        robot.AttachClosest(f'cover_{self.color}_{self.curve}')
        robot.MoveL(engraving_plate_app)
        robot.setSpeed()
        robot.setPoseFrame('carrier')
        robot.MoveJ(carrier_position_app)
        carrier_position = carrier_position_app
        if self.curve == 'none':
            carrier_position[2] = carrier_position[2] - self._APPROACH_FLAT + _FLAT_PHONE_HEIGHT
        if self.curve == 'edge':
            carrier_position[2] = carrier_position[2] - self._APPROACH_FLAT + _EDGE_PHONE_HEIGHT
        if self.curve == 'curved':
            carrier_position[2] = carrier_position[2] - self._APPROACH_FLAT + _CURVED_PHONE_HEIGHT

        robot.setSpeed(50)
        robot.MoveL(carrier_position)
        robot.DetachAll()
        robot.MoveL(carrier_position_app)
        robot.JointsHome()
        self.stat.add(f'{self.color}_{self.curve}', 1)

