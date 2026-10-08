from core.interface_classes import Connection, Port
import pytest
import numpy as np
from core.error_handling import ConnectionError
from core.constants import DataType
from core.type import sample_data
from core.shape import Shape

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

#Use get_output when source_port contains parameter with no value

def test_get_output_no_value_at_source_port():
    test_connection = Connection(connection_id = "test",
                                 source_port = Port(False,"port","node"),
                                 target_port = Port(True,"port","node"))

    test_connection.source_port.input_data = ParameterParcel(dtype = DataType.ValueInt, value = None )
    """as with previous test, doing source_port.output_data where input_data has no pixel_array or value raises a ConnectionError in
    Port - relevant ConenctionError in Conenction (commented out) never reached"""
    #with pytest.raises(ConnectionError, match = "attempt to get output where source_port.output_data has no data present"):
       # test_connection.output_data
    with pytest.raises(ConnectionError, match = "attempt to get port output where no input present"):
        test_connection.output_data

#Use get_output when source_port contains image with no pixel_array
def test_get_output_no_pixel_array_at_source_port():
    test_connection = Connection(connection_id = "test",
                                 source_port = Port(False,"port","node"),
                                 target_port = Port(True,"port","node"))

    test_connection.source_port.input_data = ImageParcel(dtype = DataType.ImageInt, pixel_array = None, image_map=None )
    """as with previous test, doing source_port.output_data where input_data has no pixel_array or value raises a ConnectionError in
    Port - relevant ConenctionError in Conenction (commented out) never reached"""
    #with pytest.raises(ConnectionError, match = "attempt to get output where source_port.output_data has no data present"):
       # test_connection.output_data
    with pytest.raises(ConnectionError, match = "attempt to get port output where no input present"):
        test_connection.output_data

#Test correct output given with no transpose or convert 
def test_get_output_correct_no_transpose_no_convert():
    test_connection = Connection(connection_id = "test",
                                 source_port = Port(False,"port","node"),
                                 target_port = Port(True,"port","node"))

    test_connection.source_port.input_data = ImageParcel(dtype = DataType.ImageInt, pixel_array = sample_data(DataType.ImageInt,[4,3,2,1],numpy = True), image_map = Shape(0,1,2,3) )

    a = test_connection.output_data
    assert np.array_equal(a.pixel_array.value,test_connection.source_port.input_data.pixel_array)
    assert a.pixel_array.value is not None
#Test correct output given with transpose but no convert
def test_get_output_correct_with_transpose_no_convert():
    test_connection = Connection(connection_id = "test",
                                 source_port = Port(False,"port","node"),
                                 target_port = Port(True,"port","node"),
                                 transpose=Shape(3,2,1,0))

    test_connection.source_port.input_data = ImageParcel(dtype = DataType.ImageInt, pixel_array = sample_data(DataType.ImageInt,[4,3,2,1],numpy = True), image_map = Shape(0,1,2,3) )

    a = test_connection.output_data
    assert a is not None
    assert a.pixel_array.value is not None
    assert a.pixel_array.value.shape == (1,2,3,4)

#Test correct output given with convert but no transpose
def test_get_output_correct_with_convert_no_transpose():
    test_connection = Connection(connection_id = "test",
                                 source_port = Port(False,"port","node"),
                                 target_port = Port(True,"port","node"),
                                 convert = DataType.ImageFloat)

    test_connection.source_port.input_data = ImageParcel(dtype = DataType.ImageInt, pixel_array = sample_data(DataType.ImageInt,[4,3,2,1],numpy = True), image_map = Shape(0,1,2,3) )

    a = test_connection.output_data
    assert a is not None
    assert a.pixel_array.value is not None
    assert a.pixel_array.data_type == DataType.ImageFloat
    #assert a.pixel_array.value.shape == (1,2,3,4)
#Test correct output given with transpose and convert
def test_get_output_correct_with_convert_and_transpose():
    test_connection = Connection(connection_id = "test",
                                 source_port = Port(False,"port","node"),
                                 target_port = Port(True,"port","node"),
                                 convert = DataType.ImageFloat,
                                 transpose=Shape(3,2,1,0))

    test_connection.source_port.input_data = ImageParcel(dtype = DataType.ImageInt, pixel_array = sample_data(DataType.ImageInt,[4,3,2,1],numpy = True), image_map = Shape(0,1,2,3) )

    a = test_connection.output_data
    assert a is not None
    assert a.pixel_array.value is not None
    assert a.pixel_array.data_type == DataType.ImageFloat
    assert a.pixel_array.value.shape == (1,2,3,4)