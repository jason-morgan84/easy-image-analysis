import pytest
import numpy as np
from core.type import ImageInt, ImageFloat, ImageBinary, ValueInt, ValueFloat

def test_data_type_ImageInt():
    mock_image = np.arange(120).reshape(2,3,4,5)
    mock_image_high = np.array([1251,2,3,4,5,6,7,8,9,10,11,12]).reshape(2,2,3)
    mock_image_low = np.array([-1,2,3,4,5,6,7,8,9,10,11,12]).reshape(2,2,3)
    mock_image_float = np.array([1.5,2,3,4,5,6,7,8,9,10,11,12]).reshape(2,2,3)
    mock_image_string = np.array(["1.5",2,3,4,5,6,7,8,9,10,11,12]).reshape(2,2,3)

    #test with out of bounds low value
    with pytest.raises(ValueError):
        ImageInt(mock_image_low)

    #test with out of bounds high value
    with pytest.raises(ValueError):
        ImageInt(mock_image_high)

    #test with wrong type float
    with pytest.raises(TypeError):
        ImageInt(mock_image_float)

    #test with wrong type string
    with pytest.raises(TypeError):
        ImageInt(mock_image_string)

    #test conversion of 4d numpy array
    mock_image_ImageInt = ImageInt(mock_image)
    assert mock_image_ImageInt.shape == (2,3,4,5)

    #test conversion to np uint8
    assert isinstance(mock_image_ImageInt.to_uint8(),np.ndarray)
    assert mock_image_ImageInt.to_uint8().dtype == np.uint8
    assert mock_image_ImageInt.to_uint8().all() == mock_image.all()

    #test immutability
    mock_image[0][0][0][0] = 25
    assert (mock_image_ImageInt.to_uint8() != mock_image).any()

def test_data_type_ImageFloat():
    mock_image = (np.arange(120)/125).reshape(2,3,4,5)
    mock_image_high = np.array([0,0.5,1,0.8,0.9,0,1,0.7,0.8,0.1,0.8,2]).reshape(2,2,3)
    mock_image_low = np.array([0,0.5,1,0.8,0.9,0,1,0.7,0.8,0.1,0.8,-0.5]).reshape(2,2,3)
    mock_image_string = np.array([0,0.5,1,0.8,0.9,0,1,0.7,0.8,0.1,0.8,"0.5"]).reshape(2,2,3)

    #test with out of bounds low value
    with pytest.raises(ValueError):
        ImageFloat(mock_image_low)

    #test with out of bounds high value
    with pytest.raises(ValueError):
        ImageFloat(mock_image_high)

    #test with wrong type string
    with pytest.raises(TypeError):
        ImageFloat(mock_image_string)

    #test conversion of 4d numpy array
    mock_image_ImageFloat = ImageFloat(mock_image)
    assert mock_image_ImageFloat.shape == (2,3,4,5)

    #test conversion to np uint8
    assert isinstance(mock_image_ImageFloat.to_float64(),np.ndarray)
    assert mock_image_ImageFloat.to_float64().dtype == np.float64
    assert mock_image_ImageFloat.to_float64().all() == mock_image.all()

    #test immutability
    mock_image[0][0][0][0] = 1
    assert (mock_image_ImageFloat.to_float64() != mock_image).any()

def test_data_type_ImageBinary():
    mock_image = np.random.randint(2, size=120).reshape(2,3,4,5)
    mock_image_small = np.array([[0,0],[1,1]])
    mock_image_high = np.array([0,1,0,1,0,1,0,1,0,1,0,2]).reshape(2,2,3)
    mock_image_low = np.array([0,1,0,1,0,1,0,1,0,1,0,-1]).reshape(2,2,3)
    mock_image_middle = np.array([0,1,0,1,0,1,0,1,0,1,0,0.6]).reshape(2,2,3)
    mock_image_string = np.array([0,1,0,1,0,1,0,1,0,1,0,"1"]).reshape(2,2,3)
    mock_image_float = np.array([0,1,0,1,0,1,0,1,0,1,0,1.0]).reshape(2,2,3)

    #test with out of bounds low value
    with pytest.raises(ValueError):
        ImageBinary(mock_image_low)

    #test with out of bounds high value
    with pytest.raises(ValueError):
        ImageBinary(mock_image_high)

    with pytest.raises(ValueError):
        ImageBinary(mock_image_middle)

    #test with wrong type string
    with pytest.raises(TypeError):
        ImageBinary(mock_image_string)

    #test conversion containing float 1
    mock_image_ImageBinary = ImageBinary(mock_image_float)
    assert mock_image_ImageBinary.shape == (2,2,3)

    #test conversion of 4d numpy array
    mock_image_ImageBinary = ImageBinary(mock_image)
    assert mock_image_ImageBinary.shape == (2,3,4,5)

    #test conversion to np uint8
    assert isinstance(mock_image_ImageBinary.to_uint8(),np.ndarray)
    assert mock_image_ImageBinary.to_uint8().dtype == np.uint8
    assert mock_image_ImageBinary.to_uint8().all() == mock_image.all()

    #test conversion to np bool
    assert isinstance(mock_image_ImageBinary.to_boolean(),np.ndarray)
    assert mock_image_ImageBinary.to_boolean().dtype == np.bool
    assert mock_image_ImageBinary.to_boolean().all() == mock_image.all()

    #test immutability
    mock_image_ImageBinary = ImageBinary(mock_image_small)
    mock_image_small[0][0] = 1

    assert (mock_image_ImageBinary.to_uint8() != mock_image_small).any()

def test_data_type_ValueInt():
    mock_value = 2
    mock_value_float = 2.0
    mock_value_string = "2"

    #test with wrong type float
    with pytest.raises(TypeError):
        ValueInt(mock_value_float)

    #test with wrong type string
    with pytest.raises(TypeError):
        ValueInt(mock_value_string)

    #check correct type
    mock_value_ValueInt = ValueInt(mock_value)
    assert isinstance(mock_value_ValueInt,ValueInt)

    #test conversion to np uint8
    assert isinstance(mock_value_ValueInt.to_uint8(),np.uint8)
    assert mock_value_ValueInt.to_uint8() == mock_value

def test_data_type_ValueFloat():
    mock_value = 2
    mock_value_float = 2.0
    mock_value_string = "2"

    #test with wrong type float
    with pytest.raises(TypeError):
        ValueFloat(mock_value_string)

    #check correct type

    mock_value_ValueFloat = ValueFloat(mock_value)
    assert isinstance(mock_value_ValueFloat,ValueFloat)

    mock_value_ValueFloat = ValueFloat(mock_value_float)
    assert isinstance(mock_value_ValueFloat,ValueFloat)



    #test conversion to np uint8
    assert isinstance(mock_value_ValueFloat.to_float64(),np.float64)
    assert mock_value_ValueFloat.to_float64() == mock_value_float

