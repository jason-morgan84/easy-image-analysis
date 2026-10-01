from core.interface_classes import Connection, Port
import pytest
from core.error_handling import ConnectionError

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