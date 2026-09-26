from core.interface_classes import Connection, Port
import pytest
from core.error_handling import ConnectionError

# Input not Port class
def test_incorrect_input():
    with pytest.raises(ConnectionError, match = "port class expected as input_port to connection"):
        Connection(connection_id = "test",
                   input_port = "25",
                   output_port = Port(True,"a","b"),
                   input_data=None,
                   output_data=None)

# Output not Port class
def test_incorrect_output():
    with pytest.raises(ConnectionError, match = "port class expected as output_port to connection"):
        Connection(connection_id = "test",
                   input_port = Port(True,"a","b"),
                   output_port = 25,
                   input_data=None,
                   output_data=None)