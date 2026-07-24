import numpy as np

def transform_point(T: np.ndarray, point: np.ndarray) -> np.ndarray:
    """坐标转换"""
    point = np.append(point, 1.0)

    transformed_point = (T @ point)[:3]

    return transformed_point

def invert_transform(T: np.ndarray) -> np.ndarray:
    """倒转变换矩阵"""
    R = T[:3, :3]
    t= T[:3, 3]

    result = np.eye(4)
    result[:3, :3] = R.T
    result[:3, 3] = -R.T @ t

    return result

def compose_transform(T1: np.ndarray, T2: np.ndarray) -> np.ndarray:
    """组合两个变换矩阵"""
    return T1 @ T2