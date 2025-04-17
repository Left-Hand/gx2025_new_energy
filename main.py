import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from utils.io import *
from utils.plot import *
from utils.geo import *
from utils.generate import *

from gen.GearGenerator import *
from gen.CircleGenerator import *
from gen.WheelGenerator import *
from shapely.geometry import LineString, MultiLineString, MultiPoint
from shapely.ops import split, unary_union
import networkx as nx


def shrink_points(raw_x: np.ndarray, raw_y: np.ndarray, radius: float) -> Tuple[np.ndarray, np.ndarray]:
    size = raw_x.size
    x = np.zeros(size, dtype=np.float32)
    y = np.zeros(size, dtype=np.float32)
    
    # Vectorized calculation for middle points
    last_x = raw_x[:-2]
    current_x = raw_x[1:-1]
    next_x = raw_x[2:]
    
    last_y = raw_y[:-2]
    current_y = raw_y[1:-1]
    next_y = raw_y[2:]
    
    vec_x = next_x - last_x
    vec_y = next_y - last_y  # Fixed vector calculation
    
    vec_length = np.sqrt(vec_x**2 + vec_y**2)
    
    # Compute offset points using vector operations
    new_x = current_x - radius * vec_y / vec_length
    new_y = current_y + radius * vec_x / vec_length
    
    # Assign values to output arrays
    x[1:-1] = new_x
    y[1:-1] = new_y
    
    # Preserve start/end points
    x[0], y[0] = raw_x[0] - radius * vec_y[0] / vec_length[0], raw_y[0] + radius * vec_x[0] / vec_length[0]
    x[-1], y[-1] = raw_x[-1] - radius * vec_y[-1] / vec_length[-1], raw_y[-1] + radius * vec_x[-1] / vec_length[-1]
    
    return x, y

#减速比
reducation_ratio:int = 48

#推杆半径
stick_radius_mm:float = 1

#凸轮厚度
cam_thickness_mm:float = 1.2

#推杆侧移
stick_shaft_mm:float = 31.75

#基圆半径
prime_circle_radius_mm:float = 55.65

#前轮到中线偏距
front_wheel_side_offset_mm:float = 24

#hou轮到中线偏距
# back_wheel_side_offset_mm:float = 65.8 + 0.6
back_wheel_side_offset_mm:float = (66.2 + 66.98 + 67.42 + 67.30)/4 - 0.6


#前轮到后轮偏距
front_wheel_front_offset_mm:float = 130.65

#后轮半径
back_wheel_radius_mm:float = 75

IGNORE_BACK = 20

# end_barb_mm:float = 4.0
end_barb_mm:float = 0.0

extra_points_cnt:int = 1000

route_path:str = 'data/points4.txt'
output_path:str = 'autogen/cam.dxf'

stick_radius:float = stick_radius_mm / 1000
stick_shaft:float = stick_shaft_mm / 1000
prime_circle_radius:float = prime_circle_radius_mm / 1000
front_wheel_side_offset:float = front_wheel_side_offset_mm / 1000
back_wheel_side_offset:float = back_wheel_side_offset_mm / 1000
front_wheel_front_offset:float = front_wheel_front_offset_mm / 1000
back_wheel_radius:float = back_wheel_radius_mm / 1000
cam_thickness = cam_thickness_mm / 1000
end_barb_meters:float = end_barb_mm / 1000



csv_data = pd.read_csv(route_path, sep=r'\s+', header=None, usecols=[0, 1, 2, 4], names=['s', 'x', 'y', 'r'])



route_x:np.float32 = np.float32(csv_data['x'].to_numpy()) / 1000
route_y:np.float32 = np.float32(csv_data['y'].to_numpy()) / 1000
path_roc:np.float32 = np.float32(csv_data['r'].to_numpy()) / 1000

wheel_x, wheel_y = shrink_points(route_x, route_y, back_wheel_radius)


path_points:np.ndarray[np.float32] = np.column_stack((wheel_x, wheel_y))

def calculate_cumulative_journey(points: np.ndarray) -> np.ndarray:
    """
    Compute cumulative journey array from 2D coordinates.
    
    Args:
        points (np.ndarray): Nx2 array of (x, y) coordinates.
    
    Returns:
        np.ndarray: 1D array of cumulative distances (meters).
    """
    # Compute differences between consecutive points
    deltas = np.diff(points, axis=0)
    segment_distances = np.sqrt(np.sum(deltas ** 2, axis=1))
    
    # Compute cumulative journey (starting at 0)
    return np.concatenate([[0.0], np.cumsum(segment_distances)])

s_array = calculate_cumulative_journey(path_points)

def journey_to_radian(journey: np.float32):
    return journey / back_wheel_radius / reducation_ratio

def roc_to_contour_radius(roc: np.float32):
    h:float = front_wheel_front_offset
    theta:np.float32 = np.arcsin(h / roc)
    wave =  - (stick_shaft + np.sign(theta) * (cam_thickness / 2)) * np.tan(theta)
    return prime_circle_radius + wave


radian_arr = journey_to_radian(s_array)
contour_arr = roc_to_contour_radius(path_roc)


stop_radian:float = radian_arr[-1]
end_radian:float = np.pi * 2 - np.arctan(stick_radius / prime_circle_radius)


#添加收尾弧
radian_arr = np.append(radian_arr, np.linspace(start = stop_radian, stop = end_radian, num = extra_points_cnt))
# contour_arr = np.append(contour_arr, np.linspace(start = contour_arr[-1], stop = prime_circle_radius + end_barb_meters, num = extra_points_cnt))
contour_arr = np.append(contour_arr, np.linspace(start = contour_arr[-1], stop = contour_arr[0], num = extra_points_cnt))

#添加倒刺
radian_arr = np.append(radian_arr, np.linspace(start = end_radian, stop = 2 * np.pi, num = 2))
contour_arr = np.append(contour_arr, np.linspace(start = contour_arr[0], stop = contour_arr[0], num = 2))



def radian_and_contour_to_cam(radian: np.float32, contour: np.float32) -> Tuple[np.float32, np.float32]:
    return contour * np.cos(radian), contour * np.sin(radian)

def save_cam(x: np.float32, y: np.float32) -> None:

    generate_dxf_from_points(x,y, output_path)     


from shapely.geometry import Polygon

def create_contour_polygon(x: np.ndarray, y: np.ndarray) -> Polygon:
    # Ensure coordinates form a closed loop (first point == last point)
    if not np.allclose(x[0], x[-1]) or not np.allclose(y[0], y[-1]):
        x = np.append(x, x[0])
        y = np.append(y, y[0])
    
    # Create Shapely Polygon
    return Polygon(np.column_stack((x, y)))

def detect_self_intersection(polygon: Polygon) -> bool:
    return not polygon.is_valid or polygon.is_self_intersecting

def simplify_polygon(polygon: Polygon, tolerance: float = 1e-6) -> Polygon:
    return polygon.simplify(tolerance, preserve_topology=True)

def prune_self_intersecting_contour(x: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    contour = LineString(np.column_stack((x, y)))
    polygon = create_contour_polygon(x, y)
    
    if not detect_self_intersection(polygon):
        return x, y
    
    # Split and simplify
    split_lines = split(contour, [pt for pt in contour.self_intersections])
    clean_lines = [line for line in split_lines.geoms if line.length > 0]
    
    # Reconstruct using graph traversal (as before)
    G = nx.Graph()
    for line in clean_lines:
        coords = list(line.coords)
        G.add_edge(coords[0], coords[-1])
    
    longest_path = max(nx.all_simple_paths(G, source=clean_lines[0].coords[0]),
                      key=lambda path: len(path))
    
    pruned_coords = np.array(longest_path)
    return pruned_coords[:, 0], pruned_coords[:, 1]

def analyze_contour_points(x: np.ndarray, y: np.ndarray) -> MultiPoint:
    return MultiPoint(np.column_stack((x, y)))

def get_extremes(points: MultiPoint) -> Tuple[float, float, float, float]:
    min_x, min_y = points.bounds[:2]
    max_x, max_y = points.bounds[2:]
    return min_x, max_x, min_y, max_y

raw_cam_x, raw_cam_y = radian_and_contour_to_cam(radian_arr, contour_arr)

def filter_xy(x, y):
    # Create polygon from raw contour
    raw_polygon = create_contour_polygon(x, y)

    # Check for self-intersections
    # if raw_polygon.is_self_intersecting:
    print("Contour is self-intersecting. Applying pruning...")
    return prune_self_intersecting_contour(raw_cam_x, raw_cam_y)
    # else:
        
    #     return raw_cam_x, raw_cam_y
    


def remap_xy(x: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Sort points by polar angle relative to their centroid
    
    Args:
        x (np.ndarray): X-coordinates
        y (np.ndarray): Y-coordinates
    
    Returns:
        Tuple[np.ndarray, np.ndarray]: Sorted (x, y) coordinates
    """

    # Compute polar angles (in radians)
    angles = np.arctan2(y, x)
    
    # Sort indices by angle (convert to 0-2π for proper ordering)
    sorted_indices = np.argsort(angles + 2 * np.pi)
    
    # Reorder coordinates
    sorted_x = x[sorted_indices]
    sorted_y = y[sorted_indices]
    
    return sorted_x, sorted_y


from shapely.geometry import Polygon, MultiPolygon

def prune_self_intersecting_contour2(x: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    # Create closed contour polygon
    polygon = create_contour_polygon(x, y)
    
    # Repair self-intersecting polygon
    # if polygon.is_self_intersecting or not polygon.is_valid:
    if True:
        # Use buffer(0) to fix topology
        repaired = polygon.buffer(0)
        
        # Handle possible MultiPolygon result
        if repaired.geom_type == 'MultiPolygon':
            # Select largest area polygon
            max_area = 0
            selected_poly = None
            for p in repaired.geoms:
                if p.area > max_area:
                    max_area = p.area
                    selected_poly = p
            repaired = selected_poly if selected_poly else repaired[0]
        
        # Extract coordinates from repaired polygon
        if repaired and repaired.exterior:
            coords = list(repaired.exterior.coords)
            return np.array(coords)[:,0], np.array(coords)[:,1]
    
    # Return original coordinates if no repair needed
    return x, y


cam_x, cam_y = shrink_points(raw_cam_x, raw_cam_y, stick_radius)
cam_x, cam_y = cam_x[1:-IGNORE_BACK], cam_y[1:-IGNORE_BACK]
cam_x = np.append(cam_x, cam_x[0])
cam_y = np.append(cam_y, cam_y[0])

cam_x, cam_y = prune_self_intersecting_contour2(cam_x, cam_y)
# cam_x, cam_y = remap_xy(cam_x, cam_y)
# cam_x, cam_y = filter_xy(cam_x, cam_y)
# cam_x, cam_y = shrink_points(raw_cam_x, raw_cam_y, 0.005)
plot_points_of2(cam_x, cam_y, raw_cam_x, raw_cam_y)
plot_points_of2(wheel_x, wheel_y, route_x, route_y)
# plot_points(cam_x, cam_y)
# plot_points(route_x, route_y)
save_cam(cam_x, cam_y)