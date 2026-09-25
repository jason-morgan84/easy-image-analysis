import numpy as np
import pytest
from core.parameter import Parameter
from core.constants import DataType
from core.shape import Shape

"""|Type constraints|	|	Type Error	| <ul><li>Incorrect type accepted</li></ul>|
|Type constraints|	|	Type Error	| <ul><li>Incorrectly shape accepted</li></ul>|"""

# Input data type not a member of DataType.value_type
@pytest.mark.parametrize("value, message", [
    # Supply dtype as not member of DataTypes.image_types
    (5, "Expected type member of DataType"),
    # Have pixel_array type not match dtype
    ("5", "Expected type member of DataType"),
    (DataType.ImageInt([1,2,3],), "Expected type member of DataType.value_types")])

def test_incorrect_data_type(value, message):
    with pytest.raises(TypeError,match = message):
        Parameter(name = "Test",
                  value = value)

def test_correct_data_type():
    # test correct data type
        Parameter(name = "Test",
                  value = DataType.ValueInt(5))


