import pytest
import numpy as np
from core.image import Image
from core.shape import Shape
from core.constants import DataType

#Insert wrong type
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

#Insert acceptable type where array type does not match DataType
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

    test_int_image = Image(mock_image_int,DataType.ImageInt,image_shape,image_map)

    test_float_image = Image(mock_float_image,DataType.ImageFloat,image_shape,image_map)

    test_binary_image = Image(mock_binary_image,DataType.ImageBinary,image_shape,image_map)

#Insert input array with more or less than 4 dimensions
def test_image_wrong_shape():
    mock_image_small = DataType.ImageInt(np.arange(120).reshape(6,4,5))
    mock_image_large = DataType.ImageInt(np.arange(120).reshape(2,3,2,2,5))

    image_shape = Shape(0,6,4,5)
    image_map = Shape(0,1,2,3)

    with pytest.raises(ValueError):
        test_image_small = Image(mock_image_small, DataType.ImageInt, image_shape, image_map)

    with pytest.raises(ValueError):
        test_image_large = Image(mock_image_large, DataType.ImageInt, image_shape, image_map)

#Input pixel data with different number of dimensions to image_shape
def test_image_non_matching_shape():
    mock_image_small = DataType.ImageInt(np.arange(120).reshape(2,3,4,5))


    image_shape_wrong = Shape(2,3,4,0)
    image_shape_right = Shape(2,3,4,5)
    image_map = Shape(0,1,2,3)

    with pytest.raises(ValueError):
        test_image_wrong= Image(mock_image_small, DataType.ImageInt, image_shape_wrong, image_map)

    test_image_right = Image(mock_image_small, DataType.ImageInt, image_shape_right, image_map)


#Input incorrect mapping (ie, shape data says z_dim = 5, but mapping associates z with an array dimension of size 3)
def test_image_non_mapping_shape():
    mock_image = DataType.ImageInt(np.arange(120).reshape(2,3,4,5))


    image_shape = Shape(2,3,4,5)
    image_map_wrong = Shape(0,1,3,2)
    image_map_wrong_repeat = Shape(0,1,1,1)
    image_map_right = Shape(0,1,2,3)

    with pytest.raises(ValueError):
        test_image_wrong= Image(mock_image, DataType.ImageInt, image_shape, image_map_wrong)

    with pytest.raises(ValueError):
        test_image_wrong= Image(mock_image, DataType.ImageInt, image_shape, image_map_wrong_repeat)

    test_image_right = Image(mock_image, DataType.ImageInt, image_shape, image_map_right)
