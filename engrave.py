import robodk.robodk
import robolink.robolink

import os
import re
import sys

COVER_CAPACITY = 10

# Function definitions
def get_cover(color, curve, robot_type, container, carrier_cp, bottom, stock):
    _APPROACH = 100  # Distance to object
    _COVER_DEPTH = 13 # Cover depth in mm

    # positions above container relative to container reference frame
    black_flat = [0, 0, 0, 0, 0, 0]
    black_curve_edge = [0, 0, 0, 0, 0, 0]
    black_curved = [0, 0, 0, 0, 0, 0]
    blue_flat = [0, 0, 0, 0, 0, 0]
    blue_curve_edge = [0, 0, 0, 0, 0, 0]
    blue_curved = [0, 0, 0, 0, 0, 0]
    white_flat = [0, 0, 0, 0, 0, 0]
    white_curve_edge = [0, 0, 0, 0, 0, 0]
    white_curved = [0, 0, 0, 0, 0, 0]
    carrier_app = [0, 0, 0, 0, 0, 0]

    # Check color and curve style

    if color == 'black' and curve == 'none':
        robot_type.setPoseFrame(container)
        robot_type.MoveJ(black_flat)
        cover_app = black_flat
        cover_app[2] = cover_app[2] - _APPROACH - _COVER_DEPTH*(COVER_CAPACITY-stock.get('black_flat'))
        robot_type.setSpeed(50)
        robot_type.MoveL(cover_app)
        robot_type.AttachClosest()
        if not robot_type.item.Valid():
            raise KeyError("Object not attached")
        robot_type.MoveL(black_flat)
        robot_type.setSpeed(100)
        robot_type.setPoseFrame(carrier_cp)
        robot_type.MoveJ(carrier_app)
        carrier_cp = carrier_app
        carrier_cp[2] = carrier_cp[2] - _APPROACH
        robot_type.setSpeed(50)
        robot_type.MoveL(carrier_cp)
        bottom.AttachClosest(container)

    elif color == 'black' and curve == 'edge':
        robot_type.setPoseFrame(container)
        robot_type.MoveJ(black_curve_edge)
        cover_app = black_curve_edge
        cover_app[2] = cover_app[2] - _APPROACH - _COVER_DEPTH*(COVER_CAPACITY-stock.get('black_edge'))
        robot_type.setSpeed(50)
        robot_type.MoveL(cover_app)
        robot_type.AttachClosest()
        if not robot_type.item.Valid():
            raise KeyError("Object not attached")
        robot_type.MoveL(black_curve_edge)
        robot_type.setSpeed(100)
        robot_type.setPoseFrame(carrier_cp)
        robot_type.MoveJ(carrier_app)
        carrier_cp = carrier_app
        carrier_cp[2] = carrier_cp[2] - _APPROACH
        robot_type.setSpeed(50)
        robot_type.MoveL(carrier_cp)
        bottom.AttachClosest(container)

    elif color == 'black' and curve == 'curved':
        robot_type.setPoseFrame(container)
        robot_type.MoveJ(black_curved)
        cover_app = black_curved
        cover_app[2] = cover_app[2] - _APPROACH - _COVER_DEPTH*(COVER_CAPACITY-stock.get('black_curved'))
        robot_type.setSpeed(50)
        robot_type.MoveL(cover_app)
        robot_type.AttachClosest()
        if not robot_type.item.Valid():
            raise KeyError("Object not attached")
        robot_type.MoveL(black_curved)
        robot_type.setSpeed(100)
        robot_type.setPoseFrame(carrier_cp)
        robot_type.MoveJ(carrier_app)
        carrier_cp = carrier_app
        carrier_cp[2] = carrier_cp[2] - _APPROACH
        robot_type.setSpeed(50)
        robot_type.MoveL(carrier_cp)
        bottom.AttachClosest(container)

    elif color == 'white' and curve == 'none':
        robot_type.setPoseFrame(container)
        robot_type.MoveJ(white_flat)
        cover_app = white_flat
        cover_app[2] = cover_app[2] - _APPROACH
        robot_type.setSpeed(50)
        robot_type.MoveL(cover_app)
        robot_type.AttachClosest()
        if not robot_type.item.Valid():
            raise KeyError("Object not attached")
        robot_type.MoveL(white_flat)
        robot_type.setSpeed(100)
        robot_type.setPoseFrame(carrier)
        robot_type.MoveJ(carrier_app)
        carrier_cp = carrier_app
        carrier[2] = carrier[2] - _APPROACH
        robot_type.setSpeed(50)
        robot_type.MoveL(carrier)
        bottom.AttachClosest(container)

    elif color == 'white' and curve == 'edge':
        robot_type.setPoseFrame(container)
        robot_type.MoveJ(white_curve_edge)
        cover_app = white_curve_edge
        cover_app[2] = cover_app[2] - _APPROACH
        robot_type.MoveL(cover_app)

    elif color == 'white' and curve == 'curved':
        robot_type.setPoseFrame(container)
        robot_type.MoveJ(white_curved)
        cover_app = white_curved
        cover_app[2] = cover_app[2] - _APPROACH
        robot_type.MoveL(cover_app)

    elif color == 'blue' and curve == 'none':
        robot_type.setPoseFrame(container)
        robot_type.MoveJ(blue_flat)
        cover_app = blue_flat
        cover_app[2] = cover_app[2] - _APPROACH
        robot_type.MoveL(cover_app)

    elif color == 'blue' and curve == 'edge':
        robot_type.setPoseFrame(container)
        robot_type.MoveJ(blue_curve_edge)
        cover_app = blue_curve_edge
        cover_app[2] = cover_app[2] - _APPROACH
        robot_type.MoveL(cover_app)

    elif color == 'blue' and curve == 'curved':
        robot_type.setPoseFrame(container)
        robot_type.MoveJ(blue_curved)
        cover_app = blue_curved
        cover_app[2] = cover_app[2] - _APPROACH
        robot_type.MoveL(cover_app)

# --------------Start program-------------------
from config import CaseConfig

colour = CaseConfig.colour()
curve_type = CaseConfig.curve_style()

RDK = robolink.robolink.Robolink()

robot = RDK.ItemUserPick('', robolink.robolink.ITEM_TYPE_ROBOT)
tool = RDK.Item('tool')
carrier = RDK.Item('carrier')
container = RDK.Item('container')
bottom = RDK.Item('bottom')

from stock import Stock

stock = Stock()

get_cover(colour, curve_type, robot, container, carrier, bottom, stock)


