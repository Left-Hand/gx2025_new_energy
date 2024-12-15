from GearGenerator import *
from CircleGenerator import *
from WheelGenerator import *
from utils.plot import *



def generate_circle():
    
    doc = ezdxf.new("R2000")
    msp = doc.modelspace()

    # points:Points = CircleGenerator(0.1, 1000).points()
    # points:Points = GearGenerator(20, 5, 800).points()
    points:Points = WheelGenerator(0.075, 0.0003, 300, 6000).points()
    # points:Points = generator.points()
    points = np.vstack(([0,0], points))

    # print(points)
    plot_points(points)

    msp.add_lwpolyline(points)
    doc.saveas("autogen/circle.dxf")

if __name__ == '__main__':
    # generate_gear()
    generate_circle()