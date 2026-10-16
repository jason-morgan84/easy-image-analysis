from core.metadata import ImageMetadata, ParameterMetadata
from core.shape import Shape
from core.constants import DataType
import numpy as np
"""
Includes functions for checking data and metadata at various points in the workflow:
    - check_metadata: checks that metadata is a dictionary with values of either ImageMetadata or ParameteMetadata types
    - check_data_dictionaries: calls check_metadata, then also checks that data is a dictionary that have associated metadata with a matching key
    - check_data: calls check_data_dictionarys, then also checks that data dictionary items match constraints of metadata
"""

# checks metadata dictionaries are dictionaries and values are of ImageMetadata or ParameterMetadata types
def check_metadata_dictionary(metadata, dtype, identifier):
    if metadata is not None:
        # check dictionary is a dictionary
        if not isinstance(metadata, dict):
            raise TypeError(f"expected '{identifier}' to be dictionary, not {type(metadata)}")
        
        for value in metadata.values():
            # check values are of correct type
            if not isinstance(value, dtype):
                raise TypeError(f"for metadata dictionary '{identifier}', expected values of type {dtype}, got {type(value)}")
        return True
    else:
        return False

# checks data dictionaries are dictionaries, have associated metadata and match a meta data key
def check_data_dictionary(data, metadata, dtype, identifier):

    # check metadata
    if not check_metadata_dictionary(metadata, dtype, identifier):
        raise ValueError(f"data present with no metadata: '{identifier}'")
    if data is None:
        raise ValueError(f"metadata present with no data: '{identifier}'")
    # check data dictionary is a dictionary
    if not isinstance(data, dict):
        raise TypeError(f"expected '{identifier}' to be dictionary, not {type(data)}")           
    
    # check key is present in relevant metadata
    for key in data.keys():
        if key not in metadata.keys():
            raise ValueError(f"key present in data dictionary '{identifier}' but not in metadata: '{key}'")

def check_data_dictionary_value(data, metadata, dtype, identifier):
    # check data dictionary is in correct format
    check_data_dictionary(data, metadata, dtype, identifier)

    # check that a metadata key exists for all data
    for key in data.keys():
        if key not in metadata.keys():
            raise ValueError(f"data present with no metadata: '{identifier}.{key}'")

    if dtype == ImageMetadata:
        for key, value in metadata.items():
            check_data_type(data=data[key], metadata=value, identifier=".".join([identifier, key]))
            check_image_shape(data=data[key], metadata=value, identifier=".".join([identifier, key]))
    elif dtype == ParameterMetadata:
        for key, value in metadata.items():
            check_data_type(data=data[key], metadata=value, identifier=".".join([identifier, key]))
            check_parameter_shape(data=data[key], metadata=value, identifier=".".join([identifier, key]))
    else:
        raise NotImplementedError(f"data checking not implemented for data type {dtype}")


def check_data_type(data, metadata, identifier):
    # go through each value in metadata, check that the respective data is of the correct dtype
    try:
        metadata.dtype.validate(data)
    except Exception as e:
        raise TypeError(f"data dictionary value for '{identifier}' does not pass dtype validation: {e}")
       

def check_image_shape(data, metadata, identifier):
    # go through each value in metadata, check that the respective image matches shape constraints
    for dimension in Shape.dimensions:
        if metadata.image_shape_constraints[dimension] != -1:
            if data.shape[metadata.image_map[dimension]] != metadata.image_shape_constraints[dimension]:
                raise ValueError(f"image shape does not match metadata; for '{identifier}', expected {dimension}={metadata.image_shape_constraints[dimension]}, got {dimension}={data.shape[metadata.image_map[dimension]]}")

def check_parameter_shape(data, metadata, identifier):
    # check whether the datatype is an array. If it is, check that shape metadata is present and it matches the arrays shape
        if metadata.dtype.is_array == True:
            if metadata.shape is None:
                raise ValueError(f"no shape defined in metadata for array type parameter '{identifier}'")
            for n, dimension in enumerate(metadata.shape):
                if data.shape[n] != dimension:
                    raise ValueError(f"array shape does not match shape metadata for '{identifier}'")

def sample_data(dtype, shape = None, zero = False):
    if dtype not in DataType:
        raise TypeError(f"sample_data dtype must be member of DataType (see constants.py)")
    value_dtype = getattr(dtype, "data_type", None)
    if value_dtype == None or value_dtype not in DataType.types():
        raise TypeError (f"Expected Image data type (see constants.py) got {dtype}")
    # used for generating sample data sets of given type

        
    if dtype.is_array is True or dtype.is_image is True:
        if shape == None:
            raise TypeError (f"{"array" if dtype.is_array else "image"} data type ({dtype}) supplied without shape")
        if type(shape) not in [list,tuple]:
            raise TypeError (f"Expected shape as list or tuple, got {type(shape)}")
        if not isinstance(shape[0],(int,np.integer)):
            raise TypeError (f"Shape should be array of integers, not {type(shape[0])}")
        if zero:
            output = dtype.numpy(np.zeros(shape))
            return output
        else:
            max = 255 if dtype.max_value == None else dtype.max_value
            min = 0 if dtype.min_value == None else dtype.min_value
            range = max - min
            random_array = np.random.random(size = shape) # gives random array between 0 and 1 of desired shape
            random_array = (random_array * range) + min # gets array between min and max values
            output = dtype.numpy(random_array)
            return output
    else:
        if zero:
            return dtype.numpy(0)
        else:
            max = 255 if dtype.max_value == None else dtype.max_value
            min = 0 if dtype.min_value == None else dtype.min_value
            range = max - min
            output = dtype.numpy(np.random.random() * range + min)
            return output