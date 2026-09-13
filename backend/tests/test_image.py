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

    image_map = Shape(0,1,2,3)

    with pytest.raises(TypeError):
        test_int_image = Image(pixel_array = mock_image_int,
                               image_map = image_map)

    with pytest.raises(TypeError):
        test_float_image = Image(pixel_array = mock_float_image,
                                 image_map = image_map)

    with pytest.raises(TypeError):
        test_binary_image = Image(pixel_array = mock_binary_image,
                                  image_map = image_map)

    correct_image = Image(pixel_array = DataType.ImageInt(mock_image_int),
                          image_map = Shape(2,3,4,5))

#Insert input array with more or less than 4 dimensions
def test_image_wrong_shape():
    mock_image_small = DataType.ImageInt(np.arange(120).reshape(6,4,5))
    mock_image_large = DataType.ImageInt(np.arange(120).reshape(2,3,2,2,5))

    image_map = Shape(0,1,2,3)

    with pytest.raises(ValueError):
        test_image_small = Image(pixel_array = mock_image_small, 
                                 image_map = image_map)

    with pytest.raises(ValueError):
        test_image_large = Image(pixel_array = mock_image_large,
                                 image_map = image_map)

#Input shape data not in Shape class
def test_image_wrong_class():
    mock_image = DataType.ImageInt(np.arange(120).reshape(2,3,4,5))

    image_map = (0,1,2,3)

    with pytest.raises(TypeError):
        test_image = Image(pixel_array = mock_image, 
                                 image_map = image_map)

#Get image shape of various shape pixel arrays 
def test_get_image():
    mock_image = DataType.ImageInt(np.arange(120).reshape(2,3,4,5))
    image_map = Shape(0,1,2,3)

    for n, dimension in enumerate(Image(mock_image, image_map).get_image_shape()):
        assert dimension == mock_image.value.shape[image_map[n]], f"{dimension}, {n}"

    image_map = Shape(2,3,1,0)
    for n, dimension in enumerate(Image(mock_image, image_map).get_image_shape()):
            print(dimension)
            assert dimension == mock_image.value.shape[image_map[n]], f"{dimension}, {n}"
    
