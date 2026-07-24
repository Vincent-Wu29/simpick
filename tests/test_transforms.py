import pytest
import numpy as np
from simpick.geometry.transforms import transform_point, invert_transform, compose_transform

def test_identity_tranform():
    """测试1：单位矩阵不改变点"""
    T = np.eye(4)

    point = np.array([1.0, 2.0, 3.0])

    result = transform_point(T, point)

    assert np.allclose(point, result, atol=1e-6)

def test_translation():
    """测试2：纯平移"""
    T = np.eye(4)
    T[:3, 3] = np.array([2.0, 3.0, 4.0])
    point = np.array([1.0, 2.0, 3.0])

    result = transform_point(T, point)
    expect = np.array([3.0, 5.0, 7.0])
    assert np.allclose(result, expect, atol=1e-6)


def test_rotation_z_90():
    """测试3：已知旋转"""
    T = np.array([
        [0, -1, 0, 0],
        [1, 0, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

    point = np.array([1.0, 0, 0])

    result = transform_point(T, point)
    expect = np.array([0, 1.0, 0])
    assert np.allclose(result, expect, atol=1e-6)

def test_inverse_round_trip():
    """测试4：变换后再反变换"""
    T = np.array([
            [0, -1.0, 0, 1.0],
            [1.0, 0, 0, 2.0],
            [0, 0, 1.0, 3.0],
            [0, 0, 0, 1]
        ])

    T_invert = invert_transform(T)
    
    point = np.array([1.0, 2.0, 3.0])

    result = transform_point(T_invert, transform_point(T, point))

    assert np.allclose(result, point, atol=1e-6)

def test_composition():
    """测试5：组合结果一致"""
    T_ab = np.array([
            [0, -1.0, 0, 1.0],
            [1.0, 0, 0, 2.0],
            [0, 0, 1.0, 3.0],
            [0, 0, 0, 1]
        ])

    T_bc = np.array([
            [0, -1.0, 0, 2.0],
            [1.0, 0, 0, 3.0],
            [0, 0, 1.0, 4.0],
            [0, 0, 0, 1]
        ])

    point = np.array([1.0, 2.0, 3.0])
    result1 = transform_point(
        T_ab,
        transform_point(T_bc, point)
    )

    T_ac = compose_transform(T_ab, T_bc)
    result2 = transform_point(T_ac, point)

    assert np.allclose(result1, result2, atol=1e-6)