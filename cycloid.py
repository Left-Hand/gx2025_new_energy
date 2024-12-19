import numpy as np
import matplotlib.pyplot as plt 
from matplotlib.patches import Circle
import ezdxf
import cv2

from typing import Tuple, List

# 参数设置
R_mm: float = 16
r_mm: float = 1.2
N_: float = 20
E_mm: float = 0.7

R_:float = R_mm / 1000
r_:float = r_mm / 1000
E_:float = E_mm / 1000

def phi(t: np.ndarray) -> np.ndarray:
    """计算角度 phi"""
    return -np.arctan(np.sin((1.0 - N_) * t) / ((R_ / E_ / N_) - np.cos((1.0 - N_) * t)))

def generate_points(t: np.ndarray) -> np.ndarray:
    """计算点的坐标"""
    x = R_ * np.cos(t) - r_ * np.cos(t - phi(t)) - (E_ * np.cos(N_ * t)) + E_
    y = -R_ * np.sin(t) + r_ * np.sin(t - phi(t)) + (E_ * np.sin(N_ * t))
    return np.column_stack((x, y))

# 时间数组
t: np.ndarray = np.linspace(0, 2 * np.pi, 2000)

# 计算点集
points: np.ndarray = generate_points(t)

# 将坐标转换为闭合的轮廓形式
contour: np.ndarray = points.reshape((-1, 1, 2))

# 获取离原点最远的点
distances: np.ndarray = np.linalg.norm(points, axis=1)
max_distance_index: int = np.argmax(distances)
max_distance: float = distances[max_distance_index]
farthest_point: np.ndarray = points[max_distance_index]

# 绘制图形
# ax: SubplotBase
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(points[:, 0], points[:, 1], label='cycloid')

circles: List[Circle] = []
for i in range(int(N_)):
    angle: float = float(i) / N_ * np.pi * 2
    center: Tuple[float, float] = (-R_ * np.cos(angle), R_ * np.sin(angle))
    circle: Circle = Circle(center, r_, fill=False, edgecolor='red', linewidth=2, label='Circle')
    circles.append(circle)

circle: Circle = Circle((0, 0), max_distance, fill=False, edgecolor='blue', linewidth=2, label='Circle')
circles.append(circle)

for circle in circles:
    ax.add_patch(circle)

# 设置标题和标签
ax.set_title('Cycloid')
ax.set_xlabel('X')
ax.set_ylabel('Y')

# 保持比例
ax.axis('equal')

# 显示网格
ax.grid(True)

# 显示图例
ax.legend()

# 显示图形
plt.show()

# 创建一个新的 DXF 文档
doc: ezdxf.document.Drawing = ezdxf.new('R2010')
msp: ezdxf.layouts.Modelspace = doc.modelspace()

# 添加多边形
polygon: ezdxf.entities.LWPolyline = msp.add_lwpolyline(points, dxfattribs={'closed': True})

# 保存 DXF 文件
doc.saveas('autogen/cycloid.dxf')