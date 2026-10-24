import pytest
import numpy as np
from core.shape import Shape, transpose
from core.constants import DataPolicy
from core.data_checks import sample_data


"""test Shape class"""
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

# test shape copy
def test_shape_copy():
    test_c = 1
    test_z = 2
    test_y = 3
    test_x = 4

    test_shape = Shape(c = test_c,z = test_z,y = test_y,x = test_x)
    test_shape_copy = test_shape.copy()

    assert (test_shape is not test_shape_copy)
    test_shape.c =5

    assert(test_shape_copy.c == 1)

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


"""test tranpose function"""

# send in non nparray 'value' 
def test_transpose_non_numpy_value():

    value = [[[[1,2,3],[1,2,3]],[[4,5,6],[4,5,6]]],[[[1,2,3],[1,2,3]],[[4,5,6],[4,5,6]]]]
    shape = Shape(c=0, z=1, y=2, x=3)

    with pytest.raises(TypeError, match = "expected value as np.array"):
        transpose(value=value, current_shape=shape, new_shape=shape)

# send in new_shape not as Shape class 
def test_transpose_non_shape_new_shape():
    value = sample_data(dtype=DataPolicy.ImageInt,shape=(1,2,3,4))
    wrong_shape = [0,1,2,3]
    right_shape = Shape(c=0, z=1, y=2, x=3)

    with pytest.raises(TypeError, match = "expected new_shape as Shape class"):
        transpose(value=value, new_shape=wrong_shape, current_shape=right_shape)

# send in new_shape with inproper value (less than 0, greater than Shape.max_image_dimensions)
def test_transpose_new_shape_incorrect_dimensions():
    value = sample_data(dtype=DataPolicy.ImageInt,shape=(1,2,3,4))
    wrong_shape = Shape(c=5, z=1, y=2, x=3)
    right_shape = Shape(c=0, z=1, y=2, x=3)

    with pytest.raises(ValueError, match = "new_shape shape dimensions out of range"):
        transpose(value=value, new_shape=wrong_shape, current_shape=right_shape)

    wrong_shape = Shape(c=0, z=1, y=-2, x=3)

    with pytest.raises(ValueError, match = "new_shape shape dimensions out of range"):
        transpose(value=value, new_shape=wrong_shape, current_shape=right_shape)

# send in current_shape not as Shape class 
def test_transpose_non_shape_current_shape():

    value = sample_data(dtype=DataPolicy.ImageInt,shape=(1,2,3,4))
    wrong_shape = [0,1,2,3]
    right_shape = Shape(c=0, z=1, y=2, x=3)

    with pytest.raises(TypeError, match = "expected current_shape as Shape class"):
        transpose(value=value, new_shape=right_shape, current_shape=wrong_shape)

# send in new_shape with inproper value (less than 0, greater than Shape.max_image_dimensions)
def test_transpose_current_shape_incorrect_dimensions():

    value = sample_data(dtype=DataPolicy.ImageInt,shape=(1,2,3,4))
    wrong_shape = Shape(c=5, z=1, y=2, x=3)
    right_shape = Shape(c=0, z=1, y=2, x=3)

    with pytest.raises(ValueError, match = "current_shape shape dimensions out of range"):
        transpose(value=value, new_shape=right_shape, current_shape=wrong_shape)

    wrong_shape = Shape(c=0, z=1, y=-2, x=3)

    with pytest.raises(ValueError, match = "current_shape shape dimensions out of range"):
        transpose(value=value, new_shape=right_shape, current_shape=wrong_shape)

# Send in valid new_shape and value| output with expected shape |
def test_transpose():

    value = sample_data(dtype=DataPolicy.ImageInt,shape=(1,2,3,4))
    new_shape = Shape(c=3, z=2, y=1, x=0)
    current_shape = Shape(c=0, z=1, y=2, x=3)

    output_shape = transpose(value=value, new_shape=new_shape, current_shape=current_shape)

    assert output_shape.shape == (4,3,2,1)
    assert value[0][0][0][0] == output_shape[0][0][0][0]
    assert value[0][1][2][3] == output_shape[3][2][1][0]

    new_shape = Shape(c=1, z=0, y=3, x=2)
    output_shape = transpose(value=value, new_shape=new_shape, current_shape=current_shape)
    assert output_shape.shape == (2,1,4,3)
    assert value[0][0][0][0] == output_shape[0][0][0][0]
    assert value[0][1][2][3] == output_shape[1][0][3][2]