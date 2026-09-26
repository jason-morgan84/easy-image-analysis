import numpy as np
import pytest
from core.parameter import Parameter
from core.image_operation import ImageParcel, ParameterParcel, ImageOperation
from core.constants import DataType
from core.shape import Shape
from core.interface_classes import Port, Connection
from core.image import Image
from core.type import sample_data

# provide missing input flag
def test_incorrect_input_flag():
    with pytest.raises(TypeError,match = "expected type bool for is_input flag, got"):
        Port(is_input = None,
             port_id = None,
             node_id = None)


# Provide incorrect image data (Image of DataType) to Node flagged as !node_input	
# Provide incorrect paramter data (Parameter of DataType) to Node flagged as !node_input
@pytest.mark.parametrize("is_input, value, message", [
    (False, Image(pixel_array = sample_data(DataType.ImageInt,(1,2,3,4)),
                  image_map = Shape(0,0,0,0)),
                    "for an output port, expected input_connection as ImageOpeartion class"),
    (False, Parameter(name = "Test",
                      value = DataType.ValueInt(2)),
                    "for an output port, expected input_connection as ImageOpeartion class")
    ])

def test_output_port_incorrect_data_type(is_input, value, message):
    with pytest.raises(TypeError,match = message):
        test_port = Port(is_input, node_id = "no_node", port_id = "test_port")
        test_port._input_data = value
        print(test_port.output())

# Provide incorrect image data (ImageParcel - numpy) data to Node flagged as node_input	
# Provide incorrect parameter data (ParameterParcel - numpy) to Node flagged as node_input
def test_input_port_incorrect_data_type():
    preceeding_port = Port(is_input = False,
                           port_id = "preceeding port",
                           node_id = "preceeding_node")

    preceeding_port.output = ImageParcel(dtype = DataType.ImageInt, 
                                         pixel_array = np.ndarray([1,2,3,4],np.uint8), 
                                         mapping = Shape(0,0,0,0))
    
    preceeding_connection = Connection(connection_id = "ID", 
                                       input_port = preceeding_port, 
                                       output_port = preceeding_port,
                                       input_data = preceeding_port.output,
                                       output_data = preceeding_port.output)
    
    with pytest.raises(TypeError, match = "Expected input of Image or Parameter class"):
        test_port = Port(is_input = True, node_id = "no_node", port_id = "test_port", input_connection = preceeding_connection, output_connection = ImageOperation("Test","Test","0.1.0",None,None))
        test_port.input_data = preceeding_port.output
        print(test_port.output_data())

        preceeding_port.output = ParameterParcel(dtype = DataType.ValueInt,
                                                 value = np.uint8(2))
         
    with pytest.raises(TypeError, match = "Expected input of Image or Parameter class"):
        test_port = Port(is_input = True, node_id = "no_node", port_id = "test_port", input_connection = preceeding_connection, output_connection = ImageOperation("Test","Test","0.1.0",None,None))
        test_port.input_data = preceeding_port.output
        print(test_port.output_data())


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
        test_port = Port(is_input = is_input, 
                         node_id = None,
                         port_id = None)
        test_port.input_data = value
        print(test_port.output_data)


