
import numpy as np

def calculate_journey_from_polyline(polyline: np.ndarray[np.float32]):
    """
    计算多段线的总行程

    参数:
    polyline (np.ndarray[np.float32]): 包含多段线点坐标的二维数组，形状为 (n, 2)

    返回:
    float: 多段线的总行程
    """
    if len(polyline) < 2:
        raise ValueError("多段线至少需要两个点")
    
    # 计算相邻点之间的差值
    diff = np.diff(polyline, axis=0)
    
    # 计算每段的距离
    distances = np.sqrt(np.sum(diff ** 2, axis=1))
    
    # 累加所有段的距离
    total_journey = np.sum(distances)
    
    return total_journey