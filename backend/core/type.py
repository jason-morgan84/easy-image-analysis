import numpy as np
import numbers
from core.constants import DataType


class BaseType:
    """ Create new DataTypes based on this framework.
    Each new DataType must have data_type and numpy set.
    min_value, max_value and is_array can be set based on requirements.
    
    For conversions between classes, permitted_conversions or warned_conversions must be set, then override the default '_convert' function.
    Attempts to convert between classes where type conversions have not been explicitly coded will result in an error message."""

    data_type = None                # reference to this data type in DataType enum in constant.py
    numpy = None                    # default numpy equivalent data_type   
    description = None              # text description of class and what its for
    min_value = None                # minimum allowed value, if defined
    max_value = None                # maximum allowed value, if defined
    is_image = False                # does this type define an image? An image is assumed to be mutli-dimensional, is_array does not need to be set to True
    is_array = False                # does this represent a multi-dimensional value?
    permitted_conversions = []    # list of other DataType classes this can be converted to automatically
    warned_conversion = []        # list of other DataType classes this can be converted to, with a prompt to user

    @classmethod
    def validate(cls, val):
        # if type has is_image or is_array flags (multi-dimensional variable)
        if cls.is_image is True or cls.is_array is True:
            # if input value is not a np array, raise TypeError
            if not isinstance(val, np.ndarray):
                raise TypeError(f"expected np.array for {cls.data_type}, got {type(val)}")
            # if input array elements are not of expected type, raise TypeError
            if val.dtype != cls.numpy:
                raise TypeError(f"expected np.array of {cls.numpy} for {cls.data_type}, got {val.dtype}")
            # if a max_value is set, raise ValueError if this is exceeded
            if cls.max_value and val.max() > cls.max_value:
                raise ValueError(f"array exceeds maximum value: {cls.data_type} has max_value of {cls.max_value}, not {val.max()}") 
            # if a min_value is set, raise ValueError if this is exceeded
            if cls.min_value and val.min() < cls.min_value:
                raise ValueError(f"array below minimum value: {cls.data_type} has min_value of {cls.min_value}, not {val.min()}") 
        # if type has is scalar variable (is_image and is_array are False)
        elif cls.is_image is False and cls.is_array is False:
            # if value is not of expected type, raise TypeError
            if not isinstance(val, cls.numpy):
                raise TypeError(f"expected data type of {cls.numpy} for {cls.data_type}, got {type(val)}")
            # if a max_value is set, raise ValueError if this is exceeded
            if cls.max_value and val > cls.max_value:
                raise ValueError(f"value exceeds maximum value: {cls.data_type} has max_value of {cls.max_value}, not {val}") 
            # if a min_value is set, raise ValueError if this is exceeded
            if cls.min_value and val < cls.min_value:
                raise ValueError(f"value below minimum value: {cls.data_type} has min_value of {cls.min_value}, not {val}") 

    def to(cls, value, dtype):
        # check value meets definition of self.data_type
        try: 
            cls.validate(value)
        except Exception as e:
            raise ValueError(f"data for conversion from {cls.data_type} to {cls.dtype} does not meet constraints: {e}")

        # check dtype is permitted type to convert self.data_type to
        cls.permitted_conversions = [] if cls.permitted_conversions == None else cls.permitted_conversions
        cls.warned_conversions = [] if cls.warned_conversions == None else cls.warned_conversions

        if dtype in cls.permitted_conversions or dtype in cls.warned_conversions or dtype == cls.data_type:
            # if acceptable dtype, carry out conversion
            try:
                output = cls._convert(value, dtype)
            except Exception as e:
                raise ValueError(f"error in conversion from {cls.data_type} to {cls.dtype}: {e}")
        else:
            raise ValueError(f"conversion from {cls.data_type} to {dtype} not permitted")

        # validate conversion is correct format for dtype
        try:
            dtype.validate(output)
        except Exception as e:
            raise ValueError(f"converted data does not validate as {dtype}: {e}")
        return output

    def _convert(self, value, dtype):
        raise NotImplementedError(f"type conversions not yet implemented for data type {self.data_type} to {dtype}")

class ImageInt(BaseType):
    data_type = DataType.ImageInt
    description = "Describes multi-dimensional arrays for images as integers in the range 0 - 255 (inclusive)"
    numpy = np.uint8
    is_array = False
    is_image = True
    min_value = 0
    max_value = 255
    permitted_conversions = [DataType.ImageFloat]

    def _convert(self, value, dtype):
        if dtype == DataType.ImageFloat:
            return dtype.numpy(value/255).copy()
        elif dtype == DataType.ImageBinary:
            return dtype.numpy(value).copy()
        elif dtype == DataType.ImageInt and dtype == self.data_type:
            return value.copy()
        else:
            raise TypeError(f"ImageInt cannot be converted to type {dtype}")

class ImageFloat(BaseType):
    data_type = DataType.ImageFloat
    description = "Data type to hold multi-dimensional arrays for images as floats in the range 0 - 1 (inclusive)"
    numpy = np.float64
    is_array = False
    is_image = True
    min_value = 0.0
    max_value = 1.0
    permitted_conversions = [DataType.ImageInt]

    def _convert(self, value, dtype):
        if dtype == DataType.ImageInt:
            return dtype.numpy(np.round(value * 255)).copy()
        elif dtype == DataType.ImageBinary:
            return dtype.numpy(np.round(value)).copy()
        elif dtype == DataType.ImageFloat:
            return value.copy()
        else:
            raise TypeError(f"ImageFloat cannot be converted to type {dtype}")

class ImageBinary(BaseType):
    data_type = DataType.ImageBinary
    description = "Data type to hold multi-dimensional arrays for images as either 1 or 0"
    numpy = np.uint8
    is_array = False
    is_image = True
    min_value = 0
    max_value = 1
    warned_conversions = [DataType.ImageInt, DataType.ImageFloat]

    def _convert(self, value, dtype):
        if dtype == DataType.ImageFloat:
            return dtype.numpy(value).copy()
        elif dtype == DataType.ImageInt:
            return dtype.numpy(value).ccopy()
        elif dtype == DataType.ImageBinary:
            return value
        else:
            raise TypeError(f"ImageBinary cannot be converted to type {dtype}")
        
class ValueInt(BaseType):
    data_type = DataType.ValueInt
    description = "Data type to hold single variables as integers"
    numpy = np.uint8
    allowed_conversions = [DataType.ValueFloat]

    def _convert(self, value, dtype):
        if dtype == DataType.ValueFloat:
            return dtype.numpy(value).copy()
        else:
            raise TypeError(f"ValueInt cannot be converted to type {dtype}")

class ValueFloat(BaseType):
    data_type = DataType.ValueFloat
    description = "Data type to hold single variables as floats"
    numpy = np.float64
    allowed_conversions = [DataType.ValueInt]

    def _convert(self, value, dtype):
        if dtype == DataType.ValueInt:
            return dtype.numpy(np.round(value)).copy()
        else:
            raise TypeError(f"ValueFloat cannot be converted to type {dtype}")

class ArrayInt(BaseType):
    data_type = DataType.ArrayInt
    description = "Data type to hold variables lists as ints"
    numpy = np.uint8
    is_array = True
    allowed_conversions = [DataType.ArrayFloat]

    def _convert(self, value, dtype):
        if dtype == DataType.ArrayFloat:
            return dtype.numpy(value).copy()
        elif dtype == DataType.ArrayInt:
            return value.copy()
        else:
            raise TypeError(f"ArrayInt cannot be converted to type {dtype}")

class ArrayFloat(BaseType):
    data_type = DataType.ArrayFloat
    description = "Data type to hold variables lists as floats"
    numpy = np.float64
    is_array = True
    allowed_conversions = [DataType.ArrayInt]

    def _convert(self, value, dtype):
        if dtype == DataType.ArrayInt:
            return dtype.numpy(np.round(value)).copy()
        elif dtype == DataType.ArrayFloat:
            return value.copy()
        else:
            raise TypeError(f"ArrayFloat cannot be converted to type {dtype}")

def sample_data(dtype, shape = None, zero = False):
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