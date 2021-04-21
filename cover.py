# The following file contains code made by ROB2 - B223
# 2. Semester AAU 2021.

# Imports for class
from robolink.robolink import Robolink, ITEM_TYPE_ROBOT# Import robolink library object
from stock import Stock  # Import class Stock from stock
from config import CaseConfig


class Cover:
    # Global class variables
    _OFFSETX_COVER_DIST = 70  # Offset in x-direction in mm (container offset between holes)
    _OFFSETY_COVER_DIST = 73  # Offset in y-direction in mm (container width / 2)
    _OFFSETZ_COVER_FLAT_DIST = 11.7  # Offset in z-direction in mm (Base cover depth)
    _OFFSETZ_COVER_EDGE_DIST = 14.7
    _OFFSETZ_COVER_CURVE_DIST = 16.7
    _BOTTOM_COVER_HEIGHT = 13
    _TOP_COVER_INDENT_OFFSET = 5
    _COVER_CAPACITY = 10  # Cover capacity for calculations
    _APPROACH_FLAT = 100 # Approach to objects in mm
    _APPROACH_EDGE = _APPROACH_FLAT + 3*10
    _APPROACH_CURVE = _APPROACH_FLAT + 5*10
    _ROBOT_HOME = [0, 0, 0, 90, 0, 0,]  # Robot home position (Joint)
    RDK = Robolink() # Establish contact to RoboDK

    # Constructor definition:
    # Always called __init__.
    # Takes in a color, curve type and a stock class
    # Sets initial position, color, curve and stock
    # for the object to use when giving positions to
    # the robot

    def __init__(self, color, curve_type, stock: Stock):
        self.color = color  # Assigning the given color string to an object field of name color
        self.curve = curve_type  # Assigning the given curve string to an object field of name curve
        self.stock = stock  # Assigning the given stock object to an object field of name stock
        self.position = [73, self._OFFSETY_COVER_DIST, 130, 0, 0, 0]  # Initialize list with y-position of cover
        self.correct_pos(self.stock)  # Correct the position of the top cover according to color, curve style and stock

    # Method definition:
    # correct_pos.
    # correction of position with the parameter self and stock with assumed type Stock
    # Applies correction of the position of the cover in relation to given data and stock
    # This is instead of having to give a static position to every type of cover.

    def correct_pos(self, stock: Stock):  # Define dictionary with the different types and give them an identifier
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
        # Initialize the identifier with the current type of cover
        identifier = case_types[f'{self.color}_{self.curve}']
        # Apply the offset for the type of cover
        self.position[0] = self.position[0] + identifier*self._OFFSETX_COVER_DIST
        # Depending on the remaining stock and type of curve, calculate the Z-offset to compensate for the empty space
        if identifier in range(3):
            self.position[2] = self.position[2] - stock.get(f'{self.color}_{self.curve}')*self._OFFSETZ_COVER_FLAT_DIST
        if identifier in range(4, 6):
            self.position[2] = self.position[2] - stock.get(f'{self.color}_{self.curve}')*self._OFFSETZ_COVER_EDGE_DIST
        if identifier in range(6, 9):
            self.position[2] = self.position[2] - stock.get(f'{self.color}_{self.curve}')*self._OFFSETZ_COVER_CURVE_DIST

    # Method definition:
    # Always called __str__.
    # for object string representation.
    # Prints relevant information from the object

    def __str__(self):
        print(f'{self.color} curve_{self.curve} cover at {self.position}')

    # Method definition:
    # get_pos.
    # Not needed method for returning the original position of the cover

    def get_pos(self):
        return self.position  # Return variable position of cover

    # Method definition:
    # grab.
    # Grabs the cover from the stock_container object and moves out of the
    # container. Takes in the an robot object for the operations

    def grab(self, robot):
        robot.setPoseFrame('stock_container')  # Sets the reference frame to the stock_container
        position_cp = self.position  # Takes a copy of the position
        position_cp[2] = 275  # Sets a new Z value for the position.
        robot.MoveJ(position_cp)  # Moves the robot to the new position.
        robot.setSpeed(50)  # Lower the speed to ensure operation safety and reduce accidental damage to cover
        robot.MoveL(self.position)  # Moves the robot linearly down to the cover
        robot.AttachClosest(f'cover_{self.color}_{self.curve}')  # Attaches the nearest cover
        robot.MoveL(position_cp)  # Slowly move take the cover linearly out of the container

    # Method definition:
    # give_top.
    # The process of retrieving the correct cover from the container, and connecting
    # it to the bottom cover, and if it needs engraving moves it to the engraving station plate.

    def give_top(self):
        carrier_offsetx = 90  # Carrier offset x (Carrier length / 2)
        carrier_offsety = 55  # Carrier offset y (Carrier width / 2)
        carrier_offsetz = 41.5 # Carrier offset z (Carrier depth)
        position_withoffset_app = [carrier_offsetx, carrier_offsety, carrier_offsetz, 0, 0, 0]  # Set initial position of the bottom cover on the pallet

        # Check the type of the cover and apply the approach offset
        if self.curve == 'none':
            position_withoffset_app[2] = position_withoffset_app[2]+self._APPROACH_FLAT
        if self.curve == 'edge':
            position_withoffset_app[2] = position_withoffset_app[2]+self._APPROACH_EDGE
        if self.curve == 'curved':
            position_withoffset_app[2] = position_withoffset_app[2]+self._APPROACH_CURVE

        robot = self.RDK.Item('fanuc', ITEM_TYPE_ROBOT)  # Establish contact with the robot
        self.grab(robot)  # Call the grab method to collect the cover
        if not robot.item.Valid():  # Checks if the cover is attached else call grab() again
            self.grab(robot)

        robot.setPoseFrame('carrier')  # Set the reference frame to that of the carrier
        robot.setSpeed(100)  # Set to normal speed
        robot.MoveJ(position_withoffset_app)  # Move the robot near the carrier

        position_withoffset = position_withoffset_app  # Copy the contents of the position into a new variable

        # Check the type of cover again and subtract the approach offset while considering that a cover is attached to the tool
        if self.curve == 'none':
            position_withoffset[2] = position_withoffset[2] - self._APPROACH_FLAT + self._OFFSETZ_COVER_FLAT_DIST
        if self.curve == 'edge':
            position_withoffset[2] = position_withoffset[2] - self._APPROACH_EDGE + self._OFFSETZ_COVER_EDGE_DIST
        if self.curve == 'curved':
            position_withoffset[2] = position_withoffset[2] - self._APPROACH_CURVE + self._OFFSETZ_COVER_CURVE_DIST
        position_withoffset[2] = position_withoffset[2] - self._TOP_COVER_INDENT_OFFSET + self._BOTTOM_COVER_HEIGHT  # Take into account that it is now a whole phone

        robot.setSpeed(50)  # Lower speed for precision
        robot.MoveL(position_withoffset)  # Move the robot down and press the top-cover onto the bottom cover
        str_cover = f'{self.color}_{self.curve}'  # Setup string for following statement
        cover = self.RDK.Item(f'cover_{self.color}_{self.curve}_{self.stock.get(str_cover)}')  # Create a cover object
        cover.AttachClosest('bottom')  # Attach the bottom cover to the top cover
        engrave_check = CaseConfig.engrave()  # Check whether the cover needs to be engraved

        if engrave_check:  # If the cover needs to be engraved do the following
            engrave_plate_pos_app = [0, 0, 0, 0, 0, 0]  # Set an initial position of the engraving plate

            # Check for type of cover an apply an approach to the z value
            if self.curve == 'none':
                engrave_plate_pos_app[2] = engrave_plate_pos_app[2] + self._APPROACH_FLAT
            elif self.curve == 'edge':
                engrave_plate_pos_app[2] = engrave_plate_pos_app[2] + self._APPROACH_EDGE
            else:
                engrave_plate_pos_app[2] = engrave_plate_pos_app[2] + self._APPROACH_CURVE

            robot.setPoseFrame('cart_robot')  # Change the reference frame to that of the cartesian engraving mechanism
            robot.MoveJ(engrave_plate_pos_app)  # Move the cover near the engraving plate
            engrave_plate_pos = engrave_plate_pos_app  # Copy contents from the initial position

            # Check for cover type and subtract the approach while taking into account carrying a phone
            if self.curve == 'none':
                engrave_plate_pos[2] = engrave_plate_pos[2] + self._OFFSETZ_COVER_FLAT_DIST - self._APPROACH_FLAT
            elif self.curve == 'edge':
                engrave_plate_pos[2] = engrave_plate_pos[2] + self._OFFSETZ_COVER_EDGE_DIST - self._APPROACH_EDGE
            else:
                engrave_plate_pos[2] = engrave_plate_pos[2] + self._OFFSETZ_COVER_CURVE_DIST - self._APPROACH_CURVE
            engrave_plate_pos[2] = engrave_plate_pos[2] + self._BOTTOM_COVER_HEIGHT - self._TOP_COVER_INDENT_OFFSET  # Take into accout that it is now a whole phone

            robot.setSpeed(50)  # Lower speed for precision
            robot.MoveL(engrave_plate_pos)  # Slowly move the phone on the plate
            robot.DetachAll()  # Detach all objects from the robot
            cart_robot = self.RDK.Item('cart_robot')  # Create a new robot object
            cart_robot.AttachClosest(f'cover_{self.color}_{self.curve}')  # Attach the phone to the new robot
            robot_home = robot.setJointsHome(self._ROBOT_HOME)  # Set the home position of the manipulator
            robot.MoveJ(robot_home)  # Move the manipulator home
