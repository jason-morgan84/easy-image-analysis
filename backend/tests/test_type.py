import pytest
import numpy as np
from core.type import ImageInt, ImageFloat, ImageBinary, ValueInt, ValueFloat

def test_data_type_ImageInt():
    mock_image = np.arange(120).reshape(2,3,4,5)
    mock_image_high = np.array([1251,2,3,4,5,6,7,8,9,10,11,12]).reshape(2,2,3)
    mock_image_low = np.array([-1,2,3,4,5,6,7,8,9,10,11,12]).reshape(2,2,3)
    mock_image_float = np.array([1.5,2,3,4,5,6,7,8,9,10,11,12]).reshape(2,2,3)
    mock_image_string = np.array(["1.5",2,3,4,5,6,7,8,9,10,11,12]).reshape(2,2,3)
    mock_image_list = [[0,0,0],[1,1,1],[2,2,2],[3,3,3]]
    mock_image_np = np.array([0,1,2])

    # test with out of bounds low value
    with pytest.raises(ValueError):
        ImageInt(mock_image_low)

    # test with out of bounds high value
    with pytest.raises(ValueError):
        ImageInt(mock_image_high)

    # test with wrong type float
    with pytest.raises(TypeError):
        ImageInt(mock_image_float)

    # test with wrong type string
    with pytest.raises(TypeError):
        ImageInt(mock_image_string)

    # test conversion of 4d list
    mock_image_ImageInt_list = ImageInt(mock_image_list)
    assert mock_image_ImageInt_list.shape == (4,3)

    # test conversion of 4d numpy array
    mock_image_ImageInt = ImageInt(mock_image)
    assert mock_image_ImageInt.shape == mock_image.shape

    # test conversion to np uint8
    assert isinstance(mock_image_ImageInt.to_uint8(),np.ndarray)
    assert mock_image_ImageInt.to_uint8().dtype == np.uint8
    assert mock_image_ImageInt.to_uint8().all() == mock_image.all()

    #test immutability of list inputs
    mock_image_np_ImageInt = ImageInt(mock_image_np)
    mock_image_np[0] = 12
    assert (mock_image_np_ImageInt.value[0] != mock_image_np[0])

    # test immutability of np.array inputst
    mock_image_list[0][0] = 12
    assert (mock_image_ImageInt_list.to_uint8()[0][0] != np.uint8(mock_image_list[0][0]))

def test_data_type_ImageFloat():
    mock_image = (np.float64(np.arange(120))/125).reshape(2,3,4,5)
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

    #test immutability of np inputs
    mock_image[0][0][0][1] = 1
    assert (mock_image_ImageFloat.value[0][0][0][1] != mock_image[0][0][0][1])

    #test immutability of lists
    mock_list_image = [0.1,0.2,0.3]
    mock_list_image_FloatImage = ImageFloat(mock_list_image)
    mock_list_image[0] = 1
    assert (mock_list_image_FloatImage.value[0] != mock_list_image[0])

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

    #test immutability of np inputs
    mock_image_ImageBinary = ImageBinary(mock_image_small)
    mock_image_small[0][0] = 1
    assert (mock_image_ImageBinary.to_uint8() != mock_image_small).any()

    #test immutability of list inputs
    mock_list_image = [0,1,0]
    mock_list_image_ImageBinary = ImageBinary(mock_list_image)
    mock_list_image[0] = 1
    assert (mock_list_image_ImageBinary.value[0] != mock_list_image[0])

def test_data_type_ValueInt():
    mock_value = 2
    mock_value_np = np.uint8(2)
    mock_value_float = 2.0
    mock_value_string = "2"

    mock_value_np_ValueInt = ValueInt(mock_value_np)

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

    #test immutability
    mock_value_ValueInt = ValueInt(mock_value)
    mock_value = 3
    assert(mock_value_ValueInt != mock_value)

    mock_value_ValueInt = ValueInt(mock_value_np)
    mock_value_np = 3
    assert(mock_value_ValueInt != mock_value_np)

def test_data_type_ValueFloat():
    mock_value = 2
    mock_value_float = 2.0
    mock_value_string = "2"
    mock_value_float_np = np.float64(2.1)

    #test with wrong type float
    with pytest.raises(TypeError):
        ValueFloat(mock_value_string)

    #check correct type
    mock_value_ValueFloat = ValueFloat(mock_value)
    assert isinstance(mock_value_ValueFloat,ValueFloat)

    mock_value_ValueFloat = ValueFloat(mock_value_float)
    assert isinstance(mock_value_ValueFloat,ValueFloat)

    #test conversion to np float64
    assert isinstance(mock_value_ValueFloat.to_float64(),np.float64)
    assert mock_value_ValueFloat.to_float64() == mock_value_float

    #test immutability
    mock_value_ValueFloat = ValueFloat(mock_value_float)
    mock_value_float = 3.0
    assert(mock_value_ValueFloat != mock_value_float)

    mock_value_ValueFloat = ValueFloat(mock_value_float_np)
    mock_value_float = 5.1
    assert(mock_value_ValueFloat != mock_value_float_np)

def test_image_conversions_ImageInt():

    mock_int_image = ImageInt(np.arange(120).reshape(2,3,4,5))
    #mock_int_image[0][0][0][0] = 5
    mock_float_image = (np.arange(120)/125).reshape(2,3,4,5)
    mock_binary_image = ImageInt(np.random.randint(2, size=120).reshape(2,3,4,5))
    #test single conversions - function and shape
    
    #test single conversion int to float, correct shape
    mock_int_image_convert = mock_int_image.to_ImageFloat()
    assert(mock_int_image_convert.shape == mock_int_image.shape)

    #test single conversion int to binary, correct shape
    mock_binary_image_convert = mock_binary_image.to_ImageBinary()
    assert(mock_binary_image_convert.shape == mock_binary_image.shape)

    #test single conversion int to float, correct value
    specific_int_image = ImageInt([0,51,102,153,204,255])
    specific_float_image = ImageFloat([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    np.testing.assert_array_almost_equal(specific_int_image.to_ImageFloat().value, specific_float_image.value)

    #test single conversion int to binary, correct value
    specific_int_image = ImageInt([0,0,0,0,1,1,1,1])
    specific_binary_image = ImageBinary([0, 0, 0, 0, 1, 1, 1, 1])
    np.testing.assert_array_almost_equal(specific_int_image.to_ImageBinary().value, specific_binary_image.value)

    """#test single conversion float to int, correct shape
    mock_int_image_convert = mock_int_image_convert.to_ImageInt()
    assert(mock_int_image_convert.shape == mock_int_image.shape)"""

    #test that repeated int to float conversions don't lead to drift in values
    for i in range(3):
       mock_int_image_3_convert = mock_int_image.to_ImageFloat().to_ImageInt()

    for i in range(7):
        mock_int_image_7_convert = mock_int_image.to_ImageFloat().to_ImageInt()

    np.testing.assert_array_equal(mock_int_image_3_convert.shape,mock_int_image_7_convert.shape)


def test_image_conversions_ImageFloat():

    mock_int_image = ImageInt(np.arange(120).reshape(2,3,4,5))
    mock_float_image = ImageFloat((np.arange(120)/125).reshape(2,3,4,5))
    mock_binary_image = ImageFloat(np.float64(np.random.randint(2, size=120)).reshape(2,3,4,5))
    #test single conversions - function and shape
    
    #test single conversion float to int, correct shape
    mock_int_image_convert = mock_float_image.to_ImageInt()
    assert(mock_int_image_convert.shape == mock_int_image.shape)

    #test single conversion float to binary, correct shape
    mock_binary_image_convert = mock_binary_image.to_ImageBinary()
    assert(mock_binary_image_convert.shape == mock_binary_image.shape)

    #test single conversion float to int, correct value
    specific_int_image = ImageInt([0,51,102,153,204,255])
    specific_float_image = ImageFloat([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    np.testing.assert_array_almost_equal(specific_float_image.to_ImageInt().value, specific_int_image.value)

    #test single conversion float to binary, correct value
    specific_float_image = ImageFloat([0.0,0.0,0.0,0.0,1.0,1.0,1.0,1.0])
    specific_binary_image = ImageBinary([0, 0, 0, 0, 1, 1, 1, 1])
    np.testing.assert_array_almost_equal(specific_float_image.to_ImageBinary().value, specific_binary_image.value)

def test_binary_conversions_ImageFloat():

    mock_binary_image = ImageBinary(np.random.randint(2, size=120).reshape(2,3,4,5))
    #test single conversions - function and shape
    
    #test single conversion binary to int, correct shape
    mock_binary_image_convert = mock_binary_image.to_ImageInt()
    assert(mock_binary_image_convert.shape == mock_binary_image.shape)

    #test single conversion binary to float, correct shape
    mock_binary_image_convert = mock_binary_image.to_ImageFloat()
    assert(mock_binary_image_convert.shape == mock_binary_image.shape)

    #test single conversion binary to int, correct value
    specific_binary_image = ImageBinary([0, 0, 0, 1, 1, 1])
    specific_int_image = ImageInt([0, 0, 0, 1, 1, 1])
    np.testing.assert_array_equal(specific_binary_image.to_ImageInt().value, specific_int_image.value)

    #test single conversion binary to float, correct value
    specific_binary_image = ImageBinary([0, 0, 0, 1, 1, 1])
    specific_float_image = ImageBinary([0.0, 0.0, 0.0, 1.0, 1.0, 1.0])
    np.testing.assert_array_almost_equal(specific_binary_image.to_ImageFloat().value, specific_float_image.value)

    #test that repeated binary to float conversions don't lead to drift in values
    for i in range(3):
       mock_binary_image_3_convert = mock_binary_image.to_ImageFloat().to_ImageBinary()

    for i in range(7):
        mock_binary_image_7_convert = mock_binary_image.to_ImageFloat().to_ImageBinary()

    np.testing.assert_array_equal(mock_binary_image_3_convert.shape,mock_binary_image_7_convert.shape)

def test_value_conversions():
    # test single conversions - function and shape
    test_int = 2
    test_float = 3.0

    assert((ValueFloat(test_float).to_ValueInt().value) == 3)

    assert((ValueInt(test_int).to_ValueFloat().value) == 2.0)

    # test repeated conversions between int and float - any drift?

    for i in range(3):
       test_int_image_3_convert = ValueInt(test_int).to_ValueFloat().to_ValueInt()

    for i in range(7):
        test_int_image_7_convert = ValueInt(test_int).to_ValueFloat().to_ValueInt()

    assert(test_int_image_3_convert.value == test_int_image_7_convert.value)

#test implicit conversion ImageFloat or ImageBianary to ImageInt
def test_implicit_conversion_to_int():
    mock_float_image = ImageFloat((np.arange(120)/125).reshape(2,3,4,5))
    mock_binary_image = ImageBinary(np.random.randint(2, size=120).reshape(2,3,4,5))

    #test single conversion int to float, correct shape
    mock_int_image_convert = ImageInt(mock_float_image)
    assert(mock_int_image_convert.shape == mock_float_image.shape)

    #test single conversion int to binary, correct shape
    mock_int_image_convert = ImageInt(mock_binary_image)
    assert(mock_int_image_convert.shape == mock_binary_image.shape)

def test_implicit_conversion_to_float():
    mock_int_image = ImageInt((np.arange(120)).reshape(2,3,4,5))
    mock_binary_image = ImageBinary(np.random.randint(2, size=120).reshape(2,3,4,5))

    #test single conversion int to float, correct shape
    mock_int_image_convert = ImageFloat(mock_int_image)
    assert(mock_int_image_convert.shape == mock_int_image.shape)

    #test single conversion int to binary, correct shape
    mock_int_image_convert = ImageFloat(mock_binary_image)
    assert(mock_int_image_convert.shape == mock_binary_image.shape)

def test_implicit_conversion_to_binary():
    mock_int_image = ImageInt([[0,0,0],[1,1,1]])
    mock_float_image = ImageFloat([[0,0,0],[1,1,1]])

    #test single conversion int to float, correct shape
    mock_int_image_convert = ImageBinary(mock_int_image)
    assert(mock_int_image_convert.shape == mock_int_image.shape)

    #test single conversion int to binary, correct shape
    mock_int_image_convert = ImageBinary(mock_float_image)
    assert(mock_int_image_convert.shape == mock_float_image.shape)

# test implicit conversions to Value_int
def test_implicit_conversion_value_int():
    float_value = 2.4

    test = ValueFloat(float_value)
    test_implicit_int = ValueInt(test)

# test implicit conversions to Value_float
def test_implicit_conversion_value_float():
    int_value = 2

    test = ValueInt(int_value)
    test_implicit_float = ValueFloat(test)

# test test_sample for ImageInt
def test_test_sample_for_ImageInt():
    with pytest.raises(TypeError):
        ImageInt.test_sample(2)

    with pytest.raises(TypeError):
        ImageInt.test_sample("2")

    with pytest.raises(TypeError):
        ImageInt.test_sample((1.0,2.0))

    assert(ImageInt.test_sample((2,3,4,5)).value.shape == (2,3,4,5))

# test test_sample for ImageFloat
def test_test_sample_for_ImageFloat():
    with pytest.raises(TypeError):
        ImageFloat.test_sample(2)

    with pytest.raises(TypeError):
        ImageFloat.test_sample("2")

    with pytest.raises(TypeError):
        ImageFloat.test_sample((1.0,2.0))

    assert(ImageFloat.test_sample((2,3,4,5)).value.shape == (2,3,4,5))

# test test_sample for ImageBinary
def test_test_sample_for_ImageBinary():
    with pytest.raises(TypeError):
        ImageBinary.test_sample(2)

    with pytest.raises(TypeError):
        ImageBinary.test_sample("2")

    with pytest.raises(TypeError):
        ImageBinary.test_sample((1.0,2.0))

    assert(ImageBinary.test_sample((2,3,4,5)).value.shape == (2,3,4,5))

# test test_sample for ValueInt
def test_test_sample_for_ValueInt():

    assert(isinstance(ValueInt.test_sample(),ValueInt))


# test test_sample for ValueInt
def test_test_sample_for_ValueFloat():

    assert(isinstance(ValueFloat.test_sample(),ValueFloat))