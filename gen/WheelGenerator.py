import sys
import os
# 获取当前脚本所在目录的上一级目录
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
# 将上一级目录添加到 sys.path
sys.path.insert(0, parent_dir)

from gen.PointsGenerator import *

class WheelGenerator(PointsGenerator):
    _radius:float
    _wave:float
    _num_teeth: int
    
    def __init__(
        self,
        radius: float,
        wave:float,
        teeth_num:int,
        num_segments:int,
        cx: float = 0,
        cy: float = 0

    ):
        super().__init__(num_segments, cx, cy)
        self._radius: float = radius
        self._wave: float = wave
        self._num_teeth: int = teeth_num

    def __generate_circle_points(
        self, 
    ) -> Points:
        angles:np.float32 = np.linspace(0, 2 * np.pi, self._num_segments, dtype = np.float32)
        # r:np.float32 = self._radius + (np.sin(angles * self._num_teeth)- 1) * self._wave
        # r:np.float32 = self._radius + np.min(np.sin(angles * self._num_teeth), 0) * self._wave
        # x:np.float32 = self._cx + r * np.cos(angles)
        # y:np.float32 = self._cy + r * np.sin(angles)
        sin_values: np.float32 = np.sin(angles * self._num_teeth)
        # 将 sin_values 中大于 0 的部分截断为 0
        truncated_sin_values: np.float32 = np.where(sin_values > 0, 0, sin_values)
        r: np.float32 = self._radius + truncated_sin_values * self._wave
        x: np.float32 = self._cx + r * np.cos(angles)
        y: np.float32 = self._cy + r * np.sin(angles)
        return np.column_stack((x, y))
    def points(self) -> Points:
        return self.__generate_circle_points()