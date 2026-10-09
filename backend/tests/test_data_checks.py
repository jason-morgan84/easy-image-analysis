import pytest
import numpy as np
from core.shape import Shape
from core.constants import DataType
from core.data_checks import check_metadata, check_data_dictionaries, check_data, check_type, check_image_shape, check_parameter_shape
from core.type import sample_data
from core.metadata import ImageMetadata, ParameterMetadata

test_image_metadata = ImageMetadata(dtype=DataType.ImageInt,
                                    image_shape_constraints=Shape(c=-1, z=-1, y=-1, x=-1),
                                    image_map=Shape(c=0, z=1, y=2, x=3))

test_parameter_metadata = ParameterMetadata(dtype = DataType.ValueInt)

sample_image = sample_data(dtype=DataType.ImageInt,
                           shape=(1,2,3,4))

sample_image_float = sample_data(dtype=DataType.ImageFloat,
                           shape=(1,2,3,4))

sample_parameter = DataType.ValueInt.numpy(2)
sample_parameter_float = DataType.ValueFloat.numpy(2)
"""check_metadata"""
# send metadata not as dictionary
@pytest.mark.parametrize("metadata, dtype, identifier, message", 
                         [(test_image_metadata,ImageMetadata,"image","expected image to be dictionary"),
                          (test_parameter_metadata,ParameterMetadata,"parameter","expected parameter to be dictionary"),
                         ])
def test_check_metadata_not_dictionary(metadata, dtype, identifier, message):
    with pytest.raises(TypeError, match = message):
        check_metadata(metadata=metadata, dtype=dtype, identifier=identifier)

# send metadata as dictionary but not of ImageMetadata/ParameterMetadata classes
@pytest.mark.parametrize("metadata, dtype, identifier, message", 
                         [({"input1":"not"},ImageMetadata,"image","for metadata image, expected values of type"),
                          ({"input2": "right"},ParameterMetadata,"parameter","for metadata parameter, expected values of type"),
                         ])
def test_check_metadata_not_dictionary_of_metadata_class(metadata, dtype, identifier, message):
    with pytest.raises(TypeError, match = message):
        check_metadata(metadata=metadata, dtype=dtype, identifier=identifier)


"""check_data_dictionaries"""
# data sent to function is a dictionary 
@pytest.mark.parametrize("data, metadata, dtype, identifier, message", 
                         [(sample_image,{"input1":test_image_metadata},ImageMetadata,"image","expected image to be dictionary, not"),
                          (sample_parameter,{"input2": test_parameter_metadata},ParameterMetadata,"parameter","expected parameter to be dictionary, not"),
                         ])
def test_check_data_dictionaries_not_dictionary(data, metadata, dtype, identifier, message):
    with pytest.raises(TypeError, match = message):
        check_data_dictionaries(data=data, metadata=metadata, dtype=dtype, identifier=identifier)

# set data where resepective metadata not present
@pytest.mark.parametrize("data, metadata, dtype, identifier, message", 
                         [({"image_input":sample_image},None,ImageMetadata,"image","data present with no metadata: 'image'"),
                          ({"parameter_input":sample_parameter},None,ParameterMetadata,"parameter","data present with no metadata: 'parameter'"),
                         ])
def test_check_data_dictionaries_no_metadata(data, metadata, dtype, identifier, message):
    with pytest.raises(ValueError, match = message):
        check_data_dictionaries(data=data, metadata=metadata, dtype=dtype, identifier=identifier)

# set data where the key in data dictionary is not present in the dictionary of metadata
@pytest.mark.parametrize("data, metadata, dtype, identifier, message", 
                         [({"image_input":sample_image},{"image":test_image_metadata},ImageMetadata,"image","key present in data dictionary 'image' but not in metadata"),
                          ({"parameter_input":sample_parameter},{"parameter":test_parameter_metadata},ParameterMetadata,"parameter","key present in data dictionary 'parameter' but not in metadata"),
                         ])
def test_check_data_dictionaries_no_matching_metadata(data, metadata, dtype, identifier, message):
    with pytest.raises(ValueError, match = message):
        check_data_dictionaries(data=data, metadata=metadata, dtype=dtype, identifier=identifier)

"""check_data"""

"""check_type"""
# set data where the dtype does not match dtype defined in metadata
@pytest.mark.parametrize("data, metadata, dtype, identifier, message", 
                         [({"image":sample_image_float},{"image":test_image_metadata},ImageMetadata,"image","dictionary value of incorrect type: for image in image expected"),
                          ({"parameter":sample_parameter_float},{"parameter":test_parameter_metadata}, ParameterMetadata, "parameter","dictionary value of incorrect type: for parameter in parameter expected"),
                         ])
def test_check_data_type_wrong_type(data, metadata, dtype, identifier, message):
    with pytest.raises(TypeError, match = message):
        check_type(data=data, metadata=metadata, identifier=identifier)

    with pytest.raises(TypeError, match = message):
        check_data(data=data, metadata=metadata, dtype=dtype, identifier=identifier)

"""check_image_shape"""
# set image where the shape does not match shape defined in metadata
test_image_metadata_shape = ImageMetadata(dtype=DataType.ImageInt,
                                    image_shape_constraints=Shape(c=4, z=4, y=4, x=4),
                                    image_map=Shape(c=0, z=1, y=2, x=3))

sample_image_shape_c= sample_data(dtype=DataType.ImageInt,
                           shape=(1,4,4,4))
sample_image_shape_z= sample_data(dtype=DataType.ImageInt,
                           shape=(4,1,4,4))
sample_image_shape_y= sample_data(dtype=DataType.ImageInt,
                           shape=(4,4,1,4))
sample_image_shape_x= sample_data(dtype=DataType.ImageInt,
                           shape=(4,4,4,1))
@pytest.mark.parametrize("data, metadata, dtype, identifier, message", 
                         [({"image":sample_image_shape_c},{"image":test_image_metadata_shape},ImageMetadata,"imagec","image shape does not match metadata; for imagec.image"),
                          ({"image":sample_image_shape_z},{"image":test_image_metadata_shape},ImageMetadata,"imagez","image shape does not match metadata; for imagez.image"),
                          ({"image":sample_image_shape_y},{"image":test_image_metadata_shape},ImageMetadata,"imagey","image shape does not match metadata; for imagey.image"),
                          ({"image":sample_image_shape_x},{"image":test_image_metadata_shape},ImageMetadata,"imagex","image shape does not match metadata; for imagex.image"),
                         ])
def test_check_data_image_shape(data, metadata, dtype, identifier, message):
    with pytest.raises(ValueError, match = message):
        check_image_shape(data=data, metadata=metadata, identifier=identifier)

    with pytest.raises(ValueError, match = message):
        check_data(data=data, metadata=metadata, dtype=dtype, identifier=identifier)

"""check_parameter_shape"""
# set parameter where shape does not exist in metadata
def test_check_data_parameter_no_shape():
    test_parameter_metadata = ParameterMetadata(dtype=DataType.ArrayInt)
    sample_parameter = sample_data(dtype=DataType.ArrayInt, shape=(1,2))
    with pytest.raises(ValueError, match = "no shape defined in metadata for array type parameter test.input"):
        check_parameter_shape(data={"input":sample_parameter}, metadata={"input":test_parameter_metadata}, identifier="test")

    with pytest.raises(ValueError, match = "no shape defined in metadata for array type parameter test.input"):
        check_data(data={"input":sample_parameter}, metadata={"input":test_parameter_metadata},  dtype = ParameterMetadata, identifier="test")

# set parameter where the shape does not match shape defined in metadata
def test_check_data_parameter_shape():
    test_parameter_metadata = ParameterMetadata(dtype=DataType.ArrayInt, shape = (2,1))
    sample_parameter = sample_data(dtype=DataType.ArrayInt, shape=(1,2))
    with pytest.raises(ValueError, match = "array shape does not match shape metadata for test.input"):
        check_parameter_shape(data={"input":sample_parameter}, metadata={"input":test_parameter_metadata}, identifier="test")

    with pytest.raises(ValueError, match = "array shape does not match shape metadata for test.input"):
        check_data(data={"input":sample_parameter}, metadata={"input":test_parameter_metadata},  dtype = ParameterMetadata, identifier="test")

"""
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

""""""test check_set_data function""""""
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
        setattr(test_image_operation, test_attribute, attribute_value)"""