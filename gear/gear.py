from GearGenerator import *
from CircleGenerator import *
from utils.plot import *

# def generate_gear():
#     generator = GearGenerator(0, 0, 20, 5)
#     generator.generate()
#     generator.save('autogen/gear.dxf')
#     print("Generated gear done")


def generate_circle():
    generator = CircleGenerator(0, 0, 0.1)
    doc = ezdxf.new("R2000")
    msp = doc.modelspace()

    points:Points = generator.points()
    points = np.vstack(([0,0], points))

    plot_points(points)
    msp.add_lwpolyline(points)

    doc.saveas("autogen/circle.dxf")

if __name__ == '__main__':
    # generate_gear()
    generate_circle()