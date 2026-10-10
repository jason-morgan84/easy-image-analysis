from core.interface_classes import Connection, Port
import pytest
import numpy as np
from core.metadata import ParameterMetadata
from core.error_handling import ConnectionError
from core.constants import DataType
from core.type import sample_data
from core.shape import Shape

sample_meta_data = ParameterMetadata(dtype=DataType.ValueInt)
# Input not Port class
def test_incorrect_input():
    with pytest.raises(ConnectionError, match = "port class expected as source for connection"):
        Connection(connection_id = "test",
                   source_port = "25",
                   target_port = Port(is_input=True, port_id="a", node_id="b", meta_data=sample_meta_data))

# Output not Port class
def test_incorrect_output():
    with pytest.raises(ConnectionError, match = "port class expected as target for connection"):
        Connection(connection_id = "test",
                   source_port = Port(is_input=True, port_id="a", node_id="b", meta_data=sample_meta_data),
                   target_port = 25)

# tranpose not shape class
def test_transpose_not_shape():
    with pytest.raises(TypeError, match = "shape class expected for transpose"):
        Connection(connection_id = "test",
                   source_port = Port(is_input=True, port_id="a", node_id="b", meta_data=sample_meta_data),
                   target_port = Port(is_input=True, port_id="a", node_id="b", meta_data=sample_meta_data),
                   transpose = [1,2,3,4])

# convert not type
def test_convert_not_type():
    with pytest.raises(TypeError, match = "datatype class expected for transpose"):
        Connection(connection_id = "test",
                   source_port = Port(is_input=True, port_id="a", node_id="b", meta_data=sample_meta_data),
                   target_port = Port(is_input=True, port_id="a", node_id="b", meta_data=sample_meta_data),
                   convert = "test")
        
