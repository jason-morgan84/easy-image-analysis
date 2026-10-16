import pytest
import numpy as np
from core.constants import DataType
from core.type import ImageInt, ArrayFloat, ImageFloat, ImageBinary, ValueInt, ValueFloat, ArrayInt
from core.data_checks import sample_data

"""test validate class"""
# test is_image or is_array flagged class without np.array
@pytest.mark.parametrize("dtype, invalid_input, message", [
    (ImageInt, 2, "expected np.array for DataType.ImageInt"), # not an array
    (ArrayFloat, "1", "expected np.array for DataType.ArrayFloat"), # not an array
    (ImageFloat, [1,2],"expected np.array for DataType.ImageFloat, got <class 'list'>"), # unexpected list
    (ArrayFloat, {"test": np.array([1,2,3])},"expected np.array for DataType.ArrayFloat, got <class 'dict'>"), #unexpected dict
])
def test_array_validation(dtype, invalid_input, message):
    with pytest.raises(TypeError, match = message):
        dtype.validate(invalid_input)


# test scalar class with list/tuple/np.array
@pytest.mark.parametrize("dtype, invalid_input, message", [
    (ValueInt, [1,2], "expected data type of <class 'numpy.uint8'> for DataType.ValueInt, got <class 'list'>"), # unexpected array
    (ValueInt, np.array([1,2,3]), "expected data type of <class 'numpy.uint8'> for DataType.ValueInt, got <class 'numpy.ndarray'>"), # unexpected np array
    (ValueFloat, (1,2),"expected data type of <class 'numpy.float64'> for DataType.ValueFloat, got <class 'tuple'>"), # unexpected tuple
])
def test_scalar_validation(dtype, invalid_input, message):
    with pytest.raises(TypeError, match = message):
        dtype.validate(invalid_input)

# test class with incorrect data type
@pytest.mark.parametrize("dtype, invalid_input, message", [
    (ValueInt, "2.0", "expected data type of <class 'numpy.uint8'> for DataType.ValueInt, got <class 'str'>"), # not an array
    (ImageBinary, np.array([1,2,3],np.float64), "expected np.array of <class 'numpy.uint8'> for DataType.ImageBinary, got float64"), # not an array
    (ArrayInt, np.array([1.0,1.1,1.2],np.float64),"expected np.array of <class 'numpy.uint8'> for DataType.ArrayInt, got float64"), # unexpected list
    (ArrayFloat, np.array([1,2,3], np.uint8),"expected np.array of <class 'numpy.float64'> for DataType.ArrayFloat, got uint8"), #unexpected dict
])
def test_incorrect_data_type(dtype, invalid_input, message):
    with pytest.raises(TypeError, match = message):
        dtype.validate(invalid_input)

# test class with max_value and input over max_value
@pytest.mark.parametrize("dtype, invalid_input, message", [
    # test removed, can't have data over 255 for uint8
    # (ImageInt, np.array([0,1,5,290], np.uint8), "expected data type of <class 'numpy.uint8'> for DataType.ValueInt, got <class 'str'>"), 
    (ImageFloat, np.array([0.5, 0.2, 1.5],np.float64),"array exceeds maximum value: DataType.ImageFloat has max_value of 1.0, not 1.5"), # unexpected list
])
def test_data_over_max_value(dtype, invalid_input, message):
    with pytest.raises(ValueError, match = message):
        dtype.validate(invalid_input)

# test class with min_value and input below min_value
@pytest.mark.parametrize("dtype, invalid_input, message", [
    # test removed, can't have data under 0 for uint8
    # (ImageInt, np.array([0,1,5,-5], np.uint8), "expected data type of <class 'numpy.uint8'> for DataType.ValueInt, got <class 'str'>"), 
    (ImageFloat, np.array([0.5, 0.2, -4.0],np.float64),"array below minimum value: DataType.ImageFloat has min_value of 0.0, not -4.0"), # unexpected list
])
def test_data_under_min_value(dtype, invalid_input, message):
    with pytest.raises(ValueError, match = message):
        dtype.validate(invalid_input)

"""test to"""
# call to function with incorrect input (input data not supplied dtype)
@pytest.mark.parametrize("dtype_call, invalid_input, dtype_to, message", [
    (ValueInt, sample_data(DataType.ValueFloat), DataType.ValueFloat,"data for conversion from DataType.ValueInt to DataType.ValueFloat does not meet constraints"), 
    (ImageBinary, sample_data(DataType.ImageInt,[1,2,3,4]), DataType.ImageInt, "data for conversion from DataType.ImageBinary to DataType.ImageInt does not meet constraints"),
    (ArrayInt, sample_data(DataType.ArrayFloat, [1,2]), DataType.ArrayInt,"data for conversion from DataType.ArrayInt to DataType.ArrayInt does not meet constraints"), 
    (ImageFloat, sample_data(DataType.ImageInt, [1,2,3]), DataType.ImageInt,"data for conversion from DataType.ImageFloat to DataType.ImageInt does not meet constraints"),
],
    ids=["value_int","image_binary","array_int","image_float"]
)
def test_to_incorrect_input(dtype_call, invalid_input,dtype_to, message):
    with pytest.raises(ValueError, match = message):
        dtype_call.to(invalid_input, dtype_to)

# call to function with non-permitted conversion
@pytest.mark.parametrize("dtype_call, invalid_input, dtype_to, message", [
    (ValueInt, sample_data(DataType.ValueInt), DataType.ArrayFloat,"conversion from DataType.ValueInt to DataType.ArrayFloat not permitted"), 
    (ImageFloat, sample_data(DataType.ImageFloat,[1,2,3,4]), DataType.ImageBinary, "conversion from DataType.ImageFloat to DataType.ImageBinary not permitted"),
    (ArrayInt, sample_data(DataType.ArrayInt, [1,2]), DataType.ValueInt,"conversion from DataType.ArrayInt to DataType.ValueInt not permitted"), 
],
    ids=["value_int","image_binary","array_int"]
)
def test_to_non_permitted_dtype(dtype_call, invalid_input,dtype_to, message):
    with pytest.raises(ValueError, match = message):
        dtype_call.to(invalid_input, dtype_to)


"""test _convert"""
# test conversions from ImageInt
@pytest.mark.parametrize("input, dtype_to", [
    (sample_data(DataType.ImageInt,[1,2,3]), DataType.ImageFloat), 
    (sample_data(DataType.ImageInt, [1,2,3]), DataType.ImageInt), 
],
    ids=["image_float","image_int"]
)
def test_convert_image_int(input, dtype_to):
    a = input
    a[0][0][0] = 0
    test_image = ImageInt.to(a, dtype_to)
    a[0][0][0] = 1
    dtype_to.validate(test_image)
    assert test_image.shape == (1,2,3)
    assert test_image[0][0][0] != 1

# test conversions from ImageFloat
@pytest.mark.parametrize("input, dtype_to", [
    (sample_data(DataType.ImageFloat,[1,2,3]), DataType.ImageFloat), 
    (sample_data(DataType.ImageFloat, [1,2,3]), DataType.ImageInt), 
],
    ids=["image_float","image_int"]
)
def test_convert_image_float(input, dtype_to):
    a = input
    a[0][0][0] = 0
    test_image = ImageFloat.to(a, dtype_to)
    a[0][0][0] = 1
    dtype_to.validate(test_image)
    assert test_image.shape == (1,2,3)
    assert test_image[0][0][0] != 1

# test conversions from ImageBinary
@pytest.mark.parametrize("input, dtype_to", [
    (sample_data(DataType.ImageBinary,[1,2,3]), DataType.ImageFloat), 
    (sample_data(DataType.ImageBinary, [1,2,3]), DataType.ImageInt), 
    (sample_data(DataType.ImageBinary, [1,2,3]), DataType.ImageBinary),
],
    ids=["image_float","image_int","image_bianry"]
)
def test_convert_image_binary(input, dtype_to):
    a = input
    a[0][0][0] = 0
    test_image = ImageBinary.to(a, dtype_to)
    a[0][0][0] = 1
    dtype_to.validate(test_image)
    assert test_image.shape == (1,2,3)
    assert test_image[0][0][0] != 1

# test conversions from ArrayInt
@pytest.mark.parametrize("input, dtype_to", [
    (sample_data(DataType.ArrayInt,[1,2,3]), DataType.ArrayInt), 
    (sample_data(DataType.ArrayInt, [1,2,3]), DataType.ArrayFloat), 
],
    ids=["array_int","array_float"]
)
def test_convert_array_int(input, dtype_to):
    a = input
    a[0][0][0] = 0
    test_image = ArrayInt.to(a, dtype_to)
    a[0][0][0] = 1
    dtype_to.validate(test_image)
    assert test_image.shape == (1,2,3)
    assert test_image[0][0][0] != 1

# test conversions from ArrayFloat
@pytest.mark.parametrize("input, dtype_to", [
    (sample_data(DataType.ArrayFloat,[1,2,3]), DataType.ArrayInt), 
    (sample_data(DataType.ArrayFloat, [1,2,3]), DataType.ArrayFloat), 
],
    ids=["array_int","array_float"]
)
def test_convert_array_float(input, dtype_to):
    a = input
    a[0][0][0] = 0
    test_image = ArrayFloat.to(a, dtype_to)
    a[0][0][0] = 1
    dtype_to.validate(test_image)
    assert test_image.shape == (1,2,3)
    assert test_image[0][0][0] != 1

# test conversions from ValueInt
@pytest.mark.parametrize("input, dtype_to", [
    (sample_data(DataType.ValueInt), DataType.ValueInt), 
    (sample_data(DataType.ValueInt), DataType.ValueFloat), 
],
    ids=["value_int","value_float"]
)
def test_convert_value_int(input, dtype_to):
    a = input
    test_image = ValueInt.to(a, dtype_to)
    a = 1
    dtype_to.validate(test_image)
    assert test_image != 1

# test conversions from ValueFloat
@pytest.mark.parametrize("input, dtype_to", [
    (sample_data(DataType.ValueFloat), DataType.ValueInt), 
    (sample_data(DataType.ValueFloat), DataType.ValueFloat), 
],
    ids=["value_int","value_float"]
)
def test_convert_value_float(input, dtype_to):
    a = input
    test_image = ValueFloat.to(a, dtype_to)
    a = 1
    dtype_to.validate(test_image)
    assert test_image != 1

# test for drift within ImageTypes
@pytest.mark.parametrize("DataType, Input, OutputType", [
    (DataType.ImageInt, np.array([1, 2], np.uint8), DataType.ImageFloat),      
    (DataType.ImageFloat, np.array([0.1, 1.0], np.float64), DataType.ImageInt),       
])
def test_for_value_drift_image_types(DataType, Input, OutputType):
    a = Input
    for i in range (5):
        b = DataType.to(value=a, dtype=OutputType)
        a = OutputType.to(value=b, dtype=DataType)
    c = Input
    for i in range (15):
        d = DataType.to(value=c, dtype=OutputType)
        c = OutputType.to(value=d, dtype=DataType)

    assert(a[0]== c[0])
    assert(a[1]== c[1])


# test for drift within value_types
@pytest.mark.parametrize("DataType, Input, OutputType", [
    (DataType.ValueFloat, 5.6, DataType.ValueInt),        
])
def test_for_value_drift_value_types(DataType, Input, OutputType):
    a = DataType.numpy(Input)
    for i in range (5):
        b = DataType.to(value=a, dtype=OutputType)
        a = OutputType.to(value=b, dtype=DataType)

    c = DataType.numpy(Input)
    for i in range (15):
        d = DataType.to(value=c, dtype=OutputType)
        c = OutputType.to(value=d, dtype=DataType)

    assert(a == c)
    assert(b == d)


# test for drift within array_types
@pytest.mark.parametrize("DataType, Input, OutputType", [
    (DataType.ArrayFloat, [5.6, 8.1], DataType.ArrayInt),        
])
def test_for_value_drift_array_types(DataType, Input, OutputType):
    a = DataType.numpy(Input)
    for i in range (5):
        b = DataType.to(value=a, dtype=OutputType)
        a = OutputType.to(value=b, dtype=DataType)

    c = DataType.numpy(Input)
    for i in range (15):
        d = DataType.to(value=c, dtype=OutputType)
        c = OutputType.to(value=d, dtype=DataType)

    assert(a[0] == c[0])
    assert(b[0] == d[0])


# goes through each member of DataType, checks that the required class variables have been 
# properly set
@pytest.mark.parametrize("enum_member", list(DataType))
def test_all_datatype_classes_have_required_attributes(enum_member):

    
    assert enum_member.data_type is not None, f"'{enum_member.__name__}.data_type' is not defined"
    assert enum_member.data_type == enum_member, f"'{enum_member.__name__}.data_type' ({enum_member.data_type}) does not match Enum member {enum_member}"
    assert enum_member.numpy is not None, f"'{enum_member.__name__}.numpy' is not defined"
    assert isinstance(enum_member.is_array, bool), f"'{enum_member.__name__}.is_array' is not boolean"










