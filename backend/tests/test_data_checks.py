import pytest
import numpy as np
from core.shape import Shape
from core.constants import DataPolicy
from core.data_checks import *
from core.metadata import ImageMetadata, ParameterMetadata

test_image_metadata = ImageMetadata(dtype=DataPolicy.ImageInt,
                                    image_shape_constraints=Shape(c=-1, z=-1, y=-1, x=-1),
                                    image_map=Shape(c=0, z=1, y=2, x=3))

test_parameter_metadata = ParameterMetadata(dtype = DataPolicy.ValueInt)

sample_image = sample_data(dtype=DataPolicy.ImageInt,
                           shape=(1,2,3,4))

sample_image_float = sample_data(dtype=DataPolicy.ImageFloat,
                           shape=(1,2,3,4))

sample_parameter = DataPolicy.ValueInt.numpy(2)
sample_parameter_float = DataPolicy.ValueFloat.numpy(2)
"""check_metadata"""
# send metadata not as dictionary
@pytest.mark.parametrize("metadata, dtype, identifier, message", 
                         [(test_image_metadata,ImageMetadata,"image","expected metadata 'image' to be dictionary"),
                          (test_parameter_metadata,ParameterMetadata,"parameter","expected metadata 'parameter' to be dictionary"),
                         ])
def test_check_metadata_not_dictionary(metadata, dtype, identifier, message):
    with pytest.raises(TypeError, match = message):
        check_metadata_dictionary(metadata=metadata, dtype=dtype, identifier=identifier)



# send metadata as dictionary but not of ImageMetadata/ParameterMetadata classes
@pytest.mark.parametrize("metadata, dtype, identifier, message", 
                         [({"input1":"not"},ImageMetadata,"image","for metadata dictionary 'image', expected values of type"),
                          ({"input2": "right"},ParameterMetadata,"parameter","for metadata dictionary 'parameter', expected values of type"),
                         ])
def test_check_metadata_not_dictionary_of_metadata_class(metadata, dtype, identifier, message):
    with pytest.raises(TypeError, match = message):
        check_metadata_dictionary(metadata=metadata, dtype=dtype, identifier=identifier)


"""check_data_dictionaries"""
# data set to function exists
@pytest.mark.parametrize("data, metadata, dtype, identifier, message", 
                         [(None,{"input1":test_image_metadata},ImageMetadata,"image","metadata present with no data: 'image'"),
                          (None,{"input2": test_parameter_metadata},ParameterMetadata,"parameter","metadata present with no data: 'parameter'"),
                         ])
def test_check_data_no_data(data, metadata, dtype, identifier, message):
    with pytest.raises(ValueError, match = message):
        check_data_dictionary(data=data, metadata=metadata, dtype=dtype, identifier=identifier)

# data sent to function is a dictionary 
@pytest.mark.parametrize("data, metadata, dtype, identifier, message", 
                         [(sample_image,{"input1":test_image_metadata},ImageMetadata,"image","expected data 'image' to be dictionary, not"),
                          (sample_parameter,{"input2": test_parameter_metadata},ParameterMetadata,"parameter","expected data 'parameter' to be dictionary, not"),
                         ])
def test_check_data_dictionaries_not_dictionary(data, metadata, dtype, identifier, message):
    with pytest.raises(TypeError, match = message):
        check_data_dictionary(data=data, metadata=metadata, dtype=dtype, identifier=identifier)

# set data where resepective metadata not present
@pytest.mark.parametrize("data, metadata, dtype, identifier, message", 
                         [({"image_input":sample_image},None,ImageMetadata,"image","data present with no metadata: 'image'"),
                          ({"parameter_input":sample_parameter},None,ParameterMetadata,"parameter","data present with no metadata: 'parameter'"),
                         ])
def test_check_data_dictionaries_no_metadata(data, metadata, dtype, identifier, message):
    with pytest.raises(ValueError, match = message):
        check_data_dictionary(data=data, metadata=metadata, dtype=dtype, identifier=identifier)

# set data where the key in data dictionary is not present in the dictionary of metadata
@pytest.mark.parametrize("data, metadata, dtype, identifier, message", 
                         [({"image_input":sample_image},{"image":test_image_metadata},ImageMetadata,"image","key present in data dictionary 'image' but not in metadata"),
                          ({"parameter_input":sample_parameter},{"parameter":test_parameter_metadata},ParameterMetadata,"parameter","key present in data dictionary 'parameter' but not in metadata"),
                         ])
def test_check_data_dictionaries_no_matching_metadata(data, metadata, dtype, identifier, message):
    with pytest.raises(ValueError, match = message):
        check_data_dictionary(data=data, metadata=metadata, dtype=dtype, identifier=identifier)

"""check_data"""

"""check_type"""
# set data where the dtype does not match dtype defined in metadata
@pytest.mark.parametrize("data, metadata, identifier, message", 
                         [({"image":sample_image_float},{"image":test_image_metadata},"image","unexpected dtype for"),
                          ({"parameter":sample_parameter_float},{"parameter":test_parameter_metadata},"parameter","unexpected dtype for"),
                         ])
def test_check_data_type_wrong_type(data, metadata, identifier, message):
    with pytest.raises(TypeError, match = message):
        check_data_type(data=data, metadata=metadata, identifier=identifier)

    with pytest.raises(TypeError, match = message):
        check_data_type(data=data, metadata=metadata, identifier=identifier)

"""check_image_shape"""
# set image where the shape does not match shape defined in metadata
test_image_metadata_shape = ImageMetadata(dtype=DataPolicy.ImageInt,
                                    image_shape_constraints=Shape(c=4, z=4, y=4, x=4),
                                    image_map=Shape(c=0, z=1, y=2, x=3))

sample_image_shape_c= sample_data(dtype=DataPolicy.ImageInt,
                           shape=(1,4,4,4))
sample_image_shape_z= sample_data(dtype=DataPolicy.ImageInt,
                           shape=(4,1,4,4))
sample_image_shape_y= sample_data(dtype=DataPolicy.ImageInt,
                           shape=(4,4,1,4))
sample_image_shape_x= sample_data(dtype=DataPolicy.ImageInt,
                           shape=(4,4,4,1))
@pytest.mark.parametrize("data, metadata, dtype, identifier, message", 
                         [(sample_image_shape_c,test_image_metadata_shape,ImageMetadata,"imagec","for 'imagec', expected c=4, got c=1"),
                          (sample_image_shape_z,test_image_metadata_shape,ImageMetadata,"imagez","for 'imagez', expected z=4, got z=1"),
                          (sample_image_shape_y,test_image_metadata_shape,ImageMetadata,"imagey","for 'imagey', expected y=4, got y=1"),
                          (sample_image_shape_x,test_image_metadata_shape,ImageMetadata,"imagex","for 'imagex', expected x=4, got x=1"),
                         ])
def test_check_data_image_shape(data, metadata, dtype, identifier, message):
    with pytest.raises(ValueError, match = message):
        check_image_shape(data=data, metadata=metadata, identifier=identifier)

 
"""test sample_data"""
# test shape checks - input value where shape is required but not passed
@pytest.mark.parametrize("dtype, message", [
    (DataPolicy.ArrayFloat, "array data type \\(DataPolicy.ArrayFloat\\) supplied without shape"),   
    (DataPolicy.ImageInt, "image data type \\(DataPolicy.ImageInt\\) supplied without shape")     
])
def test_sample_data_shape_no_shape(dtype, message):
    with pytest.raises(TypeError, match=message):
        sample_data(dtype = dtype)

# test shape checks - input value where shape is not np.array, tuple or list
@pytest.mark.parametrize("dtype, shape, message", [
    (DataPolicy.ArrayFloat, 25, "Expected shape as list or tuple, got <class 'int'>"),   
    (DataPolicy.ImageInt, {25,24,1}, "Expected shape as list or tuple, got <class 'set'>")     
])
def test_sample_data_shape_incorrect_array_format(dtype, shape, message):
    with pytest.raises(TypeError, match=message):
        sample_data(dtype = dtype,
                    shape = shape)

# test shape checks - input value where shape is not array of integers
@pytest.mark.parametrize("dtype, shape, message", [
    (DataPolicy.ArrayFloat, [1.0,2.4], "Shape should be array of integers, not <class 'float'>"),   
    (DataPolicy.ImageInt, ("2","4","5"), "Shape should be array of integers, not <class 'str'>")     
])
def test_sample_data_shape_incorrect_format(dtype, shape, message):
    with pytest.raises(TypeError, match=message):
        sample_data(dtype = dtype,
                    shape = shape)
        
# test shape checks - correct shape format
def test_sample_data_shape_correct():
    a = sample_data(DataPolicy.ImageInt,[2,4,5])
    b = sample_data(DataPolicy.ImageFloat,(2,4,5))

    assert a.shape == (2,4,5)
    assert b.shape == (2,4,5)

# test sample_data dtype - input incorrect dtype
@pytest.mark.parametrize("dtype, shape, message", [
    (int, [1.0,2.4], "sample_data dtype must be member of DataType"),   
    (float, ("2","4","5"), "sample_data dtype must be member of DataType")     
])

def test_sample_data_type_incorrect(dtype, shape, message):
    with pytest.raises(TypeError, match=message):
        sample_data(dtype = dtype,
                    shape = shape)
# test sample_data type - Input value of DataType type, output of expected numpy type

def test_sample_data_type_correct():
    test_image = sample_data(dtype=DataPolicy.ImageInt,
                             shape=[2,3],
                             zero=False)
    assert test_image.dtype == DataPolicy.ImageInt.numpy
    assert test_image.shape == (2,3)

    test_image_zeros = sample_data(dtype=DataPolicy.ImageFloat, 
                                   shape=[1,5,9], 
                                   zero=True)
    assert test_image_zeros.dtype == DataPolicy.ImageFloat.numpy
    assert test_image_zeros.shape == (1,5,9)
    assert test_image_zeros.min() == 0
    assert test_image_zeros.max() == 0

    test_array = sample_data(dtype=DataPolicy.ArrayInt,
                             shape=[1,4],
                             zero=False)
    assert test_array.dtype == DataPolicy.ArrayInt.numpy
    assert test_array.shape == (1,4)

    test_array_zeros = sample_data(dtype=DataPolicy.ArrayInt,
                                   shape=[5,2],
                                   zero=True)
    assert test_array_zeros.dtype == DataPolicy.ArrayInt.numpy
    assert test_array_zeros.shape == (5,2)
    assert test_array_zeros.min() == 0
    assert test_array_zeros.max() == 0

    test_value = sample_data(dtype=DataPolicy.ValueFloat,
                                   zero=False)
    assert test_value.dtype == DataPolicy.ValueFloat.numpy


    test_value_zero = sample_data(dtype=DataPolicy.ValueInt,
                                   zero=True)
    assert test_value_zero.dtype == DataPolicy.ValueInt.numpy
    assert test_value_zero == 0



def test_sample_data_min_max():
# value constraint check: For dtype with min, max values, do random values conform to min and max
    a = (sample_data(DataPolicy.ImageInt,[200,300,400]))
    assert a.max() <= DataPolicy.ImageInt.max_value
    assert a.min() >= DataPolicy.ImageInt.min_value


