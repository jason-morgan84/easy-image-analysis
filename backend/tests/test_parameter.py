import numpy as np
import pytest
from core.parameter import Parameter
from core.constants import DataType

"""|Type constraints|	Input value in a format not defined in data_type|	Type Error	| <ul><li>Incorrectly type data used in incorrect format</li></ul>|
|Type constraints|	Input data type not a member of DataType.value_type|	Type Error	| <ul><li>Incorrect type accepted</li></ul>|"""


def test_incorrect_data_type():
    with pytest.raises(TypeError):
        Parameter("Test",int,"Slider")

    with pytest.raises(TypeError):
        Parameter("Test",str,"Slider")

    # test correct data type
    Parameter("Test2",DataType.ValueInt,"test",2)


def test_incompatible_value_type():
    with pytest.raises(TypeError):
        Parameter("Test",DataType.ValueInt,"test","should be an integer value")

    with pytest.raises(TypeError):
        Parameter("Test",DataType.ValueFloat,"test","should be a number")    

    with pytest.raises(TypeError):
        Parameter("Test",DataType.ValueInt,"test",5.18)    

    
        
