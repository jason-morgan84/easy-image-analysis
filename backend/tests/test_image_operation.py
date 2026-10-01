import pytest
import numpy as np
from core.image import Image
from core.shape import Shape
from core.constants import DataType
from core.image_operation import ImageOperation, ImageParcel, ParameterParcel
import types

@pytest.mark.parametrize("dtype, pixel_array, shape, image_map", [
    # Supply dtype as not member of DataTypes.image_types
    (np.uint8, np.array([1,2,3],np.uint8), None, None),
    # Have pixel_array type not match dtype
    (DataType.ImageInt, np.array([0.1,0.2,0.3],np.float64), None, None),
    # Supply shape not as Shape class
    (DataType.ImageInt, np.array([1,2,3],np.uint8), [1,2], None),
    # Supply image_map not as Shape class
    (DataType.ImageInt, np.array([1,2,3],np.uint8), None, [5,1])])
def test_ImageParcel(dtype, pixel_array, shape, image_map):

    with pytest.raises(TypeError) as exc_info:
        ImageParcel(dtype = dtype, 
                    pixel_array = pixel_array, 
                    shape = shape, 
                    image_map = image_map)
    print(f"{exc_info.value}")

@pytest.mark.parametrize("dtype, value, shape", [
    # Supply dtype as not member of DataTypes.image_types
    (np.uint8, np.uint8(5), None),
    (DataType.ImageInt, np.uint8(5), None),
    # If array is expected, have value not a list, tuple or ndarray
    (DataType.ArrayFloat, 5, None),
    # If array is not expected, have value as array
    (DataType.ValueInt,[1,2],None),
    # Have value type not match dtype
    (DataType.ValueInt, np.float64(5.0), None),
    (DataType.ArrayFloat, np.array([5,2],np.uint8), None)])
def test_ParameterParcel(dtype, value, shape):

    with pytest.raises(TypeError) as exc_info:
        ParameterParcel(dtype = dtype, 
                    value = value, 
                    shape = shape)
    print(f"{exc_info.value}")

#ImageParcel Imutability - Pass value as variable then change variable
def test_ImageParcel_imutability():
        array = np.array([1,2,3],np.uint8)
        shape_test = Shape(-1,-1,-1,-1)
        image_map_test = Shape(0,0,0,0)
        test = ImageParcel(dtype = DataType.ImageInt, 
                    pixel_array = array, 
                    shape = shape_test, 
                    image_map = image_map_test)
        
        shape_test.c = 4
        image_map_test.z = 5
        array[0] = 5
        assert test.pixel_array[0] != 5
        assert test.image_map.z != 5, print(f"image_map values: {image_map_test.c} {test.image_map.c}")
        assert test.shape.c != 4, print(f"shape values: {shape_test.c} {test.shape.c}")
        
#ParameterParcel Imutability - Pass value as variable then change variable
def test_ParameterParcel_imutability():
        array = np.array([1,2,3],np.uint8)
        shape_test = np.array([3],np.uint8)
        test = ParameterParcel(dtype = DataType.ArrayInt, 
                    value = array, 
                    shape = shape_test)
        
        shape_test[0] = 4
        array[0] = 5
        print(f"value: {test.shape}")
        assert test.value[0] != 5
        assert test.shape[0] != 4, print(f"value: {shape_test}")

# test check data function
# pass input_image not as dictionary
def test_check_data_input_image_not_dictionary():

    with pytest.raises(TypeError, match = "Expected input_image to be dictionary" ):
        ImageOperation(name = "Test",
                    category = "Testing",
                    version = None,
                    docs = None,
                    alerts = None,
                    input_image = ImageParcel(dtype = DataType.ImageInt),
                    input_parameter = None,
                    output_image = None,
                    output_parameter = None)

# pass input_image as dictionary of wrong class
def test_check_data_input_image_dictionary_wrong_class():
    with pytest.raises(TypeError, match = "Expected input_image to be dictionary of"):
        ImageOperation(name = "Test",
                    category = "Testing",
                    version = None,
                    docs = None,
                    alerts = None,
                    input_image = {"input": ParameterParcel(dtype = DataType.ValueInt)},
                    input_parameter = None,
                    output_image = None,
                    output_parameter = None)

# Don't supply a value for input_image
def test_run_code_no_input_image():
    test = ImageOperation(name = "Test",
            category = "Testing",
            version = None,
            docs = None,
            alerts = None,
            input_image = None,
            input_parameter = None,
            output_image = {"output":ImageParcel(dtype = DataType.ImageInt,pixel_array=None,shape = Shape(-1,-1,-1,-1),image_map = None)},
            output_parameter = None)

    def test_function(self):
        self.output_image['output'].pixel_array = np.array([1,2,7],np.uint8)
        self.output_image['output'].image_map = Shape(0,0,0,0)
        self.output_image['output'].shape = Shape(3,3,3,3)

    setattr(test, 'execute', types.MethodType(test_function, test))
    
    with pytest.raises(ValueError,match='input_image expected, got none') as exc_info:
        test.run_code()

# Try to execute run_code with no compiled_code or compiled code in wrong format (not types.codetype)
def test_run_code_no_code():
    test = ImageOperation(name = "Test",
            category = "Testing",
            version = None,
            docs = None,
            alerts = None,
            input_image = {"input":ImageParcel(dtype = DataType.ImageInt,pixel_array=np.array([1,2,3],np.uint8),shape = Shape(-1,-1,-1,-1),image_map = Shape(0,0,0,0))},
            input_parameter = None,
            output_image = {"output":ImageParcel(dtype = DataType.ImageInt,pixel_array=None,shape = Shape(-1,-1,-1,-1),image_map = None)},
            output_parameter = None)
    
    with pytest.raises(RuntimeError, match="no code exists") as exc_info:
        test.run_code()


# Supply input_image with mising pixel array
def test_run_code_input_image_no_pixel_array():
    test = ImageOperation(name = "Test",
            category = "Testing",
            version = None,
            docs = None,
            alerts = None,
            input_image = {"input":ImageParcel(dtype = DataType.ImageInt,pixel_array=None,shape = Shape(-1,-1,-1,-1),image_map = Shape(0,0,0,0))},
            input_parameter = None,
            output_image = {"output":ImageParcel(dtype = DataType.ImageInt,pixel_array=None,shape = Shape(-1,-1,-1,-1),image_map = None)},
            output_parameter = None)

    def test_function(self):
        self.output_image['output'].pixel_array = np.array([1,2,7],np.uint8)
        self.output_image['output'].image_map = Shape(0,0,0,0)
        self.output_image['output'].shape = Shape(3,3,3,3)

    setattr(test, 'execute', types.MethodType(test_function, test))
    
    with pytest.raises(ValueError, match='No image pixel array given') as exc_info:
        test.run_code() 
    print(f"{exc_info.value}")

# Supply input pixel_array with missing image_map or shape data
def test_run_code_input_image_no_shape_or_image_map():
    test = ImageOperation(name = "Test",
            category = "Testing",
            version = None,
            docs = None,
            alerts = None,
            input_image = {"input":ImageParcel(dtype = DataType.ImageInt,pixel_array=np.array([1,2,3],np.uint8),shape = None,image_map = Shape(0,0,0,0))},
            input_parameter = None,
            output_image = {"output":ImageParcel(dtype = DataType.ImageInt,pixel_array=None,shape = Shape(-1,-1,-1,-1),image_map = None)},
            output_parameter = None)
        
    def test_function(self):
        self.output_image['output'].pixel_array = np.array([1,2,7],np.uint8)
        self.output_image['output'].image_map = Shape(0,0,0,0)
        self.output_image['output'].shape = Shape(3,3,3,3)

    setattr(test, 'execute', types.MethodType(test_function, test))
    test.input_image["input"].shape = None
    test.input_image["input"].image_map = Shape(0,0,0,0)

    with pytest.raises(ValueError) as exc_info:
        test.run_code() 

    print(f"{exc_info.value}")
# Supply input pixel_array where shape does not match constraints in shape
def test_run_code_input_image_array_not_matching_constraints():
    test = ImageOperation(name = "Test",
            category = "Testing",
            version = None,
            docs = None,
            alerts = None,
            input_image = {"input":ImageParcel(dtype = DataType.ImageInt,pixel_array=np.array([1,2,3],np.uint8),shape = Shape(-1,1,-1,-1),image_map = Shape(0,0,0,0))},
            input_parameter = None,
            output_image = {"output":ImageParcel(dtype = DataType.ImageInt,pixel_array=None,shape = Shape(-1,-1,-1,-1),image_map = None)},
            output_parameter = None)

    def test_function(self):
        self.output_image['output'].pixel_array = np.array([1,2,7],np.uint8)
        self.output_image['output'].image_map = Shape(0,0,0,0)
        self.output_image['output'].shape = Shape(3,3,3,3)

    setattr(test, 'execute', types.MethodType(test_function, test))
    with pytest.raises(ValueError) as exc_info:
        test.run_code() 

    print(f"{exc_info.value}")

# Supply input_parameter with mising value
def test_run_code_input_parameter_missing_value():
    test = ImageOperation(name = "Test",
            category = "Testing",
            version = None,
            docs = None,
            alerts = None,
            input_image = {"input":ImageParcel(dtype = DataType.ImageInt,pixel_array=np.array([1,2,3],np.uint8),shape = Shape(-1,-1,-1,-1),image_map = Shape(0,0,0,0))},
            input_parameter = {"input_parameter":ParameterParcel(dtype = DataType.ValueInt,value = None)},
            output_image = {"output":ImageParcel(dtype = DataType.ImageInt,pixel_array=None,shape = Shape(-1,-1,-1,-1),image_map = None)},
            output_parameter = None)

    def test_function(self):
        self.output_image['output'].pixel_array = np.array([1,2,7],np.uint8)
        self.output_image['output'].image_map = Shape(0,0,0,0)
        self.output_image['output'].shape = Shape(3,3,3,3)

    setattr(test, 'execute', types.MethodType(test_function, test))
        
    with pytest.raises(ValueError) as exc_info:
        test.run_code() 

    print(f"{exc_info.value}")
# Supply parameter array where array does not match defined shape
@pytest.mark.parametrize("test_shape", [None,(2,1)])
    
def test_run_code_input_parameter_wrong_shape(test_shape):
    test = ImageOperation(name = "Test",
            category = "Testing",
            version = None,
            docs = None,
            alerts = None,
            input_image = {"input":ImageParcel(dtype = DataType.ImageInt,pixel_array=np.array([1,2,3],np.uint8),shape = Shape(-1,-1,-1,-1),image_map = Shape(0,0,0,0))},
            input_parameter = {"input_parameter":ParameterParcel(dtype = DataType.ArrayInt,value = np.array([[2,5],[2,5]],np.uint8),shape = test_shape)},
            output_image = {"output":ImageParcel(dtype = DataType.ImageInt,pixel_array=None,shape = Shape(-1,-1,-1,-1),image_map = None)},
            output_parameter = None)

    def test_function(self):
        self.output_image['output'].pixel_array = np.array([1,2,7],np.uint8)
        self.output_image['output'].image_map = Shape(0,0,0,0)
        self.output_image['output'].shape = Shape(-1,-1,-1,-1)

    setattr(test, 'execute', types.MethodType(test_function, test))
    
    with pytest.raises(ValueError, match= "For parameter input ") as exc_info:
        test.run_code() 

    print(f"{exc_info.value}")
# Try to run with missing output definitions (shape for images or arrays, dtype for any output) 

def test_run_code_output_image_missing_definitions():
    test = ImageOperation(name = "Test",
            category = "Testing",
            version = None,
            docs = None,
            alerts = None,
            input_image = {"input":ImageParcel(dtype = DataType.ImageInt,pixel_array=np.array([1,2,3],np.uint8),shape = Shape(-1,-1,-1,-1),image_map = Shape(0,0,0,0))},
            input_parameter = None,
            output_image = {"output":ImageParcel(dtype = DataType.ImageInt,pixel_array=None,shape = None,image_map = None)},
            output_parameter = None)

    def test_function(self):
        self.output_image['output'].pixel_array = np.array([1,2,7],np.uint8)
        self.output_image['output'].image_map = Shape(0,0,0,0)
        self.output_image['output'].shape = Shape(-1,-1,-1,-1)

    setattr(test, 'execute', types.MethodType(test_function, test))

    with pytest.raises(ValueError, match = 'expected image shape') as exc_info:
        test.run_code() 

    print(f"{exc_info.value}")

def test_run_code_output_no_image():
    test = ImageOperation(name = "Test",
            category = "Testing",
            version = None,
            docs = None,
            alerts = None,
            input_image = {"input":ImageParcel(dtype = DataType.ImageInt,pixel_array=np.array([1,2,3],np.uint8),shape = Shape(-1,-1,-1,-1),image_map = Shape(0,0,0,0))},
            input_parameter = None,
            output_image = None,
            output_parameter = {"output":ParameterParcel(dtype = DataType.ValueInt,value=None,shape = None)})

    def test_function(self):
        self.output_parameter['output'].value = np.uint8(5)

    setattr(test, 'execute', types.MethodType(test_function, test))

    test.run_code() 

    #print(f"{exc_info.value}")


# Code provided creates an error
def test_run_code_broken_code():
    test = ImageOperation(name = "Test",
            category = "Testing",
            version = None,
            docs = None,
            alerts = None,
            input_image = {"input":ImageParcel(dtype = DataType.ImageInt,pixel_array=np.array([1,2,3],np.uint8),shape = Shape(-1,-1,-1,-1),image_map = Shape(0,0,0,0))},
            input_parameter = None,
            output_image = {"output":ImageParcel(dtype = DataType.ImageInt,pixel_array=None,shape = Shape(-1,-1,-1,-1),image_map = None)},
            output_parameter = None)

    def test_function(self):
        self.output_image['no_key'].pixel_array = np.array([1,2,3],np.uint8)

    setattr(test, 'execute', types.MethodType(test_function, test))

    with pytest.raises(RuntimeError, match = 'error executing operation') as exc_info:
        test.run_code() 

    print(f"{exc_info.value}")

# Code provided doesn't create an output
def test_run_code_no_output():
    test = ImageOperation(name = "Test",
            category = "Testing",
            version = None,
            docs = None,
            alerts = None,
            input_image = {"input":ImageParcel(dtype = DataType.ImageInt,pixel_array=np.array([1,2,3],np.uint8),shape = Shape(-1,-1,-1,-1),image_map = Shape(0,0,0,0))},
            input_parameter = None,
            output_image = {"output":ImageParcel(dtype = DataType.ImageInt,pixel_array=None,shape = Shape(-1,-1,-1,-1),image_map = None)},
            output_parameter = None)

    def test_function(self):
        a = 25 + 1

    setattr(test, 'execute', types.MethodType(test_function, test))

    with pytest.raises(ValueError, match = 'No image pixel array given for output') as exc_info:
        test.run_code() 

    print(f"{exc_info.value}")

# Code provided changes inputs
def test_run_code_alters_input():

    test = ImageOperation(name = "Test",
            category = "Testing",
            version = None,
            docs = None,
            alerts = None,
            input_image = {"input":ImageParcel(dtype = DataType.ImageInt,pixel_array=np.array([1,2,3],np.uint8),shape = Shape(-1,-1,-1,-1),image_map = Shape(0,0,0,0))},
            input_parameter = None,
            output_image = {"output":ImageParcel(dtype = DataType.ImageInt,pixel_array=None,shape = Shape(-1,-1,-1,-1),image_map = None)},
            output_parameter = None)

    
    def test_function(self):
        self.output_image['output'].pixel_array = np.array([1,2,7],np.uint8)
        self.output_image['output'].image_map = Shape(0,0,0,0)
        self.output_image['output'].shape = Shape(3,3,3,3)
        self.input_image['input'].pixel_array = np.array([1,2,7],np.uint8)
        

    setattr(test, 'execute', types.MethodType(test_function, test))

    with pytest.raises(RuntimeError, match = 'operation altered input') as exc_info:
        test.run_code() 

    print(f"{exc_info.value}")
# Code provided returns a pixel_array without image_map data

def test_run_code_output_image_no_map():
    test = ImageOperation(name = "Test",
            category = "Testing",
            version = None,
            docs = None,
            alerts = None,
            input_image = {"input":ImageParcel(dtype = DataType.ImageInt,pixel_array=np.array([1,2,3],np.uint8),shape = Shape(-1,-1,-1,-1),image_map = Shape(0,0,0,0))},
            input_parameter = None,
            output_image = {"output":ImageParcel(dtype = DataType.ImageInt,pixel_array=None,shape = Shape(-1,-1,-1,-1),image_map = None)},
            output_parameter = None)
    
    def test_function(self):
        self.output_image['output'].pixel_array = np.array([1,2,7],np.uint8)
        self.output_image['output'].shape = Shape(3,3,3,3)
        

    setattr(test, 'execute', types.MethodType(test_function, test))

    with pytest.raises(ValueError, match = 'No image image_map data given for output output') as exc_info:
        test.run_code() 

    print(f"{exc_info.value}")

# Code provided returns a pixel_array with shape that doesn't match image_map and shape constraint data
def test_run_code_output_image_no_matching_shape():
    test = ImageOperation(name = "Test",
            category = "Testing",
            version = None,
            docs = None,
            alerts = None,
            input_image = {"input":ImageParcel(dtype = DataType.ImageInt,pixel_array=np.array([1,2,3],np.uint8),shape = Shape(-1,-1,-1,-1),image_map = Shape(0,0,0,0))},
            input_parameter = None,
            output_image = {"output":ImageParcel(dtype = DataType.ImageInt,pixel_array=None,shape = Shape(-1,-1,-1,-1),image_map = None)},
            output_parameter = None)

    def test_function(self):
        self.output_image['output'].pixel_array = np.array([1,2,7],np.uint8)
        self.output_image['output'].image_map = Shape(0,0,0,0)
        self.output_image['output'].shape = Shape(1,1,1,1)
        

    setattr(test, 'execute', types.MethodType(test_function, test))

    with pytest.raises(ValueError, match = 'For output image output, pixel_array') as exc_info:
        test.run_code() 

    print(f"{exc_info.value}")


# Code provided returns an array value without shape data
def test_run_code_parameter_array_no_matching_shape():
    test = ImageOperation(name = "Test",
            category = "Testing",
            version = None,
            docs = None,
            alerts = None,
            input_image = {"input":ImageParcel(dtype = DataType.ImageInt,pixel_array=np.array([1,2,3],np.uint8),shape = Shape(-1,-1,-1,-1),image_map = Shape(0,0,0,0))},
            input_parameter = None,
            output_image = {"output":ImageParcel(dtype = DataType.ImageInt,pixel_array=None,shape = Shape(-1,-1,-1,-1),image_map = None)},
            output_parameter = {"output_parameter":ParameterParcel(dtype = DataType.ArrayInt,value = None,shape=None)},)

    def test_function(self):
        self.output_image['output'].pixel_array = np.array([1,2,7],np.uint8)
        self.output_image['output'].image_map = Shape(0,0,0,0)
        self.output_image['output'].shape = Shape(3,3,3,3)
        self.output_parameter['output_parameter'].value = np.array([0,1],np.uint8)
        

    setattr(test, 'execute', types.MethodType(test_function, test))

    with pytest.raises(ValueError, match = 'For parameter output output_parameter, array shape') as exc_info:
        test.run_code() 

    print(f"{exc_info.value}")