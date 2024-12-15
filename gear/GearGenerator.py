from PointsGenerator import *

class GearGenerator(PointsGenerator):

    cx: float
    cy: float
    num_teeth: int
    module: float
    pressure_angle: float
    pitch_diameter: float
    base_circle_radius: float
    outer_circle_radius: float
    root_circle_radius: float
    tooth_angle: float
    base_tooth_angle: float


    def __init__(
        self,
        cx: float,
        cy: float,
        num_teeth: int,
        module: float,
        pressure_angle: float = 20
    ):
        super().__init__()
        self.cx: float = cx
        self.cy: float = cy
        self.num_teeth: int = num_teeth
        self.module: float = module
        self.pressure_angle: float = pressure_angle
        self.pitch_diameter: float = self.__calculate_pitch_diameter()
        self.base_circle_radius: float = self.__calculate_base_circle_radius()
        self.outer_circle_radius: float = self.__calculate_outer_circle_radius()
        self.root_circle_radius: float = self.__calculate_root_circle_radius()
        self.tooth_angle: float = self.__calculate_tooth_angle()
        self.base_tooth_angle: float = self.__calculate_base_tooth_angle()

    def __calculate_pitch_diameter(self) -> float:
        return self.num_teeth * self.module

    def __calculate_base_circle_radius(self) -> float:
        return (self.pitch_diameter / 2) * np.cos(np.radians(self.pressure_angle))

    def __calculate_outer_circle_radius(self) -> float:
        return self.pitch_diameter / 2 + self.module

    def __calculate_root_circle_radius(self) -> float:
        return (self.pitch_diameter / 2) - 1.25 * self.module

    def __calculate_tooth_angle(self) -> float:
        return np.pi / self.num_teeth

    def __calculate_base_tooth_angle(self) -> float:
        return 2 * np.arcsin(np.tan(self.tooth_angle / 2) * np.cos(np.radians(self.pressure_angle)))

    def __generate_involute_curve(self, start_angle: float, end_condition: Callable[[float, float], bool], sign: int = 1) -> Points:
        t_values = np.linspace(0, 10, 1000)  # Adjust the range and number of points as needed
        x = self.base_circle_radius * (np.cos(start_angle + t_values) + sign * t_values * np.sin(start_angle + t_values))
        y = self.base_circle_radius * (np.sin(start_angle + t_values) - sign * t_values * np.cos(start_angle + t_values))
        valid_indices = np.where(end_condition(x, y))[0]
        return [Vec2(x[i], y[i]) for i in valid_indices]

    def __generate_outer_circle_points(self, angle: float) -> Points:
        return [
            Vec2(self.outer_circle_radius * np.cos(angle + self.base_tooth_angle / 2),
                 self.outer_circle_radius * np.sin(angle + self.base_tooth_angle / 2)),
            Vec2(self.outer_circle_radius * np.cos(angle + self.base_tooth_angle),
                 self.outer_circle_radius * np.sin(angle + self.base_tooth_angle))
        ]

    def __generate_root_circle_points(self, angle: float) -> Points:
        return [
            Vec2(self.root_circle_radius * np.cos(angle + self.base_tooth_angle + self.base_tooth_angle / 2),
                 self.root_circle_radius * np.sin(angle + self.base_tooth_angle + self.base_tooth_angle / 2)),
            Vec2(self.root_circle_radius * np.cos(angle + self.base_tooth_angle * 2),
                 self.root_circle_radius * np.sin(angle + self.base_tooth_angle * 2))
        ]

    def __translate_and_rotate_points(self, points: Points, angle: float) -> Points:
        return [Vec2(p.x + self.cx, p.y + self.cy).rotate(angle) for p in points]

    def __generate_tooth_points(self, angle: float) -> Points:
        points:Points = []
        # Add points for the involute curve
        points.extend(self.__generate_involute_curve(angle, lambda x, y: np.sqrt(x**2 + y**2) < self.outer_circle_radius))
        # Add points for the outer circle
        points.extend(self.__generate_outer_circle_points(angle))
        # Add points for the involute curve on the other side
        points.extend(self.__generate_involute_curve(angle + self.base_tooth_angle, lambda x, y: np.sqrt(x**2 + y**2) > self.root_circle_radius, sign=-1))
        # Add points for the root circle
        points.extend(self.__generate_root_circle_points(angle))
        # Add points for the involute curve back to the base circle
        points.extend(self.__generate_involute_curve(angle + self.base_tooth_angle * 2, lambda x, y: np.sqrt(x**2 + y**2) > self.base_circle_radius))
        # Translate and rotate points
        points = self.__translate_and_rotate_points(points, angle)
        return points

    def generate(self) -> None:
        points:Points = []
        for i in range(self.num_teeth):
            angle = i * 2 * np.pi / self.num_teeth
            points.extend(self.__generate_tooth_points(angle))
        self._msp.add_polyline2d(points)
