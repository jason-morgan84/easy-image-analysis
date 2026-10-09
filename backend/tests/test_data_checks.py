import pytest
import numpy as np
from core.shape import Shape
from core.constants import DataType
from core.image_operation import ImageOperation
from core.metadata import ImageMetadata, ParameterMetadata
from core.type import sample_data
import types


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