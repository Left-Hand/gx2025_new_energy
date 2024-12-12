import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from utils.io import *
from utils.plot import *
from utils.geo import *


#减速比
reducation_ratio:int = 48

#推杆半径
stick_radius_mm:float = 1

#推杆侧移
stick_shaft_mm:float = 34

#基圆半径
prime_circle_radius_mm:float = 45

#前轮到中线偏距
front_wheel_side_offset_mm:float = 24.9

#前轮到后轮偏距
front_wheel_front_offset_mm:float = 115

#前轮半径
front_wheel_radius_mm:float = 10

#后轮半径
back_wheel_radius_mm:float = 75



stick_radius:float = stick_radius_mm / 1000
stick_shaft:float = stick_shaft_mm / 1000
prime_circle_radius:float = prime_circle_radius_mm / 1000
front_wheel_side_offset:float = front_wheel_side_offset_mm / 1000
front_wheel_front_offset:float = front_wheel_front_offset_mm / 1000
front_wheel_radius:float = front_wheel_radius_mm / 1000
back_wheel_radius:float = back_wheel_radius_mm / 1000


file_path:str = 'C:/Users/Administrator/Downloads/曲线轨迹点集1.txt'

csv_data = pd.read_csv(file_path, sep=r'\s+', header=None, usecols=[0, 1, 2, 4], names=['s', 'x', 'y', 'r'])



x_array:np.float32 = np.float32(csv_data['x'].to_numpy()) / 1000
y_array:np.float32 = np.float32(csv_data['y'].to_numpy()) / 1000
r_array:np.float32 = np.float32(csv_data['r'].to_numpy()) / 1000

path_points:np.ndarray[np.float32] = np.column_stack((x_array, y_array))

# journey_step = s_array[1] - s_array[0]
total_journey = calculate_journey_from_polyline(path_points)

s_array:np.float32 = np.linspace(start = 0, stop = total_journey, num = r_array.size)

def journey_to_radian(journey: float | np.float32):
    return journey / back_wheel_radius / reducation_ratio

def roc_to_contour_radius(roc: float | np.float32):
    h:float = front_wheel_front_offset
    theta:float | np.float32 = np.arcsin(h / roc)
    radius_compensation:float | np.float32 = stick_radius / np.cos(theta)
    wave = - stick_shaft * np.tan(theta)
    return prime_circle_radius + radius_compensation + wave
    # return prime_circle_radius + radius_compensation


# print(journey_step)
# print(journey_to_rad(total_journey))
# print((total_journey))
# print(path_points[:5])
# print()


cr_array = roc_to_contour_radius(r_array)
rd_array = journey_to_radian(s_array)

stop_radian:float = rd_array[-1]
end_radian:float = np.pi * 2 - np.arctan(stick_radius / prime_circle_radius)
end_barb_len:float = 0.01
extra_points_cnt = 1000

#添加收尾弧
rd_array = np.append(rd_array, np.linspace(start = stop_radian, stop = end_radian, num = extra_points_cnt))
cr_array = np.append(cr_array, np.linspace(start = cr_array[-1], stop = prime_circle_radius + end_barb_len, num = extra_points_cnt))

#添加倒刺
rd_array = np.append(rd_array, np.linspace(start = end_radian, stop = 2 * np.pi, num = 2))
cr_array = np.append(cr_array, np.linspace(start = cr_array[0], stop = cr_array[0], num = 2))
# print(cr_array[:20])
# print(s_array[:20])
# print(s_array[-20:])
# print(rd_array[-20:])
plot_cam(cr_array, rd_array)
# plot_path(x_array, y_array)
# print(stop_radian, end_radian)