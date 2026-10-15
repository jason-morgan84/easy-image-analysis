import pytest
import numpy as np
from core.constants import DataType
from core.type import ImageInt, ArrayFloat, ImageFloat, ImageBinary, ValueInt, ValueFloat, ArrayInt
from core.type import sample_data

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
    (ImageFloat, np.array([0.5, 0.2, -4.0],np.float64),"array below maximum value: DataType.ImageFloat has min_value of 0, not -4"), # unexpected list
])
def test_data_under_min_value(dtype, invalid_input, message):
    with pytest.raises(ValueError, match = message):
        dtype.validate(invalid_input)





# tests array shape - is it maintained through conversion
def test_array_shape_maintenance():
    mock_image = np.arange(120).reshape(2,3,4,5)
    assert ImageInt(mock_image).value.shape == (2,3,4,5)
    assert ImageFloat(mock_image/1000).value.shape == (2,3,4,5)


# tests conversion immutability: modify original input after conversion
def test_immutablity_array_list():
    test_list = [2,3,4]
    test_type = ImageInt(test_list)
    test_list[0] = 5

    assert (test_list[0]!= test_type.value[0])

# goes through each member of DataType, checks that the required class variables have been 
# properly set
@pytest.mark.parametrize("enum_member", list(DataType))
def test_all_datatype_classes_have_required_attributes(enum_member):

    
    assert enum_member.data_type is not None, f"'{enum_member.__name__}.data_type' is not defined"
    assert enum_member.data_type == enum_member, f"'{enum_member.__name__}.data_type' ({enum_member.data_type}) does not match Enum member {enum_member}"
    assert enum_member.numpy is not None, f"'{enum_member.__name__}.numpy' is not defined"
    assert enum_member.allowed_sub_types is not None, f"'{enum_member.__name__}.allowed_subdtypes' is not defined"
    assert isinstance(enum_member.is_array, bool), f"'{enum_member.__name__}.is_array' is not boolean"

# test image conversions within image_types
@pytest.mark.parametrize("DataType, Input, OutputType, Output", [
    (ImageInt, [51, 10, 20], ImageFloat, 0.2),      
    (ImageInt, [0, 1, 1], ImageBinary, 0),       
    (ImageFloat, [0.4, 0.5], ImageInt, 102),     
    (ImageFloat, [1.0, 0.0], ImageBinary, 1),      
    (ImageBinary, [1, 0], ImageFloat, 1.0),    
    (ImageBinary, [0, 1], ImageInt, 0),  
])
def test_image_conversions(DataType, Input, OutputType, Output):
# test explict type conversions within ImageTypes gives expected output type
    assert DataType(Input).to(OutputType).data_type == OutputType.data_type, f"{DataType(Input).to(OutputType).value}"
# test implicit type conversions within ImageTypes gives expected output type
    assert OutputType(DataType(Input)).data_type == OutputType.data_type
# test explict type conversions gives expected output value
    assert (DataType(Input).to(OutputType).value[0] == Output)
# test implicit type conversions gives expected output value
    assert OutputType(DataType(Input)).value[0] == Output

# test for drift within ImageTypes
@pytest.mark.parametrize("DataType, Input, OutputType", [
    (ImageInt, [1, 2], ImageFloat),      
    (ImageFloat, [0.1, 1.0], ImageInt),       
    (ImageFloat, [0.1, 0.9], ImageBinary),     
    (ImageBinary, [1, 0], ImageFloat),      
    (ImageInt, [1, 0], ImageBinary),    
    (ImageBinary, [0, 1], ImageInt),    
])
def test_for_value_drift_image_types(DataType, Input, OutputType):
    a = DataType(Input)
    for i in range (5):
        b = a.to(OutputType).to(DataType)

    for i in range (15):
        c = a.to(OutputType).to(DataType)

    assert(b.value[0]== c.value[0])
    assert(b.value[1]== c.value[1])

# test conversions within value_types
@pytest.mark.parametrize("DataType, Input, OutputType, Output", [
    (ValueInt, 5, ValueFloat, 5.0),      
    (ValueFloat, 0.6, ValueInt, 1),       
])
def test_value_conversions(DataType, Input, OutputType, Output):
# test explict type conversions within value_types gives expected output type
    assert DataType(Input).to(OutputType).data_type == OutputType.data_type, f"{DataType(Input).to(OutputType).value}"
# test implicit type conversions within value_types gives expected output type
    assert OutputType(DataType(Input)).data_type == OutputType.data_type
# test explict type conversions gives expected output value
    assert (DataType(Input).to(OutputType).value == Output)
# test implicit type conversions gives expected output value
    assert OutputType(DataType(Input)).value == Output

# test for drift within value_types
@pytest.mark.parametrize("DataType, Input, OutputType", [
    (ValueFloat, 5.6, ValueInt),        
])
def test_for_value_drift_value_types(DataType, Input, OutputType):
    a = DataType(Input)
    for i in range (5):
        b = a.to(OutputType).to(DataType)

    for i in range (15):
        c = a.to(OutputType).to(DataType)

    assert(b.value== c.value)
    assert(b.value== c.value)

# test conversions within array_types
@pytest.mark.parametrize("DataType, Input, OutputType, Output", [
    (ArrayInt, [5, 2], ArrayFloat, 5.0),      
    (ArrayFloat, [0.6, 17.1], ArrayInt, 1),       
])
def test_array_conversions(DataType, Input, OutputType, Output):
# test explict type conversions within array_types gives expected output type
    assert DataType(Input).to(OutputType).data_type == OutputType.data_type, f"{DataType(Input).to(OutputType).value}"
# test implicit type conversions within array_types gives expected output type
    assert OutputType(DataType(Input)).data_type == OutputType.data_type
# test explict type conversions gives expected output value
    assert (DataType(Input).to(OutputType).value[0] == Output)
# test implicit type conversions gives expected output value
    assert OutputType(DataType(Input)).value[0] == Output

# test for drift within array_types
@pytest.mark.parametrize("DataType, Input, OutputType", [
    (ArrayFloat, [5.6, 8.1], ArrayInt),        
])
def test_for_value_drift_array_types(DataType, Input, OutputType):
    a = DataType(Input)
    for i in range (5):
        b = a.to(OutputType).to(DataType)

    for i in range (15):
        c = a.to(OutputType).to(DataType)

    assert(b.value[0] == c.value[0])
    assert(b.value[0] == c.value[0])



# test sample data generation
def test_sample_data():

# shape checks: Input value dtype where is_array = true but no shape passed
    with pytest.raises(TypeError, match="image data type \\(<class 'core.type.ImageInt'>\\) supplied without shape"):
        a = sample_data(ImageInt)

    with pytest.raises(TypeError, match="image data type \\(<class 'core.type.ImageFloat'>\\) supplied without shape"):
        b = sample_data(ImageFloat)

# shape checks: Shape passed, but not as np.array, tuple or list
    with pytest.raises(TypeError, match="Expected shape as list or tuple, got <class 'int'>"):
        a = sample_data(ImageInt,shape = 25)
    with pytest.raises(TypeError, match="Expected shape as list or tuple, got <class 'set'>"):  
        b = sample_data(ImageInt,shape = {25,24,1})

# shape checks: Shape passed, but not as array of integers
    with pytest.raises(TypeError, match="Shape should be array of integers, not <class 'float'>"):
        a = sample_data(ImageInt,shape = [1.0,2.4])
    with pytest.raises(TypeError, match="Shape should be array of integers, not <class 'str'>"):
        b = sample_data(ImageInt,shape = ("2","4","5"))

# shape checks: Shape as np.array, list, tuple
    a = sample_data(ImageInt,[2,4,5])
    b = sample_data(ImageFloat,(2,4,5))

# type checks: Input value of DataType type, output of expected type
    assert isinstance(sample_data(ImageInt,[2,3]), DataType.ImageInt.numpy)
    assert (sample_data(DataType.ImageFloat,[2,3])).data_type == DataType.ImageFloat
    assert (sample_data(DataType.ValueFloat)).data_type == DataType.ValueFloat
    assert (sample_data(DataType.ArrayInt, (5,4))).data_type == DataType.ArrayInt

#shape checks: For array dtype, does output have expected shape with randomized values
    assert (sample_data(ImageInt,[5,4], numpy=False)).value.shape == (5,4)
    assert (sample_data(ImageFloat,[1,2,3], numpy=False)).value.shape == (1,2,3)
    assert (sample_data(ArrayInt,[1,2,3,4], numpy=False)).value.shape == (1,2,3,4)

#shape checks: For array dtype, does output have expected shape with 0 values
    assert (sample_data(ImageInt,[5,4],zero = True, numpy=False)).value.shape == (5,4)
    assert (sample_data(ImageFloat,[1,2,3],zero = True, numpy=False)).value.shape == (1,2,3)
    assert (sample_data(ArrayInt,[1,2,3,4],zero = True, numpy=False)).value.shape == (1,2,3,4)
    #def sample_data(dtype, shape = None, zero = False):

# value constraint check: For dtype with min, max values, do random values conform to min and max
    a = (sample_data(ImageInt,[200,300,400], zero = True, numpy=False))
    assert a.value.max() <= a.data_type.max_value
    assert a.value.min() >= a.data_type.min_value




