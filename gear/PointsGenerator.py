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
    _cx:float
    _cy:float
    _num_segments:int
    def __init__(
        self,
        num_segments:int,
        cx: float = 0,
        cy: float = 0
    ):
        self._cx: float = cx
        self._cy: float = cy
        self._num_segments:int = num_segments
        

    @abstractmethod
    def points(self) -> Points:
        pass
