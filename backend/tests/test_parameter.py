import numpy as np
import pytest
from core.parameter import Parameter
from core.constants import DataType

"""|Type constraints|	|	Type Error	| <ul><li>Incorrect type accepted</li></ul>|
|Type constraints|	Input an ImageType without a shape|	Type Error	| <ul><li>Incorrectly shape accepted</li></ul>|"""

# Input data type not a member of DataType.value_type
def test_incorrect_data_type():
    with pytest.raises(TypeError):
        Parameter(name = "Test",
                  dtype = int,
                  value = 5)

    with pytest.raises(TypeError):
        Parameter(name = "Test",
                  dtype = str,
                  value = "5")

    # test correct data type
        Parameter(name = "Test",
                  dtype = DataType.ValueInt,
                  value = 5)

# Input a value that is not of type DataType.dtype.numpy
def test_incompatible_value_type():
    with pytest.raises(TypeError):
        Parameter(name = "Test",
                  dtype = DataType.ValueInt,
                  value = "should be an integer value")

    with pytest.raises(TypeError):
        Parameter(name = "Test",
                  dtype = DataType.ValueFloat,
                  value = "should be a number")    

    # should be np.float64
    with pytest.raises(TypeError):
        Parameter(name = "Test",
                  dtype = DataType.ValueFloat,
                  value = 5.18)    

    Parameter(name = "Test",
        dtype = DataType.ValueFloat,
        value = np.float64(5.2))

    # should be np.uint8
    with pytest.raises(TypeError):
        Parameter(name = "Test",
                  dtype = DataType.ValueInt,
                  value = 5)   

    Parameter(name = "Test",
            dtype = DataType.ValueInt,
            value = np.uint8(4))

    # should be array of np.float64
    with pytest.raises(TypeError):
        Parameter(name = "Test",
                  dtype = DataType.ImageFloat,
                  value = DataType.ImageFloat.numpy(0.18))    

    Parameter(name = "Test",
                  dtype = DataType.ImageFloat,
                  value = DataType.ImageFloat.numpy([0.14,0.16]))  

    # should be array of np.uint8
    with pytest.raises(TypeError):
        Parameter(name = "Test",
                  dtype = DataType.ImageInt,
                  value = DataType.ImageInt.numpy(5))    

    Parameter(name = "Test",
                  dtype = DataType.ImageInt,
                  value = DataType.ImageInt.numpy([0.14,0.16]))  


#Input a value that is of type DataType.dtype
def test_DataType_value_type():
    with pytest.raises(TypeError):
        Parameter(name = "Test",
                  dtype = DataType.ValueInt,
                  value = DataType.ValueInt(5))

    with pytest.raises(TypeError):
        Parameter(name = "Test",
                  dtype = DataType.ImageFloat,
                  value = DataType.ImageFloat([0.2,0.3]))        
        
#Input a shape that is not of class Shape
def test_DataType_shape_type():
    with pytest.raises(TypeError):
        Parameter(name = "Test",
                  dtype = DataType.ImageInt,
                  value = DataType.ImageInt([1,2,3]),
                  shape = (2,1,4,5))
