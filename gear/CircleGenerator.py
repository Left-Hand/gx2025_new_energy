from PointsGenerator import *


class CircleGenerator(PointsGenerator):
    _radius:float

    def __init__(
        self,
        radius: float,
        num_segments:int,
        cx: float = 0,
        cy: float = 0

    ):
        super().__init__(num_segments, cx, cy)
        self._radius: float = radius

    def __generate_circle_points(
        self, 
    ) -> Points:
        angles = np.linspace(0, 2 * np.pi, self._num_segments, dtype = np.float32)
        x:np.float32 = self._cx + self._radius * np.cos(angles)
        y:np.float32 = self._cy + self._radius * np.sin(angles)
        return np.column_stack((x, y))
    def points(self) -> Points:
        return self.__generate_circle_points()