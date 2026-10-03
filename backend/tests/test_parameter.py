import numpy as np
import pytest
from core.parameter import Parameter
from core.constants import DataType
from core.shape import Shape

"""|Type constraints|	|	Type Error	| <ul><li>Incorrect type accepted</li></ul>|
|Type constraints|	|	Type Error	| <ul><li>Incorrectly shape accepted</li></ul>|"""

# Input data type not a member of DataType.value_type
@pytest.mark.parametrize("value, message", [
    (5, "Expected type member of DataType"),
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

"""test Parameter.convert()"""
# convert arguement for array_type not in array_type class
def test_convert_wrong_array_arguement():
    test = Parameter(name = "Test",
                value = DataType.ArrayInt([1,2,3,]))
    with pytest.raises(TypeError,match = "arrays can only be converted to array_types"):
            test.convert(DataType.ImageFloat)

# convert arguement for value_type not in value_type class 
def test_convert_wrong_value_arguement():
        test = Parameter(name = "Test",
                  value = DataType.ValueInt(1))
        with pytest.raises(TypeError,match = "values can only be converted to value_types"):
              test.convert(DataType.ImageFloat)

# convert test parameter
def test_convert():

    test = Parameter(name = "Test",
                    value = DataType.ValueInt(5))

    test.convert(DataType.ValueFloat)
    
    assert test.value.data_type == DataType.ValueFloat
