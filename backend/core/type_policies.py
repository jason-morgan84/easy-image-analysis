import numpy as np
import numbers
from core.constants import DataPolicy


class BasePolicy:
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
    warned_conversions = []        # list of other DataType classes this can be converted to, with a prompt to user

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
            if cls.max_value is not None and val.max() > cls.max_value:
                raise ValueError(f"array exceeds maximum value: {cls.data_type} has max_value of {cls.max_value}, not {val.max()}") 
            # if a min_value is set, raise ValueError if this is exceeded
            if cls.min_value is not None and val.min() < cls.min_value:
                raise ValueError(f"array below minimum value: {cls.data_type} has min_value of {cls.min_value}, not {val.min()}") 
        # if type has is scalar variable (is_image and is_array are False)
        elif cls.is_image is False and cls.is_array is False:
            # if value is not of expected type, raise TypeError
            if not isinstance(val, cls.numpy):
                raise TypeError(f"expected data type of {cls.numpy} for {cls.data_type}, got {type(val)}")
            # if a max_value is set, raise ValueError if this is exceeded
            if cls.max_value is not None and val > cls.max_value:
                raise ValueError(f"value exceeds maximum value: {cls.data_type} has max_value of {cls.max_value}, not {val}") 
            # if a min_value is set, raise ValueError if this is exceeded
            if cls.min_value is not None and val < cls.min_value:
                raise ValueError(f"value below minimum value: {cls.data_type} has min_value of {cls.min_value}, not {val}") 
    @classmethod
    def to(cls, value, dtype):

        # if to is called with no dtype, return input value
        if dtype == None:
            return value.copy()
               
        # check value meets definition of self.data_type
        try: 
            cls.validate(value)
        except Exception as e:
            raise ValueError(f"data for conversion from {cls.data_type} to {dtype} does not meet constraints: {e}")

        # check dtype is permitted type to convert self.data_type to
        cls.permitted_conversions = [] if cls.permitted_conversions == None else cls.permitted_conversions
        cls.warned_conversions = [] if cls.warned_conversions == None else cls.warned_conversions
        if dtype in cls.permitted_conversions or dtype in cls.warned_conversions or dtype == cls.data_type:
            # if acceptable dtype, carry out conversion
            try:
                output = cls._convert(value, dtype)
            except Exception as e:
                raise ValueError(f"error in conversion from {cls.data_type} to {dtype}: {e}")
        else:
            raise ValueError(f"conversion from {cls.data_type} to {dtype} not permitted")

        # validate conversion is correct format for dtype
        try:
            dtype.validate(output)
        except Exception as e:
            raise ValueError(f"converted data does not validate as {dtype}: {e}")
        return output
    
    @classmethod
    def _convert(cls, value, dtype):
        raise NotImplementedError(f"type conversions not yet implemented for data type {cls.data_type} to {dtype}")

class ImageInt(BasePolicy):
    data_type = DataPolicy.ImageInt
    description = "Describes multi-dimensional arrays for images as integers in the range 0 - 255 (inclusive)"
    numpy = np.uint8
    is_array = False
    is_image = True
    min_value = 0
    max_value = 255
    permitted_conversions = [DataPolicy.ImageFloat]

    @classmethod
    def _convert(cls, value, dtype):
        if dtype == DataPolicy.ImageFloat:
            return dtype.numpy(value/255).copy()
        elif dtype == DataPolicy.ImageBinary:
            return dtype.numpy(value).copy()
        elif dtype == DataPolicy.ImageInt and dtype == cls.data_type:
            return value.copy()
        else:
            raise TypeError(f"ImageInt cannot be converted to type {dtype}")

class ImageFloat(BasePolicy):
    data_type = DataPolicy.ImageFloat
    description = "Data type to hold multi-dimensional arrays for images as floats in the range 0 - 1 (inclusive)"
    numpy = np.float64
    is_array = False
    is_image = True
    min_value = 0.0
    max_value = 1.0
    permitted_conversions = [DataPolicy.ImageInt]
    
    @classmethod
    def _convert(cls, value, dtype):
        if dtype == DataPolicy.ImageInt:
            return dtype.numpy(np.round(value * 255)).copy()
        elif dtype == DataPolicy.ImageBinary:
            return dtype.numpy(np.round(value)).copy()
        elif dtype == DataPolicy.ImageFloat:
            return value.copy()
        else:
            raise TypeError(f"ImageFloat cannot be converted to type {dtype}")

class ImageBinary(BasePolicy):
    data_type = DataPolicy.ImageBinary
    description = "Data type to hold multi-dimensional arrays for images as either 1 or 0"
    numpy = np.uint8
    is_array = False
    is_image = True
    min_value = 0
    max_value = 1
    warned_conversions = [DataPolicy.ImageInt, DataPolicy.ImageFloat]

    @classmethod
    def _convert(cls, value, dtype):
        if dtype == DataPolicy.ImageFloat:
            return dtype.numpy(value).copy()
        elif dtype == DataPolicy.ImageInt:
            return dtype.numpy(value).copy()
        elif dtype == DataPolicy.ImageBinary:
            return value.copy()
        else:
            raise TypeError(f"ImageBinary cannot be converted to type {dtype}")
        
class ValueInt(BasePolicy):
    data_type = DataPolicy.ValueInt
    description = "Data type to hold single variables as integers"
    numpy = np.uint8
    permitted_conversions = [DataPolicy.ValueFloat]

    @classmethod
    def _convert(cls, value, dtype):
        if dtype == DataPolicy.ValueFloat:
            return dtype.numpy(value).copy()
        elif dtype == DataPolicy.ValueInt:
            return dtype.numpy(value).copy()
        else:
            raise TypeError(f"ValueInt cannot be converted to type {dtype}")

class ValueFloat(BasePolicy):
    data_type = DataPolicy.ValueFloat
    description = "Data type to hold single variables as floats"
    numpy = np.float64
    permitted_conversions = [DataPolicy.ValueInt]

    @classmethod
    def _convert(cls, value, dtype):
        if dtype == DataPolicy.ValueInt:
            return dtype.numpy(np.round(value)).copy()
        elif dtype == DataPolicy.ValueFloat:
            return dtype.numpy(value).copy()
        else:
            raise TypeError(f"ValueFloat cannot be converted to type {dtype}")

class ArrayInt(BasePolicy):
    data_type = DataPolicy.ArrayInt
    description = "Data type to hold variables lists as ints"
    numpy = np.uint8
    is_array = True
    permitted_conversions = [DataPolicy.ArrayFloat]

    @classmethod
    def _convert(cls, value, dtype):
        if dtype == DataPolicy.ArrayFloat:
            return dtype.numpy(value).copy()
        elif dtype == DataPolicy.ArrayInt:
            return value.copy()
        else:
            raise TypeError(f"ArrayInt cannot be converted to type {dtype}")

class ArrayFloat(BasePolicy):
    data_type = DataPolicy.ArrayFloat
    description = "Data type to hold variables lists as floats"
    numpy = np.float64
    is_array = True
    permitted_conversions = [DataPolicy.ArrayInt]

    @classmethod
    def _convert(cls, value, dtype):
        if dtype == DataPolicy.ArrayInt:
            return dtype.numpy(np.round(value)).copy()
        elif dtype == DataPolicy.ArrayFloat:
            return value.copy()
        else:
            raise TypeError(f"ArrayFloat cannot be converted to type {dtype}")

class ValueString(BasePolicy):
    data_type = DataPolicy.ValueString
    description = "Data type to hold variables lists as floats"
    numpy = str

