
from utils.plot import *

def generate_dxf_from_points(points:Points, filename:str):
    
    doc = ezdxf.new("R2000")
    msp = doc.modelspace()

    # points = np.vstack(([0,0], points))
    # points = np.vstack(([0,0], points))

    # plot_points(points)

    msp.add_lwpolyline(points)
    doc.saveas(filename)

# if __name__ == '__main__':
#     generate_from_points(
#         WheelGenerator(0.075, 0.0003, 300, 6000).points(),
#         "autogen/circle.dxf"
#     )
    