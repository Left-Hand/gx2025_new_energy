
from utils.plot import *


BIG_CIRCLE_RADIUS = 0.008
SMALL_CIRCLE_RADIUS = 0.0024
CIRCLE_DIST = 0.012
RECT_START_X = 0.02
RECT_END_X = 0.04
RECT_HEIGHT = 0.002
def generate_dxf_from_points(points:Points, filename:str):
    
    doc = ezdxf.new("R2000")
    msp = doc.modelspace()

    # points = np.vstack(([0,0], points))
    # points = np.vstack(([0,0], points))

    # plot_points(points)

    msp.add_lwpolyline(points)
    msp.add_circle((0,0), BIG_CIRCLE_RADIUS)
    msp.add_circle((CIRCLE_DIST,0), SMALL_CIRCLE_RADIUS)
    msp.add_circle((0,CIRCLE_DIST), SMALL_CIRCLE_RADIUS)
    msp.add_circle((-CIRCLE_DIST,0), SMALL_CIRCLE_RADIUS)
    msp.add_circle((0, -CIRCLE_DIST), SMALL_CIRCLE_RADIUS)
    msp.add_lwpolyline([(RECT_START_X, RECT_HEIGHT/2), (RECT_START_X, -RECT_HEIGHT/2), (RECT_END_X, -RECT_HEIGHT/2), (RECT_END_X, RECT_HEIGHT/2), (RECT_START_X, RECT_HEIGHT/2)])
    doc.saveas(filename)

# if __name__ == '__main__':
#     generate_from_points(
#         WheelGenerator(0.075, 0.0003, 300, 6000).points(),
#         "autogen/circle.dxf"
#     )
    