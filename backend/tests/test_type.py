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
    test_array = np.array()

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


# test sample data generation

# dtype checks: Input value of non DataType type
def test_sample_data():
    with pytest.raises(TypeError):
        a = sample_data (int, (2,3))

# shape checks: Input value dtype where is_array = true but no shape passed
    with pytest.raises(TypeError):
        a = sample_data(ImageInt)
        b = sample_data(ImageFloat)

        

    assert type(sample_data(DataType.ImageInt,[2,3])) in DataType.types()
    assert isinstance(sample_data(DataType.ImageFloat,[0.2,0.3]), DataType.ImageFloat)
    assert isinstance(sample_data(DataType.ValueFloat), DataType.ValueFloat)
    assert isinstance(sample_data(DataType.ArrayInt, (5,4)), DataType.ArrayInt)

    #def sample_data(dtype, shape = None, zero = False):

