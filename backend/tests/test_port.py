import pytest
import numpy as np
from core.constants import DataType
from core.shape import Shape
from core.interface_classes import Port
from core.type import sample_data
from core.metadata import ParameterMetadata, ImageMetadata

"""port_id setter"""
# create port without port_id - ValueError: "port_id required for port instantiation"
def test_port_without_port_id():
    with pytest.raises(ValueError, match = "port_id required for port instantiation"):
        Port(port_id=None,
             node_id="node_id",
             is_input=False,
             meta_data=ImageMetadata(DataType.ImageInt,Shape(c = -1, z = -1, y = -1, x = -1),Shape(c = 0, z = 0, y = 0, x = 0)))

"""node_id setter"""
# create port without node_id - ValueError: "node_id required for port instantiation" 
def test_port_without_node_id():
    with pytest.raises(ValueError, match = "node_id required for port instantiation"):
        Port(port_id="port_id", 
             node_id=None,
             is_input=False,
             meta_data=ImageMetadata(DataType.ImageInt,Shape(c = -1, z = -1, y = -1, x = -1),Shape(c = 0, z = 0, y = 0, x = 0)))

"""is_input flag setter"""
# create port without is_input flag
def test_port_without_is_input():
    with pytest.raises(ValueError, match = "is_input flag not set for port"):
        Port(port_id="port_id", 
             node_id="node_id",
             is_input=None,
             meta_data=ImageMetadata(DataType.ImageInt,Shape(c = -1, z = -1, y = -1, x = -1),Shape(c = 0, z = 0, y = 0, x = 0)))
        
# create port where is_input flag is not boolean
def test_port_is_input_not_bool():
    with pytest.raises(TypeError, match = "is_input flag expected boolean"):
        Port(port_id="port_id", 
             node_id="node_id",
             is_input="input",
             meta_data=ImageMetadata(DataType.ImageInt,Shape(c = -1, z = -1, y = -1, x = -1),Shape(c = 0, z = 0, y = 0, x = 0)))
        
"""metadata setter"""
# Pass in value that is not ImageMetadata or ParameterMetadata class - TypeError: "meta data expected as ImageMetadata or ParameterMetadata class" 
def test_port_without_metadata():
    with pytest.raises(TypeError, match = "meta data expected as ImageMetadata or ParameterMetadata clas"):
        Port(port_id="port_id",
             node_id="node_ide",
              is_input=True,
              meta_data=None)

"""data setter"""
# For scalar data, pass in data that is not of type metadata.dtype.numpy | TypeError: data passed to port with unexpected dtype; for port {self.port_id} expected {self.metadata.dtype.numpy}
def test_unexpected_scalar_data():

    test_port = Port (port_id = "test",
                      node_id = "test",
                      is_input=True,
                      meta_data = ParameterMetadata(dtype = DataType.ValueInt))
    with pytest.raises(TypeError, match = "data passed to port with unexpected dtype; for port test expected <class 'numpy.uint8'>"):
        test_port.data = 25

# For image or array data, pass in data that is not of type np.ndarray | TypeError: data passed to port with unexpected dtype; for port {self.port_id} expected np.ndarray
def test_unexpected_array_not_array():

    test_port = Port (port_id = "test",
                      node_id = "test",
                      is_input=True,
                      meta_data = ImageMetadata(dtype = DataType.ImageInt,
                                                image_map = Shape(c = 0, z = 1, y = 2, x = 3),
                                                image_shape_constraints = Shape(c = -1, z = -1, y = -1, x = -1)))
    with pytest.raises(TypeError, match = "data passed to port with unexpected dtype; for port test expected np.ndarray"):
        test_port.data = 25

# For image or array data, pass in data that is not a ndarray of type metadata.dtype | TypeError: data passed to port with unexpected dtype; for port {self.port_id} expected {self.metadata.dtype.numpy}
def test_unexpected_array_incorrect_dtype():

    test_port = Port (port_id = "test",
                      node_id = "test",
                      is_input=False,
                      meta_data = ImageMetadata(dtype = DataType.ImageInt,
                                                image_map = Shape(c = 0, z = 1, y = 2, x = 3),
                                                image_shape_constraints = Shape(c = -1, z = -1, y = -1, x = -1)))
    with pytest.raises(TypeError, match = "data passed to port with unexpected dtype; for port test expected <class 'numpy.uint8'>"):
        test_port.data = np.array([0.1,0.2,0.3],np.float64)

# For image data, pass in a Shape arguement that is not present in Shape.dimensions* | AttributeError: dimension present in Shape.dimensions that is not a Shape arguement 
# (this error should be impossible to generate given current structure of Shape, it will give an error from Shape class instead. Leave in case of future changes to Shape class)
def test_incorrect_shape_arguement():
    with pytest.raises(AttributeError, match = "Shape class instantiated with unexpected arguement: 't'"):
        test_port = Port (port_id = "test",
                        node_id = "test",
                        is_input=False,
                        meta_data = ImageMetadata(dtype = DataType.ImageInt,
                                                    image_map = Shape(c = 0, z = 1, y = 2, x = 3, t = 5),
                                                    image_shape_constraints = Shape(c = -1, z = -1, y = -1, x = -1)))  
    """commented out: this is the error that would be raised by Port class, but it gets caught earlier by Shape class - keeping in case Shape class changes potentially break this"""
    #with pytest.raises(AttributeError, match = "dimension present in Shape.dimensions that is not a Shape arguement"):
    #    test_port = Port (port_id = "test",
    #                    node_id = "test",
    #                    meta_data = ImageMetadata(dtype = DataType.ImageInt,
    #                                                image_map = Shape(t = 0, z = 1, y = 2, x = 3),
    #                                                image_shape_constraints = Shape(c = -1, z = -1, y = -1, x = -1)))
    



# For image data, pass in data that doesn't match metadata.image_shape_constraints and metadata.image_map | ValueError: image_type passed to port with incorrect shape 
def test_image_incorrect_shape():

    test_port = Port (port_id = "test",
                      node_id = "test",
                      is_input=True,
                      meta_data = ImageMetadata(dtype = DataType.ImageInt,
                                                image_map = Shape(c = 0, z = 1, y = 2, x = 3),
                                                image_shape_constraints = Shape(c = 1, z = -1, y = -1, x = -1)))
    with pytest.raises(ValueError, match = "image_type passed to port with incorrect shape"):
        test_port.data = sample_data(DataType.ImageInt, shape = (2,3,1,4), numpy = True)

# For array data, pass in data that doesn't match metadata.shape | ValueError: array_type data passed to port with incorrect shape
def test_array_incorrect_shape():

    test_port = Port (port_id = "test",
                      node_id = "test",
                      is_input=True,
                      meta_data = ParameterMetadata(dtype = DataType.ArrayInt,
                                                shape = (1,2)))
    with pytest.raises(ValueError, match = "array_type data passed to port with incorrect shape"):
        test_port.data = np.array([0,1,2],DataType.ArrayInt.numpy)

# Pass in data where metadata.dtype does not define dtype from DataTypes** | TypeError: port MetaData defines unexpected dtype
# (this error should also be impossible to generate given current structure of Metadata classes, wil give an error from ImageMetadata or ParameterMetadata instead)
def test_incorrect_metadata_dtype():
    with pytest.raises(TypeError, match = "expected type from DataType.image_type, got: <class 'int'>"):
        test_port = Port (port_id = "test",
                        node_id = "test",
                        is_input=True,
                        meta_data = ImageMetadata(dtype = int,
                                                    image_map = Shape(c = 0, z = 1, y = 2, x = 3),
                                                    image_shape_constraints = Shape(c = 1, z = -1, y = -1, x = -1)))
        
    with pytest.raises(TypeError, match = "expected type from DataType.value_type or DataType.array_type, got: <class 'int'>"):
        test_port = Port (port_id = "test",
                        node_id = "test",
                        is_input=True,
                        meta_data = ParameterMetadata(dtype = int))
    """commented out: this error will only appear if something changes in ImageMetadata class that stops it picking up an incorrect dtype on instantiation, which should never happen"""
    #with pytest.raises(TypeError, match = "port MetaData defines unexpected dtype"):
    #    test_port = Port (port_id = "test",
    #                    node_id = "test",
    #                    meta_data = ImageMetadata(dtype = int,
    #                                                image_map = Shape(c = 0, z = 1, y = 2, x = 3),
    #                                                image_shape_constraints = Shape(c = 1, z = -1, y = -1, x = -1)))



