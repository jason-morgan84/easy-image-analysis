import pytest
import numpy as np
from core.shape import Shape

# test shape with missing attribute:
def test_shape_missing_attribute():
    with pytest.raises(AttributeError,match = "Shape class instantiated with missing arguement"):
        test = Shape (c = 1, z = 2, y = 3)

# test shape with unexpected attribute:
def test_shape_unexpected_attribute():
    with pytest.raises(AttributeError,match = "Shape class instantiated with unexpected arguement"):
        test = Shape (c = 1, z = 2, y = 3, x = 2, t = 5)

# test shape with non integer values
@pytest.mark.parametrize("c, z, y, x", [
    (0.5,1,2,3),
    (1,0.5,2,3),
    (0,1,0.5,3),
    (0,2,2,0.5)
    ])
def test_shape_non_int_values(c,z,y,x):
    with pytest.raises(TypeError, match = "for Shape class, expected integer for"):
        Shape(c = c,z = z,y = y,x = x)

# test that shape is immutable
def test_shape_immutability():
    test_c = 1
    test_z = 2
    test_y = 3
    test_x = 4

    test_shape = Shape(c = test_c,z = test_z,y = test_y,x = test_x)

    test_c = 11
    test_z = 12
    test_y = 13
    test_x = 14

    assert(test_shape.c == 1)
    assert(test_shape.z == 2)
    assert(test_shape.y == 3)
    assert(test_shape.x == 4)

def test_shape_iteration():
    test_shape = Shape(c = 2, x = 4, y = 1, z = -1)

    values = [item for item in test_shape]

    assert(values == [2,-1,1,4]); print(values)

def test_get_values():
    test_shape = Shape(c = 2, x = 4, y = 1, z = -1)

    assert test_shape[0] == 2
    assert test_shape["c"] == 2

    assert test_shape[1] == -1
    assert test_shape["z"] == -1

def test_set_values():
    test_shape = Shape(c = 2, x = 4, y = 1, z = -1)

    test_shape[0] = 5
    assert test_shape[0] == 5
    assert test_shape["c"] == 5

    test_shape["z"] = 16

    assert test_shape[1] == 16
    assert test_shape["z"] == 16


