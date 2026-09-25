import numpy as np
import pytest
from core.parameter import Parameter
from core.image_operation import ImageParcel, ParameterParcel
from core.constants import DataType
from core.shape import Shape
from core.port import Port
from core.image import Image
from core.type import sample_data

# provide missing input flag
def test_incorrect_input_flag():
    with pytest.raises(TypeError,match = "expected type bool for is_node_input flag, got"):
        Port(is_node_input = None,
             image_operation_ID = None)

# Provide incorrect image data (ImageParcel - numpy) data to Node flagged as node_input	
# Provide incorrect parameter data (ParameterParcel - numpy) to Node flagged as node_input
# Provide incorrect image data (Image of DataType) to Node flagged as !node_input	
# Provide incorrect paramter data (Parameter of DataType) to Node flagged as !node_input
@pytest.mark.parametrize("is_input, value, message", [
    (True, ImageParcel(dtype = DataType.ImageInt,
                       pixel_array = np.ndarray([1,2,3,4],np.uint8),
                       mapping = Shape(0,0,0,0)),
                    "Expected input of Image or Parameter class, got"),
    (True, ParameterParcel(dtype = DataType.ValueInt,
                           value = np.uint8(2)),
                    "Expected input of Image or Parameter class, got"),
    (False, Image(pixel_array = sample_data(DataType.ImageInt,(1,2,3,4)),
                  image_map = Shape(0,0,0,0)),
                    "Expected input of ImageParcel or ParameterParcel class"),
    (False, Parameter(name = "Test",
                      value = DataType.ValueInt(2)),
                    "Expected input of ImageParcel or ParameterParcel class")
    ])

def test_incorrect_data_type(is_input, value, message):
    with pytest.raises(TypeError,match = message):
        test_port = Port(is_input,None)
        test_port.input = value
        print(test_port.output())

# Provide correct (ImageParcel - numpy) image data to Node flagged as !node_input
# Provide correct (ImageParameter - numpy) parameter data to Node flagged as !node_input
# Provide correct (Image - DataType) image data to Node flagged as node_input
# Provide correct (Parameter - DataType) parameter data to Node flagged as node_input
@pytest.mark.parametrize("is_input, value", [
    (False, ImageParcel(dtype = DataType.ImageInt,
                       pixel_array = np.ndarray([1,2,3,4],np.uint8),
                       mapping = Shape(0,0,0,0))),
    (False, ParameterParcel(dtype = DataType.ValueInt,
                           value = np.uint8(2))),
    (True, Image(pixel_array = sample_data(DataType.ImageInt,(1,2,3,4)),
                  image_map = Shape(0,0,0,0))),
    (True, Parameter(name = "Test",
                      value = DataType.ValueInt(2)))
    ])

def test_correct_data_type(is_input, value):
        test_port = Port(is_input, None)
        test_port.input = value
        print(test_port.output)