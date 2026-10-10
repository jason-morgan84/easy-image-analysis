import numpy as np
import pytest

from core.interface_classes import Port, Connection, Node
from core.image_operation_directory import ImageOperationDirectory
from core.error_handling import ActivationError
from core.image_operation import ImageOperation
from core.constants import DataType
from core.type import sample_data
from core.shape import Shape
from core.metadata import ImageMetadata, ParameterMetadata
import types

"""
Things to test before activation:
* is the node is_ready flag true?
* is the port_id in the correct format ("type.name")
* does the input key referenced by port_name exist in ImageOperation inputs?
* does the input port contain data (pixel_array and image_map for images, value for parameters)?

Things to test after activation:
* is the port_id in the correct format ("type.name")
* does the output key referenced by port_name exist in ImageOperation outputs?
* does ImageOperation output contain data (pixel_array and image_map for images, value for parameters)?

"""

"""initiation"""
# Provide image_operation thats not ImageOperation class
def test_initiation_not_image_operation():
    a = "image_operation"
    with pytest.raises(TypeError, match = "ImageOperation class expected for image_operation"):
        test_node = Node(image_operation = a,
                         node_id = "id")



test_image_metadata = ImageMetadata(dtype = DataType.ImageInt,
                                    image_shape_constraints= Shape(c=-1, z=-1, y=-1, x=-1),
                                    image_map = Shape(c=0, z=1, y=2, x=3))
test_image = None #Image(sample_data(dtype = DataType.ImageInt, shape = (1,2,3,4)), image_map = Shape(0,1,2,3))
test_parameter_metadata = ParameterMetadata(dtype = DataType.ValueInt)
test_parameter = None #Parameter("test",DataType.ValueInt(2))
test_operation_1 = ImageOperation(name="Test Operation 1",
                                  id="test_operation_1",
                                  category = "None",
                                  version = None,
                                  docs = None,
                                  alerts = None,
                                  input_image_metadata = {"image 1": test_image_metadata, "image 2": test_image_metadata},
                                  input_parameter_metadata = {"parameter 1": test_parameter_metadata},
                                  output_image_metadata = {"output 1": test_image_metadata}
                                  )
def function1(self):
    self.output_image['output 1'].pixel_array = self.input_image['image 1'].pixel_array
    self.output_image['output 1'].image_map = self.input_image['image 1'].image_map

setattr(test_operation_1, 'execute', types.MethodType(function1, test_operation_1))

test_operation_2 = ImageOperation(name = "Test Operation 1",
                                category = "None",
                                id="test_operation_1",
                                version = None,
                                docs = None,
                                alerts = None,
                                input_image_metadata = {"image 1": test_image_metadata, "image 2": test_image_metadata, "image 3": test_image_metadata},
                                input_parameter_metadata = {"parameter 1": test_parameter_metadata, "parameter 2": test_parameter_metadata},
                                output_parameter_metadata= {"out_param_1": ParameterMetadata(dtype=DataType.ValueFloat),
                                                    "out_param_2": ParameterMetadata(dtype=DataType.ValueInt)}
)
def function2(self):
    self.output_image['output 1'].pixel_array = self.input_image['image 1'].pixel_array
    self.output_image['output 1'].image_map = self.input_image['image 1'].image_map
    self.output_parameter["out_param_1"].value = np.float64(0.5)
    self.output_parameter["out_param_2"].value = np.uint8(3)
setattr(test_operation_2, 'execute', types.MethodType(function2, test_operation_2))

# Associate Node with ImageOperations with varying numbers of input_images and input_parameters
# Associate Node with ImageOperations with varying numbers of output_images and output_parameters
def test_initiation_number_inputs():
    test_node1 = Node(test_operation_1,"test 1")
    test_node2 = Node(test_operation_2,"test 2")

    assert len(test_node1.input_ports) == 3
    assert len(test_node1.output_ports) == 1
    assert "image.image 1" in test_node1.input_ports.keys()
    assert "image.image 2" in test_node1.input_ports.keys()
    assert "parameter.parameter 1" in test_node1.input_ports.keys()

    assert len(test_node2.input_ports) == 5
    assert len(test_node2.output_ports) == 3
    assert "image.output 1" in test_node2.output_ports.keys()
    assert "parameter.out_param_1" in test_node2.output_ports.keys()
    assert "parameter.out_param_1" in test_node2.output_ports.keys()

                                


"""pre tests"""
# Activate node where is_ready is false | ActivationError | node activates|
def test_pre_test_is_ready():
    test_node1 = Node(test_operation_1,"test 1")
    test_node1.is_ready = False

    with pytest.raises(ActivationError, match = "node activated when is_ready set to False"):
        test_node1.activate_node()

# Activate node where an input port_id is in an incorrect format (not type.name)
def test_pre_test_incorrect_format_input_port_id():
    test_node1 = Node(test_operation_1,"test 1")
    test_node1.is_ready = True
    test_node1.input_ports["image.image 1"].input_data = test_image
    test_node1.input_ports["image.image 2"].input_data = test_image
    test_node1.input_ports["parameter.parameter 1"].input_data = test_parameter
    test_node1.input_ports["wrong name"] = test_node1.input_ports["image.image 1"]
    del test_node1.input_ports["image.image 1"]
    with pytest.raises(ValueError, match = "invalid port_id for input port"):
        test_node1.activate_node()

# Activate node where an input port_id name does not correctly reference a ImageOperation input_image dictionary key
def test_pre_test_mismatched_input_port_image_id():
    test_node1 = Node(test_operation_1,"test 1")
    test_node1.is_ready = True
    test_node1.input_ports["image.image 1"].input_data = test_image
    test_node1.input_ports["image.image 2"].input_data = test_image
    test_node1.input_ports["parameter.parameter 1"].input_data = test_parameter
    test_node1.input_ports["image.no image"] = test_node1.input_ports["image.image 1"]
    del test_node1.input_ports["image.image 1"]
    with pytest.raises(ActivationError, match = "node activated where input port name not present in ImageOperation input dictionary"):
        test_node1.activate_node()

# Activate node where an input port_id name does not correctly reference a ImageOperation input_parameter dictionary key
def test_pre_test_mismatched_input_port_parameter_id():
    test_node1 = Node(test_operation_1,"test 1")
    test_node1.is_ready = True
    test_node1.input_ports["image.image 1"].input_data = test_image
    test_node1.input_ports["image.image 2"].input_data = test_image
    test_node1.input_ports["parameter.parameter 1"].input_data = test_parameter
    test_node1.input_ports["parameter.no parameter"] = test_node1.input_ports["parameter.parameter 1"]
    del test_node1.input_ports["parameter.parameter 1"]
    with pytest.raises(ActivationError, match = "node activated where input port name not present in ImageOperation input dictionary"):
        test_node1.activate_node()

#Activate node where an image input port does not contain pixel_array
def test_pre_test_missing_pixel_array_input_port_image():
    test_node1 = Node(test_operation_1,"test 1")
    test_node1.is_ready = True
    test_node1.input_ports["image.image 1"].input_data = test_image
    test_node1.input_ports["image.image 2"].input_data = test_image
    test_node1.input_ports["parameter.parameter 1"].input_data = test_parameter

    with pytest.raises(TypeError, match = "Expected Image data type "):
        test_node1.input_ports["image.image 1"].input_data.pixel_array = None
    """planned test commented out here: Port output doesn't exist until Node.activate_node() is run and tries to grab Port.Output, at which point the Output getter
    in port converts the input to an output. This means the only way to set pixel_array to None is to change Port.Input.pixel_array to None, but Port.Input for an
    input_image is an Image class, which won't accept None as as image pixel_array.
    
    This means that an exception is raised in the previous line, setting pixel_array to None, not in the Node class.
    I'm leaving this as a unit test because, if the previous line stops creating an error, the Node test still needs to be run."""
    #with pytest.raises(ActivationError, match = "node activated when input pixel_array not present"):
    #    test_node1.activate_node()

#Activate node where an image input port does not contain image_map
def test_pre_test_missing_image_map_input_port_image():
    test_node1 = Node(test_operation_1,"test 1")
    test_node1.is_ready = True
    test_node1.input_ports["image.image 1"].input_data = test_image
    test_node1.input_ports["image.image 2"].input_data = test_image
    test_node1.input_ports["parameter.parameter 1"].input_data = test_parameter

    with pytest.raises(TypeError, match = "Expected image_map of Shape class"):
        test_node1.input_ports["image.image 1"].input_data.image_map = None
    """as with the previous test, this causes an error in the Image class when setting image_map to 0. Keeping the actual tests for the Node class below
    in case something changes in the Image class down the line"""
    #with pytest.raises(ActivationError, match = "node activated when input image_map not present"):
       # test_node1.activate_node()


# Activate node where a parameter input port does not contain value
def test_pre_test_missing_value_input_port_parameter():
    test_node1 = Node(test_operation_1,"test 1")
    test_node1.is_ready = True
    test_node1.input_ports["image.image 1"].input_data = test_image
    test_node1.input_ports["image.image 2"].input_data = test_image
    test_node1.input_ports["parameter.parameter 1"].input_data = test_parameter

    with pytest.raises(TypeError, match = "Expected type member of DataType"):
        test_node1.input_ports["parameter.parameter 1"].input_data.value = None
    """as with the previous test, this causes an error in the Parameter class when setting value to 0. Keeping the actual tests for the Node class below
    in case something changes in the Image class down the line"""
    #with pytest.raises(ActivationError, match = "node activated when input image_map not present"):
       # test_node1.activate_node()

"""post tests"""
# Activate node where an output port_id is in an incorrect format (not type.name) | ActivationError | node activates|
def test_post_test_incorrect_format_output_port_id():
    test_node1 = Node(test_operation_1,"test 1")
    test_node1.is_ready = True
    test_node1.input_ports["image.image 1"].input_data = test_image
    test_node1.input_ports["image.image 2"].input_data = test_image
    test_node1.input_ports["parameter.parameter 1"].input_data = test_parameter
    test_node1.output_ports["wrong name"] = test_node1.output_ports["image.output 1"]
    del test_node1.output_ports["image.output 1"]
    with pytest.raises(ValueError, match = "invalid port_id for output port"):
        test_node1.activate_node()

#Activate node where an output port_id name does not correctly reference a ImageOperation output_image dictionary key 
def test_post_test_mismatched_output_port_image_id():
    test_node1 = Node(test_operation_1,"test 1")
    test_node1.is_ready = True
    test_node1.input_ports["image.image 1"].input_data = test_image
    test_node1.input_ports["image.image 2"].input_data = test_image
    test_node1.input_ports["parameter.parameter 1"].input_data = test_parameter
    test_node1.output_ports["image.no image"] = test_node1.output_ports["image.output 1"]
    with pytest.raises(ActivationError, match = "node activated where output image port name not present in ImageOperation output dictionary"):
        test_node1.activate_node()

# Activate node where an output port_id name does not correctly reference a ImageOperation output_parameter dictionary key 
def test_post_test_mismatched_output_port_parameter_id():
    test_node2 = Node(test_operation_2,"test 2")
    test_node2.is_ready = True
    test_node2.input_ports["image.image 1"].input_data = test_image
    test_node2.input_ports["image.image 2"].input_data = test_image
    test_node2.input_ports["image.image 3"].input_data = test_image
    test_node2.input_ports["parameter.parameter 1"].input_data = test_parameter
    test_node2.input_ports["parameter.parameter 2"].input_data = test_parameter
    test_node2.output_ports["parameter.no parameter"] = test_node2.output_ports["parameter.out_param_1"]
    with pytest.raises(ActivationError, match = "node activated where output parameter port name not present in ImageOperation output dictionary"):
        test_node2.activate_node()

"""These two unit tests has been removed, because ImageOperation itself will raise an error if this occurs"""
# Activate node where an ImageOperation output_image does not contain pixel_array or image_map
# Activate node where an ImageOperation output_parameter does not contain value | ActivationError | node activates|


"""Data flow through tests"""
# Create node with ImageOperation that passes through same image<br>Input image at relevant input Port input<br>Check output port output. 


test_image_pass_through = ImageOperation(name = "test_image_pass_through",
                                         id="test_image_pass_through",
                                    category = "None",
                                    version = None,
                                    docs = None,
                                    alerts = None,
                                    input_image_metadata= {"image 1": test_image_metadata},
                                    output_image_metadata = {"output 1": test_image_metadata} #Shape(-1,-1,-1,-1))}
)
def image_pass_through(self):
    self.output_image['output 1'].pixel_array = self.input_image['image 1'].pixel_array
    self.output_image['output 1'].image_map = self.input_image['image 1'].image_map

setattr(test_image_pass_through, 'execute', types.MethodType(image_pass_through, test_image_pass_through))

def test_data_flow_image_pass_through():
    pass_through_node = Node(test_image_pass_through,"test_node")
    pass_through_node.input_ports["image.image 1"].input_data = test_image
    pass_through_node.is_ready = True
    pass_through_node.activate_node()

    # assert that expected output port exists
    assert pass_through_node.output_ports["image.output 1"].output_data

    # assert that output port output is an Image class
    #assert isinstance(pass_through_node.output_ports["image.output 1"].output_data, Image)

    # assert that output port output pixel_array is the same data type as input
    assert isinstance(pass_through_node.output_ports["image.output 1"].output_data.pixel_array, type(test_image.pixel_array))

    # assert that output port output pixel_array is the same array shape as input
    assert pass_through_node.output_ports["image.output 1"].output_data.pixel_array.value.shape == test_image.pixel_array.value.shape

    # assert that output port output pixel_array is the same values as input
    assert np.array_equal(pass_through_node.output_ports["image.output 1"].output_data.pixel_array.value, test_image.pixel_array.value)


# Create node with ImageOperation that passes through same parameter<br>Input parameter at relevant input Port input<br>Check output port output. 

test_parameter_pass_through = ImageOperation(name = "test_parameter_pass_through",
                                    category = "None",
                                    id = "test_parameter_pass_through",
                                    version = "1.0.0",
                                    docs = None,
                                    alerts = None,
                                    input_image_metadata = {"image 1": test_image_metadata},
                                    input_parameter_metadata = {"parameter 1": test_parameter_metadata},
                                    output_parameter_metadata = {"out_param_1": ParameterMetadata(dtype=DataType.ValueInt)}
)
def parameter_pass_through(self):
    self.output_parameter['out_param_1'].value = self.input_parameter['parameter 1'].value

setattr(test_parameter_pass_through, 'execute', types.MethodType(parameter_pass_through, test_parameter_pass_through))

def test_data_flow_parameter_pass_through():
    pass_through_node = Node(test_parameter_pass_through,"test_node")
    pass_through_node.input_ports["image.image 1"].input_data = test_image
    pass_through_node.input_ports["parameter.parameter 1"].input_data = test_parameter
    pass_through_node.is_ready = True
    pass_through_node.activate_node()

    # assert that expected output port exists
    assert pass_through_node.output_ports["parameter.out_param_1"].output_data

    # assert that output port output is Parameter class
   # assert isinstance(pass_through_node.output_ports["parameter.out_param_1"].output_data, Parameter)

    # assert that output port output value is the same data type as input
    assert isinstance(pass_through_node.output_ports["parameter.out_param_1"].output_data.value, type(test_parameter.value))

    # assert that output port output value is the same as input
    assert pass_through_node.output_ports["parameter.out_param_1"].output_data.value.value == test_parameter.value.value