from PointsGenerator import *


class CircleGenerator(PointsGenerator):
    cx:float
    cy:float
    radius:float
    num_segments:int
    def __init__(
        self,
        cx: float,
        cy: float,
        radius: float,
        num_segments: int = 100
    ):
        super().__init__()
        self.cx: float = cx
        self.cy: float = cy
        self.radius: float = radius
        self.num_segments: int = num_segments

    def __generate_circle_points(
        self, 
    ) -> Points:
        
        angles = np.linspace(0, 2 * np.pi, self.num_segments, dtype = np.float32)
        x:np.float32 = self.cx + self.radius * np.cos(angles)
        y:np.float32 = self.cy + self.radius * np.sin(angles)
        return np.column_stack((x, y))
    def points(self) -> Points:
        return self.__generate_circle_points()