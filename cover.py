# The following file contains code made by ROB2 - B223
# 2. Semester AAU 2021.
# The following file has no copyright and can be used freely
# Credit is expected when used commercially

# Imports for class
from robolink.robolink import Robolink, ITEM_TYPE_ROBOT# Import robolink library object
from stock import Stock  # Import class Stock from stock
from config import CaseConfig


class Cover:
    # Global class variables
    _OFFSETX_COVER_DIST = 70  # Offset in x-direction in mm
    _OFFSETY_COVER_DIST = 73  # Offset in y-direction in mm
    _OFFSETZ_COVER_DIST = 11.7  # Offset in z-direction in mm (Cover depth)
    _COVER_CAPACITY = 10  # Cover capacity for calculations
    _APPROACH = 100 # Approach to objects in mm
    _ROBOT_HOME = [0, 0, 0, 90, 0, 0,]
    RDK = Robolink() # Establish contact to RoboDK

    # Constructor:
    # for class cover
    # Takes in a color, curve type and a stock class
    # Sets initial position, color, curve and stock
    # for the object to use when giving positions to

    def __init__(self, color, curve_type, stock: Stock):
        self.color = color  # Assigning the given color string to an object field of name color
        self.curve = curve_type  # Assigning the given curve string to an object field of name curve
        self.stock = stock  # Assigning the given stock object to an object field of name stock
        self.position = [73, self._OFFSETY_COVER_DIST, 130, 0, 0, 0]  # Initialize list with y-position of cover
        self.correct_pos(self.stock)

    #

    def correct_pos(self, stock: Stock):
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
        self.position[0] = self.position[0] + identifier*self._OFFSETX_COVER_DIST
        self.position[2] = self.position[2] - stock.get(f'{self.color}_{self.curve}')*self._OFFSETX_COVER_DIST

    def __str__(self):
        print('{color} {curve} cover at {position}')

    def get_pos(self):
        return self.position

    def grab(self, robot):
        robot.setPoseFrame('stock_container')
        position_cp = self.position
        position_cp[2] = 230
        robot.MoveJ(position_cp)
        robot.setSpeed(50)
        robot.MoveL(self.position)
        robot.AttachClosest(f'cover_{self.color}_{self.curve}')
        robot.MoveL(position_cp)

    def give_top(self):
        carrier_offsetx = 90
        carrier_offsety = 55
        carrier_offsetz = 41.5
        position_withoffset_app = [carrier_offsetx, carrier_offsety, carrier_offsetz+self._APPROACH, 0, 0, 0]

        robot = self.RDK.Item('Fanuc', ITEM_TYPE_ROBOT)
        self.grab(robot)
        if not robot.item.Valid():
            self.grab(robot)

        robot.setPoseFrame('carrier')
        robot.setSpeed(100)
        robot.MoveJ(position_withoffset_app)

        position_withoffset = position_withoffset_app
        position_withoffset[2] = position_withoffset[2] - self._APPROACH

        robot.MoveL(position_withoffset)
        cover = self.RDK.Item(f'cover_{self.color}_{self.curve}')
        cover.AttachClosest('bottom')
        engrave_check = CaseConfig.engrave()

        if engrave_check:
            engrave_plate_pos_app = [0, 0, 0+self._APPROACH, 0, 0, 0]
            robot.setPoseFrame('cart_robot')
            robot.MoveJ(engrave_plate_pos_app)
            engrave_plate_pos = engrave_plate_pos_app
            engrave_plate_pos[2] = engrave_plate_pos[2]-self._APPROACH
            robot.setSpeed(50)
            robot.MoveL(engrave_plate_pos)
            robot_home = robot.setJointsHome(self._ROBOT_HOME)
            robot.MoveJ(robot_home)


            # Move cover to engrave_base
            # Detach phone from robot and attach to engrave_base
            # Robot return home







