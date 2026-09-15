import pytest
import numpy as np
from core.image import Image
from core.shape import Shape
from core.constants import DataType
from core.image_operation import ImageOperation, ImageParcel, ParameterParcel


@pytest.mark.parametrize("dtype, pixel_array, shape, mapping", [
    # Supply dtype as not member of DataTypes.image_types
    (np.uint8, np.array([1,2,3],np.uint8), None, None),
    # Have pixel_array type not match dtype
    (DataType.ImageInt, np.array([0.1,0.2,0.3],np.float64), None, None),
    # Supply shape not as Shape class
    (DataType.ImageInt, np.array([1,2,3],np.uint8), [1,2], None),
    # Supply mapping not as Shape class
    (DataType.ImageInt, np.array([1,2,3],np.uint8), None, [5,1])])
def test_ImageParcel(dtype, pixel_array, shape, mapping):

    with pytest.raises(TypeError) as exc_info:
        ImageParcel(dtype = dtype, 
                    pixel_array = pixel_array, 
                    shape = shape, 
                    mapping = mapping)
    print(f"{exc_info.value}")

@pytest.mark.parametrize("dtype, value, shape", [
    # Supply dtype as not member of DataTypes.image_types
    (np.uint8, np.uint8(5), None),
    (DataType.ImageInt, np.uint8(5), None),
    # If array is expected, have value not a list, tuple or ndarray
    (DataType.ArrayFloat, 5, None),
    # Have value type not match dtype
    (DataType.ValueInt, np.float64(5.0), None),
    (DataType.ArrayFloat, np.array([5,2],np.uint8), None)])
def test_ParameterParcel(dtype, value, shape):

    with pytest.raises(TypeError) as exc_info:
        ParameterParcel(dtype = dtype, 
                    value = value, 
                    shape = shape)
    print(f"{exc_info.value}")


def test_check_data():
    with pytest.raises(TypeError)  as exc_info:
        ImageOperation(name = "Test",
                    category = "Testing",
                    compiled_code = None,
                    version = None,
                    docs = None,
                    alerts = None,
                    input_image = ImageParcel(dtype = DataType.ImageInt),
                    input_parameter = None,
                    output_image = None,
                    output_parameter = None)
    print(f"{exc_info.value}")
    with pytest.raises(TypeError)  as exc_info:
        ImageOperation(name = "Test",
                    category = "Testing",
                    compiled_code = None,
                    version = None,
                    docs = None,
                    alerts = None,
                    input_image = ParameterParcel(dtype = DataType.ValueInt),
                    input_parameter = None,
                    output_image = None,
                    output_parameter = None)
    print(f"{exc_info.value}")