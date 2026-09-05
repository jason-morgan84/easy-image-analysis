import pytest
import numpy as np
from core.image import Image
from core.shape import Shape
from core.constants import DataType

def test_image_type_constraints():
    mock_image_int = np.int8(np.arange(120).reshape(2,3,4,5))
    mock_float_image = (np.arange(120)/125).reshape(2,3,4,5)
    mock_binary_image = np.bool(np.random.randint(2, size=120)).reshape(2,3,4,5)

    image_shape = Shape(2,3,4,5)
    image_map = Shape(0,1,2,3)

    with pytest.raises(TypeError):
        test_int_image = Image(mock_image_int,np.int8,image_shape,image_map), print(getattr(mock_image_int, "data_type", None))

    with pytest.raises(TypeError):
        test_float_image = Image(mock_float_image,DataType.ImageFloat,image_shape,image_map)

    with pytest.raises(TypeError):
        test_binary_image = Image(mock_binary_image,DataType.ImageFloat,image_shape,image_map)

def test_image_non_matching_types():
    mock_image_int = DataType.ImageInt(np.arange(120).reshape(2,3,4,5))
    mock_float_image = DataType.ImageFloat((np.arange(120)/125).reshape(2,3,4,5))
    mock_binary_image = DataType.ImageBinary(np.random.randint(2, size=120).reshape(2,3,4,5))

    image_shape = Shape(2,3,4,5)
    image_map = Shape(0,1,2,3)



    with pytest.raises(TypeError):
        test_int_image = Image(mock_image_int,DataType.ImageFloat,image_shape,image_map)

    with pytest.raises(TypeError):
        test_float_image = Image(mock_float_image,DataType.ImageInt,image_shape,image_map)

    with pytest.raises(TypeError):
        test_binary_image = Image(mock_binary_image,DataType.ImageInt,image_shape,image_map)

    print(getattr(mock_image_int,"data_type",None))
    test_int_image = Image(mock_image_int,DataType.ImageInt,image_shape,image_map)

    test_float_image = Image(mock_float_image,DataType.ImageFloat,image_shape,image_map)

    test_binary_image = Image(mock_binary_image,DataType.ImageBinary,image_shape,image_map)

