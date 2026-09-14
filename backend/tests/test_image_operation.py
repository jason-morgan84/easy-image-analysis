import pytest
import numpy as np
from core.image import Image
from core.shape import Shape
from core.constants import DataType
from core.image_operation import ImageOperation

@pytest.mark.parametrize("image_input, param_input, image_output, param_output", [
    ([1,2,3,4], None, None, None),
    (None, None, [1,2,3,4], None),
    (None, 5, None, None),
    (None, None, None, 5),

])
def test_input_outputs_as_dictionaries(image_input, param_input, image_output, param_output):
    with pytest.raises(TypeError) as exc_info:
        ImageOperation(name = "test",
                       category = "check_image_test",
                       compiled_code = None,
                       version = 0.0,
                       docs = "This is to test check image",
                       input_image = image_input,
                       input_parameter = param_input,
                       output_image = image_output,
                       output_parameter = param_output)
        
    print(f"{exc_info.value}")

"""@pytest.mark.parametrize("image_input, image_output", [
    ({}, None, None, None),
    (None, None, [1,2,3,4], None),

])
def test_images_not_as_correct_dtype(image_input, param_input, image_output, param_output):
    with pytest.raises(TypeError) as exc_info:
        ImageOperation(name = "test",
                       category = "check_image_test",
                       compiled_code = None,
                       version = 0.0,
                       docs = "This is to test check image",
                       input_image = image_input,
                       input_parameter = param_input,
                       output_image = image_output,
                       output_parameter = param_output)
    print(f"{exc_info.value}")"""