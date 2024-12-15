from PointsGenerator import *

class GearGenerator(PointsGenerator):
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
        num_teeth: int,
        module: float,
        num_segments: int = 100,
        pressure_angle: float = 20,
        cx: float = 0,
        cy: float = 0
    ):
        super().__init__(num_segments, cx, cy)
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

    # def __generate_involute_curve(self, start_angle: float, end_condition: Callable[[float, float], bool], sign: int = 1) -> Points:
    #     t_values = np.linspace(0, 10, int(self._num_segments / self.num_teeth))  # Adjust the range and number of points as needed
    #     x = self.base_circle_radius * (np.cos(start_angle + t_values) + sign * t_values * np.sin(start_angle + t_values))
    #     y = self.base_circle_radius * (np.sin(start_angle + t_values) - sign * t_values * np.cos(start_angle + t_values))
    #     valid_indices = np.where(end_condition(x, y))[0]
    #     return [np.float32((x[i], y[i])) for i in valid_indices]
    def __generate_involute_curve(self, start_angle: float, end_condition: Callable[[float, float], bool], sign: int = 1) -> Points:
        # Adjust the range of t_values based on the geometry of the involute curve
        t_max = 10  # This value might need adjustment based on the specific gear parameters
        t_values = np.linspace(0, t_max, int(self._num_segments / self.num_teeth))  # Adjust the range and number of points as needed
        
        x = self.base_circle_radius * (np.cos(start_angle + t_values) + sign * t_values * np.sin(start_angle + t_values))
        y = self.base_circle_radius * (np.sin(start_angle + t_values) - sign * t_values * np.cos(start_angle + t_values))
        
        valid_indices = np.where(end_condition(x, y))[0]
        return [np.float32((x[i], y[i])) for i in valid_indices]

    def __generate_outer_circle_points(self, angle: float) -> Points:
        return [
            np.float32((self.outer_circle_radius * np.cos(angle + self.base_tooth_angle / 2),
                 self.outer_circle_radius * np.sin(angle + self.base_tooth_angle / 2))),
            np.float32((self.outer_circle_radius * np.cos(angle + self.base_tooth_angle),
                 self.outer_circle_radius * np.sin(angle + self.base_tooth_angle)))
        ]

    def __generate_root_circle_points(self, angle: float) -> Points:
        return [
            np.float32((self.root_circle_radius * np.cos(angle + self.base_tooth_angle + self.base_tooth_angle / 2),
                 self.root_circle_radius * np.sin(angle + self.base_tooth_angle + self.base_tooth_angle / 2))),
            np.float32((self.root_circle_radius * np.cos(angle + self.base_tooth_angle * 2),
                 self.root_circle_radius * np.sin(angle + self.base_tooth_angle * 2)))
        ]

    def __translate_and_rotate_points(self, points: Points, angle: float) -> Points:
        return [((p[0] + self._cx, p[1] + self._cy).rotate(angle) for p in points)]

    def __generate_tooth_points(self, angle: float) -> Points:
        points:Points = []
        # points += (self.__generate_involute_curve(angle, lambda x, y: np.sqrt(x**2 + y**2) < self.outer_circle_radius, sign = -1))
        points += (self.__generate_involute_curve(angle, lambda x, y: np.sqrt(x**2 + y**2) < self.outer_circle_radius, sign = 1))
        points += (self.__generate_outer_circle_points(angle))
        # points += (self.__generate_involute_curve(angle + self.base_tooth_angle, lambda x, y: np.sqrt(x**2 + y**2) > self.root_circle_radius, sign=-1))
        points += (self.__generate_root_circle_points(angle))
        # points += (self.__generate_involute_curve(angle + self.base_tooth_angle * 2, lambda x, y: np.sqrt(x**2 + y**2) > self.base_circle_radius))
        # points += self.__translate_and_rotate_points(points, angle)
        return points

    def points(self) -> Points:
        points:Points = []
        for i in range(self.num_teeth):
            angle = i * 2 * np.pi / self.num_teeth
            points += (self.__generate_tooth_points(angle))
        return points