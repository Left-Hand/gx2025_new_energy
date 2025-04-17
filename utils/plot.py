from utils.common import *

def plot_path(x_points: np.float32, y_points: np.float32):
    """
    绘制路径图

    参数:
    x_points (np.float32): x 坐标数组
    y_points (np.float32): y 坐标数组
    """
    fontdict={"family": "KaiTi", "size": 15, "color": "b"}

    plt.figure(figsize=(10, 6))
    plt.plot(x_points, y_points, marker='o', linestyle='-')
    plt.title('路径图', fontsize=13, fontdict = fontdict)
    
    plt.xlabel('X 坐标', fontsize=13, fontdict = fontdict)
    plt.ylabel('Y 坐标', fontsize=13, fontdict = fontdict)
    plt.grid(True)
    plt.axis('equal')  # 保持 x 和 y 轴的比例相同
    plt.show()

def plot_points(x_points: np.float32, y_points : np.float32, name:str = '') -> None:
    """
    绘制点集

    参数:
    x_points (np.float32): x 坐标数组
    y_points (np.float32): y 坐标数组
    """
    fontdict={"family": "KaiTi", "size": 15, "color": "b"}

    plt.figure(figsize=(10, 6))
    plt.plot(x_points, y_points, linestyle='-') 
    plt.title(name, fontsize=13, fontdict = fontdict)
    
    plt.xlabel('X 坐标', fontsize=13, fontdict = fontdict)
    plt.ylabel('Y 坐标', fontsize=13, fontdict = fontdict)
    plt.grid(True)
    plt.axis('equal')  # 保持 x 和 y 轴的比例相同
    plt.show()

def plot_points_of2(x_points1: np.float32, y_points1 : np.float32,x_points2: np.float32, y_points2 : np.float32, name:str = '') -> None:
    """
    绘制点集

    参数:
    x_points (np.float32): x 坐标数组
    y_points (np.float32): y 坐标数组
    """
    fontdict={"family": "KaiTi", "size": 15, "color": "b"}

    plt.figure(figsize=(10, 6))
    plt.plot(x_points1, y_points1, linestyle='-') 
    plt.plot(x_points2, y_points2, linestyle='-') 
    plt.title(name, fontsize=13, fontdict = fontdict)
    
    plt.xlabel('X 坐标', fontsize=13, fontdict = fontdict)
    plt.ylabel('Y 坐标', fontsize=13, fontdict = fontdict)
    plt.grid(True)
    plt.axis('equal')  # 保持 x 和 y 轴的比例相同
    plt.show()

def plot_cam(r_points: np.float32, theta_points: np.float32):
    """
    根据给定的半径和弧度绘制凸轮

    参数:
    r_points (np.float32): 半径数组
    theta_points (np.float32): 弧度数组
    """
    # 确保 theta_points 是以弧度为单位的
    if not np.all(theta_points >= 0) or not np.all(theta_points <= 2 * np.pi):
        raise ValueError("theta_points 必须在 [0, 2*pi] 范围内")

    # 创建极坐标图
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    
    # 绘制凸轮轮廓
    ax.plot(theta_points, r_points, label='Cam Profile', linewidth=2)
    
    # 添加标题和标签
    ax.set_title('凸轮轮廓图', va='bottom')
    ax.set_xlabel('弧度 (radians)')
    ax.set_ylabel('半径 (meters)')
    
    # 显示图例
    ax.legend()
    
    # 显示图形
    plt.show()