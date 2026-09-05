import pytest
import numpy as np
from core.shape import Shape

def test_shape_type_constraints():

    test_int= Shape(1,2,3,4)
    test_np_int = Shape(np.uint16(2),np.uint8(1),np.int64(5),np.int8(1))

    with pytest.raises(TypeError):
        Shape(0.5,1,2,3)

    with pytest.raises(TypeError):
        Shape(1,0.5,2,3)

    with pytest.raises(TypeError):
        Shape(5,1,2.1,3)

    with pytest.raises(TypeError):
        Shape(5,1,2,3.5)

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


