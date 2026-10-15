import pytest
import numpy as np
from core.shape import Shape
from core.constants import DataType
from core.data_checks import check_metadata, check_data_dictionaries, check_data, check_type, check_image_shape, check_parameter_shape, sample_data
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
                         [(test_image_metadata,ImageMetadata,"image","expected 'image' to be dictionary"),
                          (test_parameter_metadata,ParameterMetadata,"parameter","expected 'parameter' to be dictionary"),
                         ])
def test_check_metadata_not_dictionary(metadata, dtype, identifier, message):
    with pytest.raises(TypeError, match = message):
        check_metadata(metadata=metadata, dtype=dtype, identifier=identifier)

# send metadata as dictionary but not of ImageMetadata/ParameterMetadata classes
@pytest.mark.parametrize("metadata, dtype, identifier, message", 
                         [({"input1":"not"},ImageMetadata,"image","for metadata dictionary 'image', expected values of type"),
                          ({"input2": "right"},ParameterMetadata,"parameter","for metadata dictionary 'parameter', expected values of type"),
                         ])
def test_check_metadata_not_dictionary_of_metadata_class(metadata, dtype, identifier, message):
    with pytest.raises(TypeError, match = message):
        check_metadata(metadata=metadata, dtype=dtype, identifier=identifier)


"""check_data_dictionaries"""
# data set to function exists
@pytest.mark.parametrize("data, metadata, dtype, identifier, message", 
                         [(None,{"input1":test_image_metadata},ImageMetadata,"image","metadata present with no data: 'image'"),
                          (None,{"input2": test_parameter_metadata},ParameterMetadata,"parameter","metadata present with no data: 'parameter'"),
                         ])
def test_check_data_no_data(data, metadata, dtype, identifier, message):
    with pytest.raises(ValueError, match = message):
        check_data_dictionaries(data=data, metadata=metadata, dtype=dtype, identifier=identifier)

# data sent to function is a dictionary 
@pytest.mark.parametrize("data, metadata, dtype, identifier, message", 
                         [(sample_image,{"input1":test_image_metadata},ImageMetadata,"image","expected 'image' to be dictionary, not"),
                          (sample_parameter,{"input2": test_parameter_metadata},ParameterMetadata,"parameter","expected 'parameter' to be dictionary, not"),
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
                         [({"image":sample_image_float},{"image":test_image_metadata},ImageMetadata,"image","dictionary value of incorrect type: for 'image' in 'image' expected"),
                          ({"parameter":sample_parameter_float},{"parameter":test_parameter_metadata}, ParameterMetadata, "parameter","dictionary value of incorrect type: for 'parameter' in 'parameter' expected"),
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
                         [({"image":sample_image_shape_c},{"image":test_image_metadata_shape},ImageMetadata,"imagec","image shape does not match metadata; for 'imagec.image'"),
                          ({"image":sample_image_shape_z},{"image":test_image_metadata_shape},ImageMetadata,"imagez","image shape does not match metadata; for 'imagez.image'"),
                          ({"image":sample_image_shape_y},{"image":test_image_metadata_shape},ImageMetadata,"imagey","image shape does not match metadata; for 'imagey.image'"),
                          ({"image":sample_image_shape_x},{"image":test_image_metadata_shape},ImageMetadata,"imagex","image shape does not match metadata; for 'imagex.image'"),
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
    with pytest.raises(ValueError, match = "no shape defined in metadata for array type parameter 'test.input'"):
        check_parameter_shape(data={"input":sample_parameter}, metadata={"input":test_parameter_metadata}, identifier="test")

    with pytest.raises(ValueError, match = "no shape defined in metadata for array type parameter 'test.input'"):
        check_data(data={"input":sample_parameter}, metadata={"input":test_parameter_metadata},  dtype = ParameterMetadata, identifier="test")

# set parameter where the shape does not match shape defined in metadata
def test_check_data_parameter_shape():
    test_parameter_metadata = ParameterMetadata(dtype=DataType.ArrayInt, shape = (2,1))
    sample_parameter = sample_data(dtype=DataType.ArrayInt, shape=(1,2))
    with pytest.raises(ValueError, match = "array shape does not match shape metadata for 'test.input'"):
        check_parameter_shape(data={"input":sample_parameter}, metadata={"input":test_parameter_metadata}, identifier="test")

    with pytest.raises(ValueError, match = "array shape does not match shape metadata for 'test.input'"):
        check_data(data={"input":sample_parameter}, metadata={"input":test_parameter_metadata},  dtype = ParameterMetadata, identifier="test")

"""test sample_data"""
# test shape checks - input value where shape is required but not passed
@pytest.mark.parametrize("dtype, message", [
    (DataType.ArrayFloat, "array data type \\(<class 'core.type.ArrayFloat'>\\) supplied without shape"),   
    (DataType.ImageInt, "image data type \\(<class 'core.type.ImageInt'>\\) supplied without shape")     
])
def test_sample_data_shape_no_shape(dtype, message):
    with pytest.raises(TypeError, match=message):
        sample_data(dtype = dtype)

# test shape checks - input value where shape is not np.array, tuple or list
@pytest.mark.parametrize("dtype, shape, message", [
    (DataType.ArrayFloat, 25, "Expected shape as list or tuple, got <class 'int'>"),   
    (DataType.ImageInt, {25,24,1}, "Expected shape as list or tuple, got <class 'set'>")     
])
def test_sample_data_shape_incorrect_array_format(dtype, shape, message):
    with pytest.raises(TypeError, match=message):
        sample_data(dtype = dtype,
                    shape = shape)

# test shape checks - input value where shape is not array of integers
@pytest.mark.parametrize("dtype, shape, message", [
    (DataType.ArrayFloat, [1.0,2.4], "Shape should be array of integers, not <class 'float'>"),   
    (DataType.ImageInt, ("2","4","5"), "Shape should be array of integers, not <class 'str'>")     
])
def test_sample_data_shape_incorrect_format(dtype, shape, message):
    with pytest.raises(TypeError, match=message):
        sample_data(dtype = dtype,
                    shape = shape)
        
# test shape checks - correct shape format
def test_sample_data_shape_correct():
    a = sample_data(DataType.ImageInt,[2,4,5])
    b = sample_data(DataType.ImageFloat,(2,4,5))

    assert a.shape == (2,4,5)
    assert b.shape == (2,4,5)

# test sample_data dtype - input incorrect dtype
@pytest.mark.parametrize("dtype, shape, message", [
    (int, [1.0,2.4], "Shape should be array of integers, not <class 'float'>"),   
    (float, ("2","4","5"), "Shape should be array of integers, not <class 'str'>")     
])

def test_sample_data_type_incorrect(dtype, shape, message):
    with pytest.raises(TypeError, match=message):
        sample_data(dtype = dtype,
                    shape = shape)
# test sample_data type - Input value of DataType type, output of expected numpy type

def test_sample_data_type_correct():
    assert sample_data(DataType.ImageInt,[2,3]).dtype == DataType.ImageInt.numpy
    assert sample_data(DataType.ImageFloat,[2,3]).dtype == DataType.ImageFloat.numpy
    assert type(sample_data(DataType.ValueFloat,[2,3])) ==DataType.ValueFloat.numpy
    assert sample_data(DataType.ArrayInt,[2,3]).dtype == DataType.ArrayInt.numpy



def test_sample_data():

# type checks: Input value of DataType type, output of expected type
    assert isinstance(sample_data(DataType.ImageInt,[2,3]), DataType.ImageInt.numpy)
    assert (sample_data(DataType.ImageFloat,[2,3])).data_type == DataType.ImageFloat
    assert (sample_data(DataType.ValueFloat)).data_type == DataType.ValueFloat
    assert (sample_data(DataType.ArrayInt, (5,4))).data_type == DataType.ArrayInt

#shape checks: For array dtype, does output have expected shape with randomized values
    assert (sample_data(DataType.ImageInt,[5,4], numpy=False)).value.shape == (5,4)
    assert (sample_data(DataType.ImageFloat,[1,2,3], numpy=False)).value.shape == (1,2,3)
    assert (sample_data(DataType.ArrayInt,[1,2,3,4], numpy=False)).value.shape == (1,2,3,4)

#shape checks: For array dtype, does output have expected shape with 0 values
    assert (sample_data(DataType.ImageInt,[5,4],zero = True, numpy=False)).value.shape == (5,4)
    assert (sample_data(DataType.ImageFloat,[1,2,3],zero = True, numpy=False)).value.shape == (1,2,3)
    assert (sample_data(DataType.ArrayInt,[1,2,3,4],zero = True, numpy=False)).value.shape == (1,2,3,4)
    #def sample_data(dtype, shape = None, zero = False):

# value constraint check: For dtype with min, max values, do random values conform to min and max
    a = (sample_data(DataType.ImageInt,[200,300,400], zero = True, numpy=False))
    assert a.value.max() <= a.data_type.max_value
    assert a.value.min() >= a.data_type.min_value


