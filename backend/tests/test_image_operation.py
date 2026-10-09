import pytest
import numpy as np
from core.shape import Shape
from core.constants import DataType
from core.image_operation import ImageOperation
from core.metadata import ImageMetadata, ParameterMetadata
from core.type import sample_data
import types

test_image_operation = ImageOperation(name="Test",
                          id="test",
                          category = "Testing",
                          version = None,
                          docs = None,
                          alerts = None,
                          input_image_metadata={"input1":ImageMetadata(dtype=DataType.ImageInt,
                                                            image_shape_constraints=Shape(c=-1, z=-1, y=-1, x=-1),
                                                            image_map=Shape(c=0, z=1, y=2, x=3))
                                                },
                            )

test_image_metadata = ImageMetadata(dtype=DataType.ImageInt,
                                    image_shape_constraints=Shape(c=-1, z=-1, y=-1, x=-1),
                                    image_map=Shape(c=0, z=1, y=2, x=3)
                                    )

test_parameter_metadata = ParameterMetadata(dtype=DataType.ValueInt)

"""input_image_metadata setter"""
#  create ImageOperation with no input_image_metadata or set input_image_metadata to None
def test_input_image_metadata_setter():
    with pytest.raises(ValueError, match="for ImageOperation, input_metadata is required"):
        ImageOperation(name="Test",
                          id="test",
                          category = "Testing",
                          version = None,
                          docs = None,
                          alerts = None,
                          input_image_metadata = None
                        )
    with pytest.raises(ValueError, match="for ImageOperation, input_metadata is required"):
        test_image_operation.input_image_metadata = None


"""check_set_metadata"""
# send metadata not as dictionary
@pytest.mark.parametrize("test_attribute, attribute_value, message", 
                         [("input_image_metadata",test_image_metadata,"expected input_image_metadata to be dictionary"),
                          ("output_image_metadata",test_image_metadata,"expected output_image_metadata to be dictionary"),
                          ("input_parameter_metadata",test_parameter_metadata,"expected input_parameter_metadata to be dictionary"),
                          ("output_parameter_metadata",test_parameter_metadata,"expected output_parameter_metadata to be dictionary")])
def test_check_set_metadata_input_metadata_not_dictionary(test_attribute, attribute_value, message):
    with pytest.raises(TypeError, match=message):
        setattr(test_image_operation, test_attribute, attribute_value)

# send metadata as dictionary but not of ImageMetadata/ParameterMetadata classes
@pytest.mark.parametrize("test_attribute, attribute_value, message", 
                         [("input_image_metadata",{"input1": "this"},"for metadata input_image_metadata, expected values of type"),
                          ("output_image_metadata",{"output1": "is"},"for metadata output_image_metadata, expected values of type"),
                          ("input_parameter_metadata",{"input2": "not"},"for metadata input_parameter_metadata, expected values of type"),
                          ("output_parameter_metadata",{"output2": "right"},"for metadata output_parameter_metadata, expected values of type")])
def test_check_set_metadata_input_metadata_wrong_type(test_attribute, attribute_value, message):
    with pytest.raises(TypeError, match=message):
        setattr(test_image_operation, test_attribute, attribute_value)

"""test check_set_data function"""
# dictionary sent to function is a dictionary 
@pytest.mark.parametrize("test_attribute, attribute_value, message", 
                         [("input_image",[0,1,2,3],"expected input_image to be dictionary"),
                          ("output_image",[0,1,2,3],"expected output_image to be dictionary"),
                          ("input_parameter",[0,1,2,3],"expected input_parameter to be dictionary"),
                          ("output_parameter",[0,1,2,3],"expected output_parameter to be dictionary")])
def test_check_set_data_input_data_not_dictionary(test_attribute, attribute_value, message):
    with pytest.raises(TypeError, match=message):
        setattr(test_image_operation, test_attribute, attribute_value)

# set data where resepective metadata not present
# (this doesn't work for image_data - the image_data_metadata setter (tested above) requires an input dictionary)
@pytest.mark.parametrize("test_attribute, test_metadata_attribute, attribute_value, message", 
                         [("output_image","output_image_metadata",{"output_image_1":[0,1,2,3]},"output_image present with no meta_data"),
                          ("input_parameter","input_parameter_metadata",{"input_parameter_1":[0,1,2,3]},"input_parameter present with no meta_data"),
                          ("output_parameter","output_parameter_metadata",{"output_parameter_1":[0,1,2,3]},"output_parameter present with no meta_data")])

def test_check_set_data_input_without_meta_data(test_attribute, test_metadata_attribute, attribute_value, message):
    with pytest.raises(ValueError, match=message):
        setattr(test_image_operation, test_metadata_attribute, None)
        setattr(test_image_operation, test_attribute, attribute_value)

# set data where the key in data dictionary is not present in the dictionary of metadata
@pytest.mark.parametrize("test_attribute, test_metadata_attribute, test_metadata_attribute_value, attribute_value, message", 
                         [("input_image","input_image_metadata", {"input_1": test_image_metadata}, {"input_image_1":[0,1,2,3]},"key present in input_image but not in metadata"),
                          ("output_image","output_image_metadata", {"output_1": test_image_metadata}, {"output_image_1":[0,1,2,3]},"key present in output_image but not in metadata"),
                          ("input_parameter","input_parameter_metadata",{"output_2": test_parameter_metadata},{"input_parameter_1":[0,1,2,3]},"key present in input_parameter but not in metadata"),
                          ("output_parameter","output_parameter_metadata",{"output_3": test_parameter_metadata},{"output_parameter_1":[0,1,2,3]},"key present in output_parameter but not in metadata")])

def test_check_set_data_input_without_meta_data_key(test_attribute, test_metadata_attribute, test_metadata_attribute_value, attribute_value, message):
    with pytest.raises(ValueError, match=message):
        setattr(test_image_operation, test_metadata_attribute, test_metadata_attribute_value)
        setattr(test_image_operation, test_attribute, attribute_value)

# set data where the dtype does not match dtype defined in metadata
@pytest.mark.parametrize("test_attribute, test_metadata_attribute, test_metadata_attribute_value, attribute_value, message", 
                         [("input_image","input_image_metadata", {"input_image_1": test_image_metadata}, {"input_image_1":sample_data(DataType.ImageFloat,(1,2,3,4))},"dictionary value of incorrect type: for input_image_1 in input_image"),
                          ("output_image","output_image_metadata", {"output_image_1": test_image_metadata}, {"output_image_1":sample_data(DataType.ImageFloat,(1,2,3,4))},"dictionary value of incorrect type: for output_image_1 in output_image"),
                          ("input_parameter","input_parameter_metadata",{"input_parameter_1": test_parameter_metadata},{"input_parameter_1":np.float64(2)},"dictionary value of incorrect type: for input_parameter_1 in input_parameter"),
                          ("output_parameter","output_parameter_metadata",{"output_parameter_1": test_parameter_metadata},{"output_parameter_1":np.float64(5)},"dictionary value of incorrect type: for output_parameter_1 in output_parameter")])

def test_check_set_data_input_with_incorrect_dtype(test_attribute, test_metadata_attribute, test_metadata_attribute_value, attribute_value, message):
    with pytest.raises(TypeError, match=message):
        setattr(test_image_operation, test_metadata_attribute, test_metadata_attribute_value)
        setattr(test_image_operation, test_attribute, attribute_value)



"""test check_code"""
# Try to execute run_code with no code in execute
def test_run_code_no_code():
  
    with pytest.raises(RuntimeError, match="no code exists") as exc_info:
        test_image_operation.check_code()



"""
# Supply input_image with mising pixel array
def test_run_code_input_image_no_pixel_array():
    test = ImageOperation(name = "Test",
            category = "Testing",
            version = None,
            docs = None,
            alerts = None,
            #input_image = {"input":ImageParcel(dtype = DataType.ImageInt,pixel_array=None,shape = Shape(-1,-1,-1,-1),image_map = Shape(0,0,0,0))},
            input_parameter = None,
            #output_image = {"output":ImageParcel(dtype = DataType.ImageInt,pixel_array=None,shape = Shape(-1,-1,-1,-1),image_map = None)},
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
            #input_image = {"input":ImageParcel(dtype = DataType.ImageInt,pixel_array=np.array([1,2,3],np.uint8),shape = None,image_map = Shape(0,0,0,0))},
            input_parameter = None,
            #output_image = {"output":ImageParcel(dtype = DataType.ImageInt,pixel_array=None,shape = Shape(-1,-1,-1,-1),image_map = None)},
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
            #input_image = {"input":ImageParcel(dtype = DataType.ImageInt,pixel_array=np.array([1,2,3],np.uint8),shape = Shape(-1,1,-1,-1),image_map = Shape(0,0,0,0))},
            input_parameter = None,
            #output_image = {"output":ImageParcel(dtype = DataType.ImageInt,pixel_array=None,shape = Shape(-1,-1,-1,-1),image_map = None)},
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
            #input_image = {"input":ImageParcel(dtype = DataType.ImageInt,pixel_array=np.array([1,2,3],np.uint8),shape = Shape(-1,-1,-1,-1),image_map = Shape(0,0,0,0))},
            #input_parameter = {"input_parameter":ParameterParcel(dtype = DataType.ValueInt,value = None)},
            #output_image = {"output":ImageParcel(dtype = DataType.ImageInt,pixel_array=None,shape = Shape(-1,-1,-1,-1),image_map = None)},
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
            #input_image = {"input":ImageParcel(dtype = DataType.ImageInt,pixel_array=np.array([1,2,3],np.uint8),shape = Shape(-1,-1,-1,-1),image_map = Shape(0,0,0,0))},
            #input_parameter = {"input_parameter":ParameterParcel(dtype = DataType.ArrayInt,value = np.array([[2,5],[2,5]],np.uint8),shape = test_shape)},
            #output_image = {"output":ImageParcel(dtype = DataType.ImageInt,pixel_array=None,shape = Shape(-1,-1,-1,-1),image_map = None)},
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
            #input_image = {"input":ImageParcel(dtype = DataType.ImageInt,pixel_array=np.array([1,2,3],np.uint8),shape = Shape(-1,-1,-1,-1),image_map = Shape(0,0,0,0))},
            input_parameter = None,
            #output_image = {"output":ImageParcel(dtype = DataType.ImageInt,pixel_array=None,shape = None,image_map = None)},
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
            #input_image = {"input":ImageParcel(dtype = DataType.ImageInt,pixel_array=np.array([1,2,3],np.uint8),shape = Shape(-1,-1,-1,-1),image_map = Shape(0,0,0,0))},
            input_parameter = None,
            output_image = None,)
            #output_parameter = {"output":ParameterParcel(dtype = DataType.ValueInt,value=None,shape = None)})

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
            #input_image = {"input":ImageParcel(dtype = DataType.ImageInt,pixel_array=np.array([1,2,3],np.uint8),shape = Shape(-1,-1,-1,-1),image_map = Shape(0,0,0,0))},
            input_parameter = None,
            #output_image = {"output":ImageParcel(dtype = DataType.ImageInt,pixel_array=None,shape = Shape(-1,-1,-1,-1),image_map = None)},
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
            #input_image = {"input":ImageParcel(dtype = DataType.ImageInt,pixel_array=np.array([1,2,3],np.uint8),shape = Shape(-1,-1,-1,-1),image_map = Shape(0,0,0,0))},
            input_parameter = None,
            #output_image = {"output":ImageParcel(dtype = DataType.ImageInt,pixel_array=None,shape = Shape(-1,-1,-1,-1),image_map = None)},
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
            #input_image = {"input":ImageParcel(dtype = DataType.ImageInt,pixel_array=np.array([1,2,3],np.uint8),shape = Shape(-1,-1,-1,-1),image_map = Shape(0,0,0,0))},
            input_parameter = None,
            #output_image = {"output":ImageParcel(dtype = DataType.ImageInt,pixel_array=None,shape = Shape(-1,-1,-1,-1),image_map = None)},
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
            #input_image = {"input":ImageParcel(dtype = DataType.ImageInt,pixel_array=np.array([1,2,3],np.uint8),shape = Shape(-1,-1,-1,-1),image_map = Shape(0,0,0,0))},
            input_parameter = None,
            #output_image = {"output":ImageParcel(dtype = DataType.ImageInt,pixel_array=None,shape = Shape(-1,-1,-1,-1),image_map = None)},
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
            #input_image = {"input":ImageParcel(dtype = DataType.ImageInt,pixel_array=np.array([1,2,3],np.uint8),shape = Shape(-1,-1,-1,-1),image_map = Shape(0,0,0,0))},
            input_parameter = None,
            #output_image = {"output":ImageParcel(dtype = DataType.ImageInt,pixel_array=None,shape = Shape(-1,-1,-1,-1),image_map = None)},
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
            #input_image = {"input":ImageParcel(dtype = DataType.ImageInt,pixel_array=np.array([1,2,3],np.uint8),shape = Shape(-1,-1,-1,-1),image_map = Shape(0,0,0,0))},
            input_parameter = None,)
            #output_image = {"output":ImageParcel(dtype = DataType.ImageInt,pixel_array=None,shape = Shape(-1,-1,-1,-1),image_map = None)},
            #output_parameter = {"output_parameter":ParameterParcel(dtype = DataType.ArrayInt,value = None,shape=None)},)

    def test_function(self):
        self.output_image['output'].pixel_array = np.array([1,2,7],np.uint8)
        self.output_image['output'].image_map = Shape(0,0,0,0)
        self.output_image['output'].shape = Shape(3,3,3,3)
        self.output_parameter['output_parameter'].value = np.array([0,1],np.uint8)
        

    setattr(test, 'execute', types.MethodType(test_function, test))

    with pytest.raises(ValueError, match = 'For parameter output output_parameter, array shape') as exc_info:
        test.run_code() 

    print(f"{exc_info.value}")"""