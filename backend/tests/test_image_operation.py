import pytest
import numpy as np
from core.shape import Shape
from core.constants import DataType
from core.image_operation import ImageOperation
from core.metadata import ImageMetadata, ParameterMetadata
from core.type import sample_data
import types
import copy


test_image_metadata_imageint = ImageMetadata(dtype=DataType.ImageInt,
                                    image_shape_constraints=Shape(c=-1, z=-1, y=-1, x=-1),
                                    image_map=Shape(c=0, z=1, y=2, x=3)
                                    )

test_parameter_metadata_valueint = ParameterMetadata(dtype=DataType.ValueInt)
test_parameter_metadata_arrayint = ParameterMetadata(dtype=DataType.ArrayInt, shape=(1,2))

test_image_data_imageint = sample_data(DataType.ImageInt,(1,2,3,4))
test_image_data_imagefloat = sample_data(DataType.ImageFloat,(1,2,3,4))
test_parameter_data_valueint = sample_data(DataType.ValueInt)
test_parameter_data_valuefloat = sample_data(DataType.ValueFloat)

"""input_image_metadata setter"""
#  create ImageOperation with no input_image_metadata or set input_image_metadata to None
def test_input_image_metadata_setter_no_metadata():
    with pytest.raises(ValueError, match="for ImageOperation, input_metadata is required"):
        ImageOperation(name="Test",
                          id="test",
                          category = "Testing",
                          version = None,
                          docs = None,
                          alerts = None,
                          input_image_metadata = None
                        )

    test_image_operation = ImageOperation(name="Test",
                        id="test",
                        category = "Testing",
                        version = None,
                        docs = None,
                        alerts = None,
                        input_image_metadata={"input1":test_image_metadata_imageint},
                        )
    with pytest.raises(ValueError, match="for ImageOperation, input_metadata is required"):
        test_image_operation.input_image_metadata = None

"""all metadata setters"""
# create ImageOperation with incorrect input_image_metadata
@pytest.mark.parametrize("attribute, metadata, message", 
                         [
                            ("input_image_metadata","not a dictionary","expected 'input_image_metadata' to be dictionary"),
                            ("input_image_metadata",{"dictionary not": "right class"},"for metadata dictionary 'input_image_metadata', expected values of type"),
                            ("output_image_metadata","not a dictionary","expected 'output_image_metadata' to be dictionary"),
                            ("output_image_metadata",{"dictionary not": "right class"},"for metadata dictionary 'output_image_metadata', expected values of type"),
                            ("input_parameter_metadata","not a dictionary","expected 'input_parameter_metadata' to be dictionary"),
                            ("input_parameter_metadata",{"dictionary not": "right class"},"for metadata dictionary 'input_parameter_metadata', expected values of type"),
                            ("output_parameter_metadata","not a dictionary","expected 'output_parameter_metadata' to be dictionary"),
                            ("output_parameter_metadata",{"dictionary not": "right class"},"for metadata dictionary 'output_parameter_metadata', expected values of type"),
                            ])

def test_metadata_setters_wrong_metadata(attribute,metadata, message):

    test_image_operation = ImageOperation(name="Test",
                    id="test",
                    category = "Testing",
                    version = None,
                    docs = None,
                    alerts = None,
                    input_image_metadata={"input1":test_image_metadata_imageint},
                    )
    with pytest.raises(TypeError, match=message):
        setattr(test_image_operation,attribute,metadata)

"""all data setters"""
# pass data to ImageOperation not as a dictionary
@pytest.mark.parametrize("data_attribute, data, metadata_attribute, metadata, message", 
                         [
                             ("input_image",test_image_data_imageint,"input_image_metadata",{"input1": test_image_metadata_imageint},"expected 'input_image' to be dictionary"),
                             ("output_image",test_image_data_imageint,"output_image_metadata",{"output1": test_image_metadata_imageint},"expected 'output_image' to be dictionary" ),
                             ("input_parameter",test_parameter_data_valueint,"input_parameter_metadata",{"input2":test_parameter_metadata_valueint},"expected 'input_parameter' to be dictionary"),
                             ("output_parameter",test_parameter_data_valueint,"output_parameter_metadata",{"output2":test_parameter_metadata_valueint},"expected 'output_parameter' to be dictionary")
                         ])
def test_data_setters_not_dictionary(data_attribute, data, metadata_attribute, metadata, message):
    test_image_operation = ImageOperation(name="Test",
                id="test",
                category = "Testing",
                version = None,
                docs = None,
                alerts = None,
                input_image_metadata={"input1":test_image_metadata_imageint})
    setattr(test_image_operation,metadata_attribute,metadata)
    with pytest.raises(TypeError,match = message):
        setattr(test_image_operation,data_attribute,data)

# pass data to ImageOperation as a dictionary with missing metadata (except input_image where input_image_metadata is required)
# pass data to ImageOperation as a dictionary with key that doesn't match metadata
@pytest.mark.parametrize("data_attribute, data, metadata_attribute, metadata, message", 
                         [
                             ("input_image",{"input_1": test_image_data_imageint},"input_image_metadata",{"input1": test_image_metadata_imageint},"key present in data dictionary 'input_image' but not in metadata: 'input_1'"),
                             ("output_image",{"output_1": test_image_data_imageint},"output_image_metadata",None,"data present with no metadata: 'output_image'" ),
                             ("output_image",{"output_1": test_image_data_imageint},"output_image_metadata",{"output1": test_image_metadata_imageint},"key present in data dictionary 'output_image' but not in metadata: 'output_1'" ),
                             ("input_parameter",{"input_2":test_parameter_data_valueint},"input_parameter_metadata",None,"data present with no metadata: 'input_parameter'"),
                             ("input_parameter",{"input_2":test_parameter_data_valueint},"input_parameter_metadata",{"input2":test_parameter_metadata_valueint},"key present in data dictionary 'input_parameter' but not in metadata: 'input_2'"),
                             ("output_parameter",{"output_2":test_parameter_data_valueint},"output_parameter_metadata",None,"data present with no metadata: 'output_parameter'"),
                             ("output_parameter",{"output_2":test_parameter_data_valueint},"output_parameter_metadata",{"output2":test_parameter_metadata_valueint},"key present in data dictionary 'output_parameter' but not in metadata: 'output_2'")

                         ])
def test_data_setters_incorrect_data(data_attribute, data, metadata_attribute, metadata, message):
    test_image_operation = ImageOperation(name="Test",
            id="test",
            category = "Testing",
            version = None,
            docs = None,
            alerts = None,
            input_image_metadata={"input1":test_image_metadata_imageint})
    setattr(test_image_operation,metadata_attribute,metadata)
    with pytest.raises(ValueError,match = message):
        setattr(test_image_operation,data_attribute,data)

"""test reset_input"""
def test_reset_input():
    test_image_operation = ImageOperation(name="Test",
            id="test",
            category = "Testing",
            version = None,
            docs = None,
            alerts = None,
            input_image_metadata={"input1":test_image_metadata_imageint},
            input_parameter_metadata = {"input2":test_parameter_metadata_valueint},
            input_image = {"input1":test_image_data_imageint},
            input_parameter = {"input2":test_parameter_data_valueint}
            )
    
    test_image_operation.reset_input()
    assert test_image_operation.input_image == None
    assert test_image_operation.input_parameter == None

"""test reset_output"""
def test_reset_output():
    test_image_operation = ImageOperation(name="Test",
        id="test",
        category = "Testing",
        version = None,
        docs = None,
        alerts = None,
        input_image_metadata={"input1":test_image_metadata_imageint},
        input_parameter_metadata = {"input2":test_parameter_metadata_valueint},
        output_parameter_metadata = {"input2":test_parameter_metadata_valueint},
        output_parameter = {"input2":test_parameter_data_valueint},
        output_image_metadata = {"input1": test_image_metadata_imageint},
        output_image = {"input1":test_image_data_imageint},

        )

    test_image_operation.reset_output()
    assert test_image_operation.output_image == None
    assert test_image_operation.output_parameter == None

"""test check_code"""

def test_check_code():
    test_image_operation = ImageOperation(name="Test",
        id="test",
        category = "Testing",
        version = None,
        docs = None,
        alerts = None,
        input_image_metadata={"input1":test_image_metadata_imageint})
    
    with pytest.raises(RuntimeError, match="no code exists"):
        test_image_operation.check_code()
    test_image_operation.execute = None
    with pytest.raises(RuntimeError, match="no code exists"):
        test_image_operation.check_code()

def function_for_testing(self):
    self.output_image={"output": np.array([1,2,7],np.uint8)}

"""test run_code"""
# Try to execute run_code with no code in execute
def test_run_code_no_code():
    test_image_operation = ImageOperation(name="Test",
        id="test",
        category = "Testing",
        version = None,
        docs = None,
        alerts = None,
        input_image_metadata={"input1":test_image_metadata_imageint})
    with pytest.raises(RuntimeError, match="no code exists"):
        test_image_operation.run_code()

# run_code with no input_image
def test_run_code_no_input_image():
    test_image_operation = ImageOperation(name="Test",
        id="test",
        category = "Testing",
        version = None,
        docs = None,
        alerts = None,
        input_image_metadata={"input1":test_image_metadata_imageint})
    
    setattr(test_image_operation, "execute", types.MethodType(function_for_testing, test_image_operation))
    with pytest.raises(ValueError, match="metadata present with no data: 'input_image'"):
        test_image_operation.run_code()

#run_code with input_parameter_metadata but no input_parameter
def test_run_code_input_parameter_metadata_no_data():
    test_image_operation = ImageOperation(name="Test",
        id="test",
        category = "Testing",
        version = None,
        docs = None,
        alerts = None,
        input_image_metadata={"input1":test_image_metadata_imageint},
        input_image = {"input1":test_image_data_imageint},
        input_parameter_metadata={"input2": test_parameter_metadata_valueint}
        )
    setattr(test_image_operation, "execute", types.MethodType(function_for_testing, test_image_operation))
    with pytest.raises(ValueError, match="metadata present with no data: 'input_parameter'"):
        test_image_operation.run_code()

#run_code with input_parameter but not input_parameter_metadata
def test_run_code_input_parameter_data_no_metadata():
    test_image_operation = ImageOperation(name="Test",
        id="test",
        category = "Testing",
        version = None,
        docs = None,
        alerts = None,
        input_image_metadata={"input1":test_image_metadata_imageint},
        input_image = {"input1":test_image_data_imageint},
        input_parameter_metadata={"input2": test_parameter_metadata_valueint},
        input_parameter = {"input2": test_parameter_data_valueint}
        )
    
    setattr(test_image_operation, "execute", types.MethodType(function_for_testing, test_image_operation))
    setattr(test_image_operation,"input_parameter_metadata",None)
    with pytest.raises(ValueError, match="data present with no metadata: 'input_parameter'"):
        test_image_operation.run_code()
        
#run_code where input_image_data type doesn't match input_image_metadata
def test_run_code_input_image_data_wrong_type():
    test_image_operation = ImageOperation(name="Test",
        id="test",
        category = "Testing",
        version = None,
        docs = None,
        alerts = None,
        input_image_metadata={"input1":test_image_metadata_imageint},
        input_image = {"input1":test_image_data_imageint},
        input_parameter_metadata={"input2": test_parameter_metadata_valueint},
        input_parameter = {"input2": test_parameter_data_valueint}
        )
    
    setattr(test_image_operation, "execute", types.MethodType(function_for_testing, test_image_operation))

    setattr(test_image_operation,"input_image",{"input1":test_image_data_imagefloat})
    with pytest.raises(TypeError, match="dictionary value of incorrect type"):
        test_image_operation.run_code()

#run_code where input_image shape deosn't match input_image_metadata
def test_run_code_input_image_data_wrong_shape():

    test_image_operation = ImageOperation(name="Test",
        id="test",
        category = "Testing",
        version = None,
        docs = None,
        alerts = None,
        input_image_metadata={"input1":ImageMetadata(dtype=DataType.ImageInt,
                                    image_shape_constraints=Shape(c=-1, z=-1, y=-1, x=-1),
                                    image_map=Shape(c=0, z=1, y=2, x=3)
                                    )},
        input_image = {"input1":test_image_data_imageint},
        input_parameter_metadata={"input2": test_parameter_metadata_valueint},
        input_parameter = {"input2": test_parameter_data_valueint}
        )
    setattr(test_image_operation, "execute", types.MethodType(function_for_testing, test_image_operation))
    # set input_image to have input1 where c = 1
    setattr(test_image_operation,"input_image",{"input1":sample_data(DataType.ImageInt,(1,2,3,4))})
    # set input_image_metadata to have shape constraints for input1 as c = 2
    test_image_operation.input_image_metadata["input1"].image_shape_constraints.c = 2
    with pytest.raises(ValueError, match="image shape does not match metadata"):
        test_image_operation.run_code()

#run_code where input_parameter_data type doesn't match input_parameter_metadata
def test_run_code_input_parameter_data_wrong_type():
    test_image_operation = ImageOperation(name="Test",
        id="test",
        category = "Testing",
        version = None,
        docs = None,
        alerts = None,
        input_image_metadata={"input1":test_image_metadata_imageint},
        input_image = {"input1":test_image_data_imageint},
        input_parameter_metadata={"input2": test_parameter_metadata_valueint},
        input_parameter = {"input2": test_parameter_data_valuefloat}
        )

    setattr(test_image_operation, "execute", types.MethodType(function_for_testing, test_image_operation))
    with pytest.raises(TypeError, match="dictionary value of incorrect type"):
        test_image_operation.run_code()

#run_code where input_parameter_data shape doesn't match input_parameter_metadata
def test_run_code_input_parameter_wrong_shape():
    test_image_operation = ImageOperation(name="Test",
        id="test",
        category = "Testing",
        version = None,
        docs = None,
        alerts = None,
        input_image_metadata={"input1":test_image_metadata_imageint},
        input_image = {"input1":test_image_data_imageint},
        input_parameter_metadata={"input2":ParameterMetadata(dtype=DataType.ArrayInt, shape=(1,2))},
        input_parameter = {"input2":sample_data(dtype = DataType.ArrayInt, shape = (2,1))}
        )
    setattr(test_image_operation, "execute", types.MethodType(function_for_testing, test_image_operation))

    with pytest.raises(ValueError, match="array shape does not match shape metadata"):
        test_image_operation.run_code()

#run_code with no output metadata
def test_run_code_no_output_metadata():
    test_image_operation = ImageOperation(name="Test",
        id="test",
        category = "Testing",
        version = None,
        docs = None,
        alerts = None,
        input_image_metadata={"input1":test_image_metadata_imageint},
        input_image = {"input1":test_image_data_imageint},
        )
    setattr(test_image_operation, "execute", types.MethodType(function_for_testing, test_image_operation))
    setattr(test_image_operation,"output_parameter_metadata",None)
    setattr(test_image_operation,"output_image_metadata",None)
    with pytest.raises(RuntimeError, match="no defined outputs present for ImageOperation"):
        test_image_operation.run_code()

#run_code with existing output data and check it changes
def test_run_code_change_in_output():
    def function_no_change_to_output(self):
        self.output_image = {"output1": self.input_image["input1"].copy()}
        self.output_image["output1"][0][0][0][0] = 15

    test_image_operation = ImageOperation(name="Test",
        id="test",
        category = "Testing",
        version = None,
        docs = None,
        alerts = None,
        input_image_metadata={"input1":test_image_metadata_imageint},
        input_image = {"input1":test_image_data_imageint},
        output_image_metadata={"output1":test_image_metadata_imageint}
        )
    setattr(test_image_operation, "execute", types.MethodType(function_no_change_to_output, test_image_operation))
    setattr(test_image_operation,"output_image",{"output1":test_image_data_imageint})

    test_image_operation.output_image["output1"][0][0][0][0] = 25

    test_image_operation.run_code()

    assert test_image_operation.output_image["output1"][0][0][0][0] == 15


#Code provided creates an error
def test_run_code_error_in_code():
    def function_creates_error(self):
        a = 1
        b = 0
        print(a/b)

    test_image_operation = ImageOperation(name="Test",
        id="test",
        category = "Testing",
        version = None,
        docs = None,
        alerts = None,
        input_image_metadata={"input1":test_image_metadata_imageint},
        input_image = {"input1":test_image_data_imageint},
        output_image_metadata={"output1":test_image_metadata_imageint}
        )
    setattr(test_image_operation, "execute", types.MethodType(function_creates_error, test_image_operation))
    
    with pytest.raises(RuntimeError, match="error executing operation 'Test': division by zero"):
        test_image_operation.run_code()

#Code provided doesn't create an output
def test_run_code_no_output():
    def function_no_change_to_output(self):
        print("Nothing changes here")

    test_image_operation = ImageOperation(name="Test",
        id="test",
        category = "Testing",
        version = None,
        docs = None,
        alerts = None,
        input_image_metadata={"input1":test_image_metadata_imageint},
        input_image = {"input1":test_image_data_imageint},
        output_image_metadata={"output1":test_image_metadata_imageint}
        )
    setattr(test_image_operation, "execute", types.MethodType(function_no_change_to_output, test_image_operation))

    with pytest.raises(RuntimeError, match="operation did not generate an output"):
        test_image_operation.run_code()

#Code provided changes inputs
def test_run_code_changes_input_image():
    def function_no_change_to_output(self):
        self.output_image = {"output1": self.input_image["input1"].copy()}
        self.input_image["input1"][0][0][0][0] += 1
        
    test_image_operation = ImageOperation(name="Test",
        id="test",
        category = "Testing",
        version = None,
        docs = None,
        alerts = None,
        input_image_metadata={"input1":test_image_metadata_imageint},
        input_image = {"input1":test_image_data_imageint},
        output_image_metadata={"output1":test_image_metadata_imageint}
        )
    setattr(test_image_operation, "execute", types.MethodType(function_no_change_to_output, test_image_operation))

    with pytest.raises(RuntimeError,match="operation altered input values "):
        test_image_operation.run_code()

def test_run_code_changes_input_parameter_value():
    def function_no_change_to_output(self):
        self.output_image = {"output1": self.input_image["input1"].copy()}
        self.input_parameter["input2"] += 1

    test_image_operation = ImageOperation(name="Test",
        id="test",
        category = "Testing",
        version = None,
        docs = None,
        alerts = None,
        input_image_metadata={"input1":test_image_metadata_imageint},
        input_image = {"input1":test_image_data_imageint},
        output_image_metadata={"output1":test_image_metadata_imageint},
        input_parameter_metadata={"input2":test_parameter_metadata_valueint},
        input_parameter={"input2":test_parameter_data_valueint}
        )
    setattr(test_image_operation, "execute", types.MethodType(function_no_change_to_output, test_image_operation))

    with pytest.raises(RuntimeError,match="operation altered input values "):
        test_image_operation.run_code()

def test_run_code_changes_input_parameter_array():
    def function_no_change_to_output(self):
        self.output_image = {"output1": self.input_image["input1"].copy()}
        self.input_parameter["input2"][0][0] += 1

    test_image_operation = ImageOperation(name="Test",
        id="test",
        category = "Testing",
        version = None,
        docs = None,
        alerts = None,
        input_image_metadata={"input1":test_image_metadata_imageint},
        input_image = {"input1":test_image_data_imageint},
        output_image_metadata={"output1":test_image_metadata_imageint},
        input_parameter_metadata={"input2":test_parameter_metadata_arrayint},
        input_parameter={"input2":sample_data(dtype = DataType.ArrayInt, shape=(1,2))}
        )
    setattr(test_image_operation, "execute", types.MethodType(function_no_change_to_output, test_image_operation))

    with pytest.raises(RuntimeError,match="operation altered input values "):
        test_image_operation.run_code()

#Code provided returns an image with type that doesn't match metadata
def test_run_code_image_output_wrong_type():
    def function_no_change_to_output(self):
        self.output_image = {"output1": sample_data(dtype=DataType.ImageFloat, shape=(1,2,3,4))}

    test_image_operation = ImageOperation(name="Test",
        id="test",
        category = "Testing",
        version = None,
        docs = None,
        alerts = None,
        input_image_metadata={"input1":test_image_metadata_imageint},
        input_image = {"input1":test_image_data_imageint},
        output_image_metadata={"output1":test_image_metadata_imageint},
        )

    setattr(test_image_operation, "execute", types.MethodType(function_no_change_to_output, test_image_operation))

    with pytest.raises(TypeError,match="dictionary value of incorrect type: for 'output1'"):
        test_image_operation.run_code()

#Code provided returns an image with shape that doesn't match metadata
def test_run_code_output_wrong_shape():
    def function_no_change_to_output(self):
        self.output_image = {"output1": sample_data(dtype=DataType.ImageInt, shape=(1,2,3,4))}

    test_image_operation = ImageOperation(name="Test",
        id="test",
        category = "Testing",
        version = None,
        docs = None,
        alerts = None,
        input_image_metadata={"input1":test_image_metadata_imageint},
        input_image = {"input1":test_image_data_imageint},
        output_image_metadata={"output1":ImageMetadata(dtype = DataType.ImageInt,
                                                       image_shape_constraints=Shape(c=5, z=-1, y=-1, x=-1),
                                                       image_map=Shape(c=0, z=1, y=2, x=-3))},
        )
    setattr(test_image_operation, "execute", types.MethodType(function_no_change_to_output, test_image_operation))


    with pytest.raises(ValueError,match="image shape does not match metadata"):
        test_image_operation.run_code()

#Code provided returns an parameter with array type that doesn't match metadata
def test_run_code_parameter_output_wrong_type():
    def function_no_change_to_output(self):
        self.output_image = {"output1": sample_data(dtype=DataType.ImageInt, shape=(1,2,3,4))}
        self.output_parameter = {"output2": sample_data(dtype=DataType.ValueFloat)}

    test_image_operation = ImageOperation(name="Test",
        id="test",
        category = "Testing",
        version = None,
        docs = None,
        alerts = None,
        input_image_metadata={"input1":test_image_metadata_imageint},
        input_image = {"input1":test_image_data_imageint},
        output_image_metadata={"output1":test_image_metadata_imageint},
        output_parameter_metadata={"output2":test_parameter_metadata_valueint}
        )

    setattr(test_image_operation, "execute", types.MethodType(function_no_change_to_output, test_image_operation))

    with pytest.raises(TypeError,match="dictionary value of incorrect type: for 'output2'"):
        test_image_operation.run_code()

#Code provided returns an parameter with array shape that doesn't match metadata
def test_run_code_parameter_output_wrong_shape():
    def function_no_change_to_output(self):
        self.output_image = {"output1": sample_data(dtype=DataType.ImageInt, shape=(1,2,3,4))}
        self.output_parameter = {"output2": sample_data(dtype=DataType.ArrayInt, shape = (2,1))}

    test_image_operation = ImageOperation(name="Test",
        id="test",
        category = "Testing",
        version = None,
        docs = None,
        alerts = None,
        input_image_metadata={"input1":test_image_metadata_imageint},
        input_image = {"input1":test_image_data_imageint},
        output_image_metadata={"output1":test_image_metadata_imageint},
        output_parameter_metadata={"output2": ParameterMetadata(dtype=DataType.ArrayInt, shape = (1,2))}
        )

    setattr(test_image_operation, "execute", types.MethodType(function_no_change_to_output, test_image_operation))

    with pytest.raises(ValueError,match="array shape does not match shape metadata for 'output_parameter.output2'"):
        test_image_operation.run_code()

"""
# Code provided creates an error
def test_run_code_broken_code():
    test=ImageOperation(name="Test",
            category="Testing",
            version=None,
            docs=None,
            alerts=None,
            #input_image={"input":ImageParcel(dtype=DataType.ImageInt,pixel_array=np.array([1,2,3],np.uint8),shape=Shape(-1,-1,-1,-1),image_map=Shape(0,0,0,0))},
            input_parameter=None,
            #output_image={"output":ImageParcel(dtype=DataType.ImageInt,pixel_array=None,shape=Shape(-1,-1,-1,-1),image_map=None)},
            output_parameter=None)

    def test_function(self):
        self.output_image['no_key'].pixel_array=np.array([1,2,3],np.uint8)

    setattr(test, 'execute', types.MethodType(test_function, test))

    with pytest.raises(RuntimeError, match='error executing operation') as exc_info:
        test.run_code() 

    print(f"{exc_info.value}")

# Code provided doesn't create an output
def test_run_code_no_output():
    test=ImageOperation(name="Test",
            category="Testing",
            version=None,
            docs=None,
            alerts=None,
            #input_image={"input":ImageParcel(dtype=DataType.ImageInt,pixel_array=np.array([1,2,3],np.uint8),shape=Shape(-1,-1,-1,-1),image_map=Shape(0,0,0,0))},
            input_parameter=None,
            #output_image={"output":ImageParcel(dtype=DataType.ImageInt,pixel_array=None,shape=Shape(-1,-1,-1,-1),image_map=None)},
            output_parameter=None)

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