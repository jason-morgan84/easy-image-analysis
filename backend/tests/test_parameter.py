import numpy as np
import pytest
from core.parameter import Parameter
from core.constants import DataType
from core.shape import Shape

"""|Type constraints|	|	Type Error	| <ul><li>Incorrect type accepted</li></ul>|
|Type constraints|	|	Type Error	| <ul><li>Incorrectly shape accepted</li></ul>|"""

# Input data type not a member of DataType.value_type
def test_incorrect_data_type():
    with pytest.raises(TypeError):
        Parameter(name = "Test",
                  value = 5)

    with pytest.raises(TypeError):
        Parameter(name = "Test",
                  value = "5")

    # test correct data type
        Parameter(name = "Test",
                  value = DataType.ValueInt(5))


