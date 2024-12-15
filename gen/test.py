from PointsGenerator import *

def create_simple_line() -> None:
    # create a new DXF R2010 document
    doc = ezdxf.new("R2010")

    # add new entities to the modelspace
    msp = doc.modelspace()
    # add a LINE entity
    msp.add_line((0, 0), (10, 0))
    # save the DXF document
    doc.saveas("autogen/line.dxf")

def convert_to_tuples(points) -> list[tuple[float, float]]:
    """
    将二维点云转换为 list[tuple[int, int]]
    
    :param points: 输入的二维点云，可以是 numpy 数组或列表
    :return: 转换后的 list[tuple[int, int]]
    """
    if isinstance(points, np.ndarray):
        points = points.tolist()
    
    # return [(round(x,4),round(y,4)) for x, y in points]
    return [(round(x,4),round(y,4)) for x, y in points]


def create_lwpolyline() -> None:
    doc = ezdxf.new("R2000")
    msp = doc.modelspace()
    np.set_printoptions(suppress=True, precision=4)
    # 半径为 10 的圆，生成 10 个点
    num_points = 100
    radius = 10
    angles = np.linspace(0, 2 * np.pi, num_points, endpoint=False)
    points = np.array([(radius * np.cos(angle), radius * np.sin(angle)) for angle in angles])
    points = np.vstack(([0,0], points))
    # _raw_points:list[tuple[float, float]] = convert_to_tuples(points.tolist())
    # org:list[tuple[float, float]] = [(0.0,0.0)]
    # _raw_points = org + _raw_points
    # _raw_points = [(10.0, 0.0), (3.0, 0.0), (6.00, 3.0), (6.0, 6.0)]
    # _raw_points = [(10.0, 0.0), (3.0, 0.0), (6.00, 3.0), (6.0, 6.0)]
    # _raw_points = [(0.0,0.0), (10.0, 0.0), (9.9803, 0.6279), (9.9211, 1.2533), (9.8229, 1.8738)]
    # plot_p
    print(points)
    # msp.add_lwpolyline(points)

    msp.add_lwpolyline(points)

    # 确保保存的目录存在
    os.makedirs("autogen", exist_ok=True)
    doc.saveas("autogen/lwpolyline1.dxf")


create_lwpolyline()