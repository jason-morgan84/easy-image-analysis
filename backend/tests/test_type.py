import pytest
import numpy as np
from core.constants import DataType
from core.type import ImageInt, ArrayFloat, ImageFloat, ImageBinary, ValueInt, ValueFloat

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

# sends arrays to DataTypes expecting scalars and vice versa
@pytest.mark.parametrize("DataType, invalid_input", [
    (ImageInt, 2), # not an array
    (ArrayFloat, 1), # not an array
    (ValueInt, [1,2]), # unexpected list
    (ValueFloat, np.array([1,2,3])), #unexpected np.array
])
def test_is_array_validation(DataType, invalid_input):
    with pytest.raises(TypeError):
        DataType(invalid_input)

# sends data outside min/max values
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

