from core.interface_classes import Connection, Port
import pytest
from core.error_handling import ConnectionError
from core.image_operation import ParameterParcel, ImageParcel
from core.constants import DataType

# Input not Port class
def test_incorrect_input():
    with pytest.raises(ConnectionError, match = "port class expected as source for connection"):
        Connection(connection_id = "test",
                   source_port = "25",
                   target_port = Port(True,"a","b"))

# Output not Port class
def test_incorrect_output():
    with pytest.raises(ConnectionError, match = "port class expected as target for connection"):
        Connection(connection_id = "test",
                   source_port = Port(True,"a","b"),
                   target_port = 25)

# tranpose not shape class
def test_transpose_not_shape():
    with pytest.raises(TypeError, match = "shape class expected for transpose"):
        Connection(connection_id = "test",
                   source_port = Port(True,"a","b"),
                   target_port = Port(True,"a","b"),
                   transpose = [1,2,3,4])

# convert not type
def test_convert_not_type():
    with pytest.raises(TypeError, match = "datatype class expected for transpose"):
        Connection(connection_id = "test",
                   source_port = Port(True,"a","b"),
                   target_port = Port(True,"a","b"),
                   convert = "test")
        
"""test get_output"""
#Use get_output when no data at source_port

def test_get_output_no_data_at_source_port():
    test_connection = Connection(connection_id = "test",
                                 source_port = Port(True,"a","b"),
                                 target_port = Port(True,"a","b"))

    test_connection.source_port.output_data = None
    """top test commented out: attempted to get data from a port where none is present raises a ConnectionError in the port
    commented out test matches error message from connection if port is changed to break this"""
    #with pytest.raises(ConnectionError, match = "attempt to get output where source_port.output_data has no data present"):
       # test_connection.output_data
    with pytest.raises(ConnectionError, match = "attempt to get port output where no input present"):
        test_connection.output_data
#Use get_output when source_port contains image with no pixel_array
def test_get_output_no_value_at_source_port():
    test_connection = Connection(connection_id = "test",
                                 source_port = Port(False,"port","node"),
                                 target_port = Port(True,"port","node"))

    test_connection.source_port.input_data = ParameterParcel(dtype = DataType.ValueInt, value = None )
    """top test commented out: attempted to get data from a port where none is present raises a ConnectionError in the port
    commented out test matches error message from connection if port is changed to break this"""
    #with pytest.raises(ConnectionError, match = "attempt to get output where source_port.output_data has no data present"):
       # test_connection.output_data
    #TODO: THERE IS NO INPUT DATA CHECKER ON PORT. THIS MEANS output_data NEEDS TO CHECK THERES A VALUE OR PIXEL_ARRAY PRESENT BEFORE TRYING TO CONVERT IT
    with pytest.raises(ConnectionError, match = "attempt to get port output where no input present"):
        test_connection.output_data
#Use get_output when source_port contains parameter with no value
#Test correct output given with no transpose or convert 
#Test correct output given with transpose but no convert
#Test correct output given with convert but no transpose
#Test correct output given with transpose and convert