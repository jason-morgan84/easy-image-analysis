from core.interface_classes import Connection, Port
import pytest
from core.error_handling import ConnectionError

# Input not Port class
def test_incorrect_input():
    with pytest.raises(ConnectionError, match = "port class expected as input to connection"):
        Connection(25, Port(True, "a", "b"),"Connection1")

# Output not Port class
def test_incorrect_output():
    with pytest.raises(ConnectionError, match = "port class expected as output to connection"):
        Connection(Port(True, "a", "b"),"output","Connection2")