import pytest
import numpy as np
from core.constants import DataPolicy
from core.type_policies import ImageInt, ArrayFloat, ImageFloat, ImageBinary, ValueInt, ValueFloat, ArrayInt
from core.data_checks import sample_data

"""test validate class"""
# test is_image or is_array flagged class without np.array
@pytest.mark.parametrize("dtype, invalid_input, message", [
    (ImageInt, 2, "expected np.array for DataPolicy.ImageInt"), # not an array
    (ArrayFloat, "1", "expected np.array for DataPolicy.ArrayFloat"), # not an array
    (ImageFloat, [1,2],"expected np.array for DataPolicy.ImageFloat, got <class 'list'>"), # unexpected list
    (ArrayFloat, {"test": np.array([1,2,3])},"expected np.array for DataPolicy.ArrayFloat, got <class 'dict'>"), #unexpected dict
])
def test_array_validation(dtype, invalid_input, message):
    with pytest.raises(TypeError, match = message):
        dtype.validate(invalid_input)


# test scalar class with list/tuple/np.array
@pytest.mark.parametrize("dtype, invalid_input, message", [
    (ValueInt, [1,2], "expected data type of <class 'numpy.uint8'> for DataPolicy.ValueInt, got <class 'list'>"), # unexpected array
    (ValueInt, np.array([1,2,3]), "expected data type of <class 'numpy.uint8'> for DataPolicy.ValueInt, got <class 'numpy.ndarray'>"), # unexpected np array
    (ValueFloat, (1,2),"expected data type of <class 'numpy.float64'> for DataPolicy.ValueFloat, got <class 'tuple'>"), # unexpected tuple
])
def test_scalar_validation(dtype, invalid_input, message):
    with pytest.raises(TypeError, match = message):
        dtype.validate(invalid_input)

# test class with incorrect data type
@pytest.mark.parametrize("dtype, invalid_input, message", [
    (ValueInt, "2.0", "expected data type of <class 'numpy.uint8'> for DataPolicy.ValueInt, got <class 'str'>"), # not an array
    (ImageBinary, np.array([1,2,3],np.float64), "expected np.array of <class 'numpy.uint8'> for DataPolicy.ImageBinary, got float64"), # not an array
    (ArrayInt, np.array([1.0,1.1,1.2],np.float64),"expected np.array of <class 'numpy.uint8'> for DataPolicy.ArrayInt, got float64"), # unexpected list
    (ArrayFloat, np.array([1,2,3], np.uint8),"expected np.array of <class 'numpy.float64'> for DataPolicy.ArrayFloat, got uint8"), #unexpected dict
])
def test_incorrect_data_type(dtype, invalid_input, message):
    with pytest.raises(TypeError, match = message):
        dtype.validate(invalid_input)

# test class with max_value and input over max_value
@pytest.mark.parametrize("dtype, invalid_input, message", [
    # test removed, can't have data over 255 for uint8
    # (ImageInt, np.array([0,1,5,290], np.uint8), "expected data type of <class 'numpy.uint8'> for DataPolicy.ValueInt, got <class 'str'>"), 
    (ImageFloat, np.array([0.5, 0.2, 1.5],np.float64),"array exceeds maximum value: DataPolicy.ImageFloat has max_value of 1.0, not 1.5"), # unexpected list
])
def test_data_over_max_value(dtype, invalid_input, message):
    with pytest.raises(ValueError, match = message):
        dtype.validate(invalid_input)

# test class with min_value and input below min_value
@pytest.mark.parametrize("dtype, invalid_input, message", [
    # test removed, can't have data under 0 for uint8
    # (ImageInt, np.array([0,1,5,-5], np.uint8), "expected data type of <class 'numpy.uint8'> for DataType.ValueInt, got <class 'str'>"), 
    (ImageFloat, np.array([0.5, 0.2, -4.0],np.float64),"array below minimum value: DataPolicy.ImageFloat has min_value of 0.0, not -4.0"), # unexpected list
])
def test_data_under_min_value(dtype, invalid_input, message):
    with pytest.raises(ValueError, match = message):
        dtype.validate(invalid_input)

"""test to"""
# call to function with incorrect input (input data not supplied dtype)
@pytest.mark.parametrize("dtype_call, invalid_input, dtype_to, message", [
    (ValueInt, sample_data(DataPolicy.ValueFloat), DataPolicy.ValueFloat,"data for conversion from DataPolicy.ValueInt to DataPolicy.ValueFloat does not meet constraints"), 
    (ImageBinary, sample_data(DataPolicy.ImageInt,[1,2,3,4]), DataPolicy.ImageInt, "data for conversion from DataPolicy.ImageBinary to DataPolicy.ImageInt does not meet constraints"),
    (ArrayInt, sample_data(DataPolicy.ArrayFloat, [1,2]), DataPolicy.ArrayInt,"data for conversion from DataPolicy.ArrayInt to DataPolicy.ArrayInt does not meet constraints"), 
    (ImageFloat, sample_data(DataPolicy.ImageInt, [1,2,3]), DataPolicy.ImageInt,"data for conversion from DataPolicy.ImageFloat to DataPolicy.ImageInt does not meet constraints"),
],
    ids=["value_int","image_binary","array_int","image_float"]
)
def test_to_incorrect_input(dtype_call, invalid_input,dtype_to, message):
    with pytest.raises(ValueError, match = message):
        dtype_call.to(invalid_input, dtype_to)

# call to function with non-permitted conversion
@pytest.mark.parametrize("dtype_call, invalid_input, dtype_to, message", [
    (ValueInt, sample_data(DataPolicy.ValueInt), DataPolicy.ArrayFloat,"conversion from DataPolicy.ValueInt to DataPolicy.ArrayFloat not permitted"), 
    (ImageFloat, sample_data(DataPolicy.ImageFloat,[1,2,3,4]), DataPolicy.ImageBinary, "conversion from DataPolicy.ImageFloat to DataPolicy.ImageBinary not permitted"),
    (ArrayInt, sample_data(DataPolicy.ArrayInt, [1,2]), DataPolicy.ValueInt,"conversion from DataPolicy.ArrayInt to DataPolicy.ValueInt not permitted"), 
],
    ids=["value_int","image_binary","array_int"]
)
def test_to_non_permitted_dtype(dtype_call, invalid_input,dtype_to, message):
    with pytest.raises(ValueError, match = message):
        dtype_call.to(invalid_input, dtype_to)


"""test _convert"""
# test conversions from ImageInt
@pytest.mark.parametrize("input, dtype_to", [
    (sample_data(DataPolicy.ImageInt,[1,2,3]), DataPolicy.ImageFloat), 
    (sample_data(DataPolicy.ImageInt, [1,2,3]), DataPolicy.ImageInt), 
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
    (sample_data(DataPolicy.ImageFloat,[1,2,3]), DataPolicy.ImageFloat), 
    (sample_data(DataPolicy.ImageFloat, [1,2,3]), DataPolicy.ImageInt), 
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
    (sample_data(DataPolicy.ImageBinary,[1,2,3]), DataPolicy.ImageFloat), 
    (sample_data(DataPolicy.ImageBinary, [1,2,3]), DataPolicy.ImageInt), 
    (sample_data(DataPolicy.ImageBinary, [1,2,3]), DataPolicy.ImageBinary),
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
    (sample_data(DataPolicy.ArrayInt,[1,2,3]), DataPolicy.ArrayInt), 
    (sample_data(DataPolicy.ArrayInt, [1,2,3]), DataPolicy.ArrayFloat), 
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
    (sample_data(DataPolicy.ArrayFloat,[1,2,3]), DataPolicy.ArrayInt), 
    (sample_data(DataPolicy.ArrayFloat, [1,2,3]), DataPolicy.ArrayFloat), 
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
    (sample_data(DataPolicy.ValueInt), DataPolicy.ValueInt), 
    (sample_data(DataPolicy.ValueInt), DataPolicy.ValueFloat), 
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
    (sample_data(DataPolicy.ValueFloat), DataPolicy.ValueInt), 
    (sample_data(DataPolicy.ValueFloat), DataPolicy.ValueFloat), 
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
    (DataPolicy.ImageInt, np.array([1, 2], np.uint8), DataPolicy.ImageFloat),      
    (DataPolicy.ImageFloat, np.array([0.1, 1.0], np.float64), DataPolicy.ImageInt),       
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
    (DataPolicy.ValueFloat, 5.6, DataPolicy.ValueInt),        
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
    (DataPolicy.ArrayFloat, [5.6, 8.1], DataPolicy.ArrayInt),        
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
@pytest.mark.parametrize("enum_member", list(DataPolicy))
def test_all_datatype_classes_have_required_attributes(enum_member):

    
    assert enum_member.data_type is not None, f"'{enum_member.__name__}.data_type' is not defined"
    assert enum_member.data_type == enum_member, f"'{enum_member.__name__}.data_type' ({enum_member.data_type}) does not match Enum member {enum_member}"
    assert enum_member.numpy is not None, f"'{enum_member.__name__}.numpy' is not defined"
    assert isinstance(enum_member.is_array, bool), f"'{enum_member.__name__}.is_array' is not boolean"










