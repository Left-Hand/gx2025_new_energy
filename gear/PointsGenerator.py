import sys
import os

# 获取当前脚本所在目录的上一级目录
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
# 将上一级目录添加到 sys.path
sys.path.insert(0, parent_dir)


from utils.common import *
# from ..utils.plot import plot_points

def save_dxf(doc: Drawing, filename: str) -> None:
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        doc.saveas(filename)
    except FileNotFoundError as e:
        print(f"File path error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


class PointsGenerator(ABC):
    # _doc: Drawing
    # _msp: Modelspace 

    def __init__(self):
        # self._doc: Drawing = ezdxf.new('R2010')
        # self._msp: Modelspace = self._doc.modelspace()
        pass
        
    # @abstractmethod
    # def generate(self) -> None:
    #     pass

    @abstractmethod
    def points(self) -> Points:
        pass
    # def _add_polyline(self, points:Points):
    #     # self._msp.add_lwpolyline(numpy_to_vec2_list(points))
    #     self._msp.add_lwpolyline(points)
    
    # def save(self, filename: str) -> None:
    #     save_dxf(self._doc, filename)
