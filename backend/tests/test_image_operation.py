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

"""Testing run_code"""
test_code = "import numpy as np\nprint('code running')\n"+\
    "output_image['output'].pixel_array = np.array([1,2,3],np.uint8)"
    

compiled_code = compile(test_code,"<string>","exec")

# Don't supply a value for input_image
def test_run_code_no_input_image():
    test = ImageOperation(name = "Test",
            category = "Testing",
            compiled_code = compiled_code,
            version = None,
            docs = None,
            alerts = None,
            input_image = None,
            input_parameter = None,
            output_image = {"output":ImageParcel(dtype = DataType.ImageInt,pixel_array=None,shape = Shape(-1,-1,-1,-1),mapping = None)},
            output_parameter = None)
    
    with pytest.raises(ValueError) as exc_info:
        test.run_code()

# Try to execute run_code with no compiled_code or compiled code in wrong format (not types.codetype)
def test_run_code_no_code():
    test = ImageOperation(name = "Test",
            category = "Testing",
            compiled_code = None,
            version = None,
            docs = None,
            alerts = None,
            input_image = {"input":ImageParcel(dtype = DataType.ImageInt,pixel_array=np.array([1,2,3],np.uint8),shape = Shape(-1,-1,-1,-1),mapping = Shape(0,0,0,0))},
            input_parameter = None,
            output_image = {"output":ImageParcel(dtype = DataType.ImageInt,pixel_array=None,shape = Shape(-1,-1,-1,-1),mapping = None)},
            output_parameter = None)
    
    with pytest.raises(TypeError) as exc_info:
        test.run_code()
    print(f"{exc_info.value}")
    test.compiled_code = test_code

    with pytest.raises(TypeError) as exc_info:
        test.run_code()

    test.compiled_code = compiled_code
    test.run_code()
    print(f"{exc_info.value}")

# Supply input_image with mising pixel array
def test_run_code_no_input_image_pixel_array():
    test = ImageOperation(name = "Test",
            category = "Testing",
            compiled_code = compiled_code,
            version = None,
            docs = None,
            alerts = None,
            input_image = {"input":ImageParcel(dtype = DataType.ImageInt,pixel_array=None,shape = Shape(-1,-1,-1,-1),mapping = Shape(0,0,0,0))},
            input_parameter = None,
            output_image = {"output":ImageParcel(dtype = DataType.ImageInt,pixel_array=None,shape = Shape(-1,-1,-1,-1),mapping = None)},
            output_parameter = None)
    
    with pytest.raises(ValueError) as exc_info:
        test.run_code() 
    print(f"{exc_info.value}")
# Supply input pixel_array with missing mapping or shape data
def test_run_code_no_input_image_shape_or_mapping():
    test = ImageOperation(name = "Test",
            category = "Testing",
            compiled_code = compiled_code,
            version = None,
            docs = None,
            alerts = None,
            input_image = {"input":ImageParcel(dtype = DataType.ImageInt,pixel_array=np.array([1,2,3],np.uint8),shape = None,mapping = Shape(0,0,0,0))},
            input_parameter = None,
            output_image = {"output":ImageParcel(dtype = DataType.ImageInt,pixel_array=None,shape = Shape(-1,-1,-1,-1),mapping = None)},
            output_parameter = None)
        
    with pytest.raises(ValueError) as exc_info:
        test.run_code() 
    print(f"{exc_info.value}")
    test.input_image["input"].shape = None
    test.input_image["input"].mapping = Shape(0,0,0,0)

    with pytest.raises(ValueError) as exc_info:
        test.run_code() 
    print(f"{exc_info.value}")
# Supply input pixel_array where shape does not match constraints in shape
def test_run_code_input_image_array_not_matching_constraints():
    test = ImageOperation(name = "Test",
            category = "Testing",
            compiled_code = compiled_code,
            version = None,
            docs = None,
            alerts = None,
            input_image = {"input":ImageParcel(dtype = DataType.ImageInt,pixel_array=np.array([1,2,3],np.uint8),shape = Shape(-1,1,-1,-1),mapping = Shape(0,0,0,0))},
            input_parameter = None,
            output_image = {"output":ImageParcel(dtype = DataType.ImageInt,pixel_array=None,shape = Shape(-1,-1,-1,-1),mapping = None)},
            output_parameter = None)
        
    with pytest.raises(ValueError) as exc_info:
        test.run_code() 

    print(f"{exc_info.value}")

# Supply input_parameter with mising value
def test_run_code_input_parameter_missing_value():
    #TODO: DO THIS BIT
    test = ImageOperation(name = "Test",
            category = "Testing",
            compiled_code = compiled_code,
            version = None,
            docs = None,
            alerts = None,
            input_image = {"input":ImageParcel(dtype = DataType.ImageInt,pixel_array=np.array([1,2,3],np.uint8),shape = Shape(-1,1,-1,-1),mapping = Shape(0,0,0,0))},
            input_parameter = None,
            output_image = {"output":ImageParcel(dtype = DataType.ImageInt,pixel_array=None,shape = Shape(-1,-1,-1,-1),mapping = None)},
            output_parameter = None)
        
    with pytest.raises(ValueError) as exc_info:
        test.run_code() 

    print(f"{exc_info.value}")
# Supply parameter array where array does not match defined shape
# Try to run with missing output definitions (shape for images or arrays, dtype for any output) 
# Code provided creates an error
# Code provided doesn't create an output
# Code provided changes inputs
# Code provided returns a pixel_array without mapping data
# Code provided returns a pixel_array with shape that doesn't match mapping and shape constraint data
# Code provided returns an array value without shape data