import numpy as np
import pytest

from core.interface_classes import Port, Connection, Node
from core.image_operation_directory import ImageOperationDirectory
from core.error_handling import ActivationError
from core.image_operation import ImageOperation, ImageParcel, ParameterParcel
from core.constants import DataType
from core.type import sample_data
from core.shape import Shape
import types

"""
Things to test before activation:
* is the node is_ready flag true?
* is the port_id in the correct format ("type.name")
* does the input key referenced by port_name exist in ImageOperation inputs?
* does the input port contain data (pixel_array and mapping for images, value for parameters)?

Things to test after activation:
* is the port_id in the correct format ("type.name")
* does the output key referenced by port_name exist in ImageOperation outputs?
* does ImageOperation output contain data (pixel_array and mapping for images, value for parameters)?

"""

"""initiation"""
# Provide image_operation thats not ImageOperation class
def test_initiation_not_image_operation():
    a = "image_operation"
    with pytest.raises(TypeError, match = "ImageOperation class expected for image_operation"):
        test_node = Node(image_operation = a,
                         node_id = "id")



test_image = ImageParcel(dtype = DataType.ImageInt, 
                            pixel_array = sample_data(dtype = DataType.ImageInt, shape = (1,2,3,4), zero = True, numpy = True),
                            shape = Shape(-1,-1,-1,-1),
                            mapping = Shape(0,1,2,3))
test_parameter = ParameterParcel(dtype = DataType.ValueInt, value = np.uint8(2))
test_operation_1 = ImageOperation(name = "Test Operation 1",
                                    category = "None",
                                    version = None,
                                    docs = None,
                                    alerts = None,
                                    input_image = {"image 1": test_image, "image 2": test_image},
                                    input_parameter = {"parameter 1": test_parameter},
                                    output_image = {"output 1": ImageParcel(dtype = DataType.ImageInt, shape = Shape(-1,-1,-1,-1))}
)
def function1(self):
    self.output_image['output 1'].pixel_array = self.input_image['image 1'].pixel_array

setattr(test_operation_1, 'execute', types.MethodType(function1, test_operation_1))

test_operation_2 = ImageOperation(name = "Test Operation 1",
                                category = "None",
                                version = None,
                                docs = None,
                                alerts = None,
                                input_image = {"image 1": test_image, "image 2": test_image, "image 3": test_image},
                                input_parameter = {"parameter 1": test_parameter, "parameter 2": test_parameter},
                                output_image = {"output 1": ImageParcel(dtype = DataType.ImageInt, shape = Shape(-1,-1,-1,-1))},
                                output_parameter = {"out_param_1": ParameterParcel(dtype=DataType.ValueFloat,value = None),
                                                    "out_param_2": ParameterParcel(dtype=DataType.ValueInt, value = None)}
)
def function2(self):
    self.output_image['output 1'].pixel_array = self.input_image['image 1'].pixel_array
    self.output_parameter["out_param_1"].value = 0.5
    self.output_parameter["out_param_1"].value = 3
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
# Activate node where an input port_id is in an incorrect format (not type.name) | ActivationError | node activates|
# Activate node where an input port_id name does not correctly reference a ImageOperation input_image dictionary key | ActivationError | node activates|
# Activate node where an input port_id name does not correctly reference a ImageOperation input_parameter dictionary key | ActivationError | node activates|
#Activate node where an image input port does not contain pixel_array or mapping | ActivationError | node activates|
# Activate node where a parameter input port does not contain value | ActivationError | node activates|
"""post tests"""
# Activate node where an output port_id is in an incorrect format (not type.name) | ActivationError | node activates|
#Activate node where an output port_id name does not correctly reference a ImageOperation output_image dictionary key | ActivationError | node activates|
# Activate node where an output port_id name does not correctly reference a ImageOperation output_parameter dictionary key | ActivationError | node activates|
#Activate node where an ImageOperation output_image does not contain pixel_array or mapping | ActivationError | node activates|
#Activate node where an ImageOperation output_parameter does not contain value | ActivationError | node activates|