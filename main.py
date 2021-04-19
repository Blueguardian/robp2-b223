import robodk.robodk
import robolink.robolink

PIXELS_AS_OBJECTS = True  # Set to True to generate PDF or HTML simulations that include the drawn path
TCP_KEEP_TANGENCY = True  # Set to True to keep the tangency along the path
SIZE_BOARD = [1000, 2000]  # Size of the image. The image will be scaled keeping its aspect ratio
MM_X_PIXEL = 2  # in mm. The path will be cut depending on the pixel size. If this value is changed it is recommended to scale the pixel object

RDK = robolink.robolink.Robolink()
# IMAGE_FILE = 'World map.svg'             # Path of the SVG image, it can be relative to the current RDK station

# --------------------------------------------------------------------------------
# function definitions:

def point2D_2_pose(cls, point, tangent):
    """Converts a 2D point to a 3D pose in the XY plane including rotation being tangent to the path"""
    return robodk.robodk.transl(point.x, point.y, 0) * robodk.robodk.rotz(tangent.angle())


def svg_draw_robot(svg_img, board, pix_ref, item_frame, item_tool, robot):
    """Draws the image with the robot. It is slower that svg_draw_quick but it makes sure that the image can be drawn with the robot."""

    APPROACH = 100  # approach distance in MM for each path
    home_joints = robot.JointsHome().tolist()  # [0,0,0,0,90,0] # home joints, in deg
    if abs(home_joints[4]) < 5:
        home_joints[4] = 90.0

    robot.setPoseFrame(item_frame)
    robot.setPoseTool(item_tool)
    robot.MoveJ(home_joints)

    # get the target orientation depending on the tool orientation at home position
    orient_frame2tool = robodk.robodk.invH(item_frame.Pose()) * robot.SolveFK(home_joints) * item_tool.Pose()
    orient_frame2tool[0:3, 3] = robodk.robodk.Mat([0, 0, 0])

    for path in svg_img:
        # use the pixel reference to set the path color, set pixel width and copy as a reference
        print('Drawing %s, RGB color = [%.3f,%.3f,%.3f]' % (
            path.idname, path.fill_color[0], path.fill_color[1], path.fill_color[2]))
        pix_ref.Recolor(path.fill_color)
        if PIXELS_AS_OBJECTS:
            pix_ref.Copy()
        np = path.nPoints()

        # robot movement: approach to the first target
        p_0 = path.getPoint(0)
        target0 = robodk.robodk.transl(p_0.x, p_0.y, 0) * orient_frame2tool
        target0_app = target0 * robodk.robodk.transl(0, 0, -APPROACH)
        robot.MoveL(target0_app)

        # if TCP_KEEP_TANGENCY:
        #    joints_now = robot.Joints().tolist()
        #    joints_now[5] = -180
        #    robot.MoveJ(joints_now)
        RDK.RunMessage('Drawing %s' % path.idname)
        RDK.RunProgram('SetColorRGB(%.3f,%.3f,%.3f)' % (path.fill_color[0], path.fill_color[1], path.fill_color[2]))
        for i in range(np):
            p_i = path.getPoint(i)
            v_i = path.getVector(i)

            pt_pose = point2D_2_pose(p_i, v_i)

            if TCP_KEEP_TANGENCY:
                # moving the tool along the path (axis 6 may reach its limits)
                target = pt_pose * orient_frame2tool
            else:
                # keep the tool orientation constant
                target = robodk.robodk.transl(p_i.x, p_i.y, 0) * orient_frame2tool

            # Move the robot to the next target
            robot.MoveL(target)

            # create a new pixel object with the calculated pixel pose
            if PIXELS_AS_OBJECTS:
                board.Paste().setPose(pt_pose)
            else:
                board.AddGeometry(pix_ref, pt_pose)

        target_app = target * robodk.robodk.transl(0, 0, -APPROACH)
        robot.MoveL(target_app)

    robot.MoveL(home_joints)


def get_cover(color, curve, robot_type, cover, carrier_cp, bottom):
    _APPROACH = 100 #Distance to object

    # Positions above covers in container
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

#Check color and curve style

    if color == 'black' and curve_style == 'none':
        robot_type.setPoseFrame(cover)
        robot_type.MoveJ(black_flat)
        cover_app = black_flat
        cover_app[2] = cover_app[2] - _APPROACH
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
        bottom.AttachClosest(cover)


    elif color == 'black' and curve_style == 'sides':
        robot_type.setPoseFrame(cover)
        robot_type.MoveJ(black_curve_edge)
        cover_app = black_curve_edge
        cover_app[2] = cover_app[2] - _APPROACH
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
        bottom.AttachClosest(cover)

    elif color == 'black' and curve_style == 'curved':
        robot_type.setPoseFrame(cover)
        robot_type.MoveJ(black_curved)
        cover_app = black_curved
        cover_app[2] = cover_app[2] - _APPROACH
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
        bottom.AttachClosest(cover)

    elif color == 'white' and curve_style == 'none':
        robot_type.setPoseFrame(cover)
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
        bottom.AttachClosest(cover)

    elif color == 'white' and curve_style == 'sides':
        robot_type.setPoseFrame(cover)
        robot_type.MoveJ(white_curve_edge)
        cover_app = white_curve_edge
        cover_app[2] = cover_app[2] - _APPROACH
        robot_type.MoveL(cover_app)

    elif color == 'white' and curve_style == 'curved':
        robot_type.setPoseFrame(cover)
        robot_type.MoveJ(white_curved)
        cover_app = white_curved
        cover_app[2] = cover_app[2] - _APPROACH
        robot_type.MoveL(cover_app)

    elif color == 'blue' and curve_style == 'none':
        robot_type.setPoseFrame(cover)
        robot_type.MoveJ(blue_flat)
        cover_app = blue_flat
        cover_app[2] = cover_app[2] - _APPROACH
        robot_type.MoveL(cover_app)

    elif color == 'blue' and curve_style == 'sides':
        robot_type.setPoseFrame(cover)
        robot_type.MoveJ(blue_curve_edge)
        cover_app = blue_curve_edge
        cover_app[2] = cover_app[2] - _APPROACH
        robot_type.MoveL(cover_app)

    elif color == 'blue' and curve_style == 'curved':
        robot_type.setPoseFrame(cover)
        robot_type.MoveJ(blue_curved)
        cover_app = blue_curved
        cover_app[2] = cover_app[2] - _APPROACH
        robot_type.MoveL(cover_app)

# --------------------------------------------------------------------------------
from config import CaseConfig

colour = CaseConfig.colour()
curve_style = CaseConfig.curve_style()
file_path = CaseConfig.file()

# Program start

# locate and import the svgpy module
# Old versions of RoboDK required adding required paths to the process path
# New versions of RoboDK automatically add the current folder to the path (after 4.2.2)
# path_stationfile = RDK.getParam('PATH_OPENSTATION')
# sys.path.append(os.path.abspath(path_stationfile)) # temporary add path to import station modules
# print(os.getcwd())
# print(os.environ['PYTHONPATH'].split(os.pathsep))
# print(os.environ['PATH'].split(os.pathsep))


from svgpy.svg import *

# select the file to draw
svgfile = file_path
if len(svgfile) == 0:
    svgfile = svgpy.svg.getOpenFile()

# import the SVG file
svgdata = svgpy.svg.svg_load(svgfile)

IMAGE_SIZE = svgpy.Point(108, 52)  # size of the image in MM
svgdata.calc_polygon_fit(IMAGE_SIZE, MM_X_PIXEL)
size_img = svgdata.size_poly()  # returns the size of the current polygon

# get the robot, frame and tool objects
robot = RDK.ItemUserPick('FANUC ', robolink.robolink.ITEM_TYPE_ROBOT)
framedraw = RDK.Item('Frame draw')
tool = RDK.Item('Tool')

# get the pixel reference to draw
pixel_ref = RDK.Item('pixel')

# delete previous image if any
# image = RDK.Item('Board & image')
# if image.Valid() and image.Type() == robolink.robolink.ITEM_TYPE_OBJECT: image.Delete()

# make a drawing board base on the object reference "Blackboard 250mm"
carrier = RDK.Item('carrier')
cover = RDK.Item('cover')
bottom = RDK.Item('bottom')


board_draw = framedraw.Paste()
board_draw.setVisible(True, False)
board_draw.setName('Board & image')
board_draw.Scale([size_img.x / 250, size_img.y / 250, 1])  # adjust the board size to the image size (scale)

pixel_ref.Copy()

# quickly show the final result without checking the robot movements:
# svg_draw_quick(svgdata, board_draw, pixel_ref)

get_cover(colour, curve_style, robot, cover, carrier, bottom)

# draw the image with the robot:
svg_draw_robot(svgdata, board_draw, pixel_ref, framedraw, tool, robot)
