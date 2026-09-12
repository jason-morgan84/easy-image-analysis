import pytest
import numpy as np
from core.constants import DataType
from core.type import ImageInt, ArrayFloat, ImageFloat, ImageBinary, ValueInt, ValueFloat, ArrayInt
from core.type import sample_data


@pytest.mark.parametrize("DataType, invalid_input", [
    (ImageInt, 5.18),
    (ImageFloat, "not_a_number"),
    (ValueInt, 3.14),
    (ValueFloat, "not_a_number"),
    (ImageBinary, -2515.21),
])
def test_base_type_error_handling(DataType, invalid_input):
    with pytest.raises(TypeError):
        DataType(invalid_input)

# tests is_array: sends arrays to types expecting scalars and vice versa
@pytest.mark.parametrize("DataType, invalid_input", [
    (ImageInt, 2), # not an array
    (ArrayFloat, 1), # not an array
    (ValueInt, [1,2]), # unexpected list
    (ValueFloat, np.array([1,2,3])), #unexpected np.array
])
def test_is_array_validation(DataType, invalid_input):
    with pytest.raises(TypeError):
        DataType(invalid_input)

# tests array shape - is it maintained through conversion
def test_array_shape_maintenance():
    mock_image = np.arange(120).reshape(2,3,4,5)
    assert ImageInt(mock_image).value.shape == (2,3,4,5)
    assert ImageFloat(mock_image/1000).value.shape == (2,3,4,5)

# test type bounds
@pytest.mark.parametrize("DataType, invalid_input", [
    (ImageInt, [-1, 10, 20]),       # Below min_val (0)
    (ImageInt, [0, 5, 260]),        # Above max_val (255)
    (ImageFloat, [-0.1, 0.5]),      # Below min_val (0.0)
    (ImageFloat, [0.5, 1.2]),       # Above max_val (1.0)
    (ImageBinary, [1, 2]),       # Above max_val (1.0)
])
def test_min_max_bounds(DataType, invalid_input):
    with pytest.raises(ValueError):
        DataType(invalid_input)

#to_numpy: Convert value using to_numpy function
def test_to_numpy():
    test_array = ImageInt([1,2,3,4])
    assert isinstance(test_array.to_numpy()[0],test_array.numpy)

    test_array = ImageFloat([1,0.2,0.3,0.4])
    assert isinstance(test_array.to_numpy()[0],test_array.numpy)

    test_value = ValueFloat(1.2)
    assert isinstance(test_value.to_numpy(),test_array.numpy)

#Immutability: Modify original input list after instantiation of array data type
def test_immutablity_array_list():
    test_list = [2,3,4]
    test_type = ImageInt(test_list)
    test_list[0] = 5

    assert (test_list[0]!= test_type.value[0])

#Immutability: Modify original input np.array after instantiation of array data type
def test_immutablity_array_np():
    test_list = np.array([2,3,4])
    test_type = ImageInt(test_list)
    test_list[0] = 5

    assert (test_list[0]!= test_type.value[0])

#Immutability: Modify original input value after instantiation of scalar data type
def test_immutablity_scalar():
    test = 5
    test_type = ValueInt(test)
    test = 7
    
    assert (test != test_type.value)

#Immutability: Modify original numpy type value after instantiation of scalar data type
def test_immutablity_scalar_np():
    test = np.uint8(5)
    test_type = ValueInt(test)
    test = 7
    
    assert (test != test_type.value)

# goes through each member of DataType, checks that the required class variables have been 
# properly set
@pytest.mark.parametrize("enum_member", list(DataType))
def test_all_datatype_classes_have_required_attributes(enum_member):

    
    assert enum_member.data_type is not None, f"'{enum_member.__name__}.data_type' is not defined"
    assert enum_member.data_type == enum_member, f"'{enum_member.__name__}.data_type' ({enum_member.data_type}) does not match Enum member {enum_member}"
    assert enum_member.numpy is not None, f"'{enum_member.__name__}.numpy' is not defined"
    assert enum_member.allowed_sub_types is not None, f"'{enum_member.__name__}.allowed_subdtypes' is not defined"
    assert isinstance(enum_member.is_array, bool), f"'{enum_member.__name__}.is_array' is not boolean"


# test sample data generation
def test_sample_data():
    with pytest.raises(TypeError):
        a = sample_data (int, (2,3))

# shape checks: Input value dtype where is_array = true but no shape passed
    with pytest.raises(TypeError):
        a = sample_data(ImageInt)
        b = sample_data(ImageFloat)

# shape checks: Shape passed, but not as np.array, tuple or list
    with pytest.raises(TypeError):
        a = sample_data(ImageInt,shape = 25)
        b = sample_data(ImageInt,shape = {25,24,1})

# shape checks: Shape passed, but not as array of integers
    with pytest.raises(TypeError):
        a = sample_data(ImageInt,shape = [1.0,2.4])
        b = sample_data(ImageInt,shape = ("2","4","5"))

# shape checks: Shape as np.array, list, tuple
    a = sample_data(ImageInt,[2,4,5])
    b = sample_data(ImageFloat,(2,4,5))

# type checks: Input value of DataType type, output of expected type
    assert (sample_data(ImageInt,[2,3])).data_type == DataType.ImageInt
    assert (sample_data(DataType.ImageFloat,[2,3])).data_type == DataType.ImageFloat
    assert (sample_data(DataType.ValueFloat)).data_type == DataType.ValueFloat
    assert (sample_data(DataType.ArrayInt, (5,4))).data_type == DataType.ArrayInt

#shape checks: For array dtype, does output have expected shape with randomized values
    assert (sample_data(ImageInt,[5,4])).value.shape == (5,4)
    assert (sample_data(ImageFloat,[1,2,3])).value.shape == (1,2,3)
    assert (sample_data(ArrayInt,[1,2,3,4])).value.shape == (1,2,3,4)

#shape checks: For array dtype, does output have expected shape with 0 values
    assert (sample_data(ImageInt,[5,4],zero = True)).value.shape == (5,4)
    assert (sample_data(ImageFloat,[1,2,3],zero = True)).value.shape == (1,2,3)
    assert (sample_data(ArrayInt,[1,2,3,4],zero = True)).value.shape == (1,2,3,4)
    #def sample_data(dtype, shape = None, zero = False):

# value constraint check: For dtype with min, max values, do random values conform to min and max
    a = (sample_data(ImageInt,[200,300,400],zero = True))
    assert a.value.max() <= a.data_type.max_value
    assert a.value.min() >= a.data_type.min_value




