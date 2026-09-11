import numpy as np
import numbers
from core.constants import DataType


class BaseType:
    """ Create new DataTypes based on this framework.
    Each new DataType must have data_type, numpy and allowed_sub_types set.
    min_value, max_value and is_array can be set based on requirements.
    
    For conversions between classes, override the default 'to' function in the new class.
    Attempts to convert between classes where type conversions have not been explicitly coded will result in an error message."""

    data_type = None            # reference to this data type in DataType enum in constant.py
    numpy = None                # default numpy equivalent data_type   
    description = None          # text description of class and what its for
    allowed_sub_types = None    # tuple of allowed data types eg (np.integers, int)
    min_value = None            # minimum allowed value, if defined
    max_value = None            # maximum allowed value, if defined
    is_array = False            # type classes must define either an 1d or multi-dimensional data type.

    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self,val):
        # if val is already a member of a DataType class but is not the current data type class, call self.to(self.data_type) function for implicit conversion
        value_dtype = getattr(val, "data_type", None)
        if isinstance(value_dtype,DataType) and value_dtype != self.data_type:
            val = val.to(self.data_type)
        else:
            # defines different validation methods is data type is an array (is_array = True) or not (is_array = False)
            if self.is_array:
                self.validate_array()
            else:
                self.validate_scalar()

    def validate_array(self, val):
        # if input value is not a np array, list or tuple then give error
        if not isinstance(val, (np.ndarray, list, tuple)):
            raise TypeError (f"Expected list or np.array, got {type(val)}")
        # if a collection but not np.array, convert to np.array, else copy the np.array
        # this is required for immutability
        val = np.array(val) if isinstance(val, (list,tuple)) else val.copy()

        # if array members are not one of the allowed data subtypes, give type error
        if not np.issubdtype(val.dtype, self.allowed_sub_types):
            raise TypeError (f"Expected {self.allowed_sub_types}, got {val.dtype}")

        # if min and max values are defined, check value is within the boundaries else give error
        # these are explicit boundaries and not constraints - an error is given if unacceptable data is passed in, data is not changed to be within boundaries
        if ((self.min_value != None and val.min() < self.min_value) or 
            (self.max_value != None and val.max() > self.max_value)):
                raise ValueError(f"Value out of bounds (must be {self.min_value}-{self.max_value})")
            
        self._value = val

    def validate_scalar(self, val):
        # check value is a an allowed sub type
        if not isinstance(val, self.allowed_sub_types):
            raise TypeError (f"Expected {self.allowed_sub_types}, got {type(val)}")

        # check value is within range, if appropriate
        if self.min_value != None and self.max_value!=None:
            if val > self.max_value or val < self.min_value:
                raise ValueError(f"Value out of bounds (must be {self.min_value}-{self.max_value})")

    def to_numpy(self):
        if self.is_array:
            return np.array(self.value, self.numpy)
        else:
            return self.numpy(self.value)

    def to(self, dtype):
        raise NotImplementedError(f"Type conversions not yet implemented for data type {self.data_type}")

class ImageInt(BaseType):
    data_type = DataType.ImageInt
    description = "Data type to hold multi-dimensional arrays for images as integers in the range 0 - 255 inclusive"
    numpy = np.uint8
    is_array = True
    min_val = 0
    max_val = 255
    allowed_subdtypes = (np.integer, int)

    def to(self, dtype):
        if dtype == DataType.ImageFloat:
            return ImageFloat(self.value/255)
        elif dtype == DataType.ImageBinary:
            return ImageBinary(self.value)
        else:
            raise TypeError(f"ImageInt cannot be converted to type {dtype}")

class ImageFloat(BaseType):
    data_type = DataType.ImageFloat
    description = "Data type to hold multi-dimensional arrays for images as floats in the range 0 - 1 inclusive"
    numpy = np.float64
    is_array = True
    min_val = 0
    max_val = 1
    allowed_subdtypes = (numbers.Number, np.number)

    def to(self, dtype):
        if dtype == DataType.ImageInt:
            return ImageInt(np.uint8(np.round(self.value * 255)))
        elif dtype == DataType.ImageBinary:
            return ImageBinary(self.value)
        else:
            raise TypeError(f"ImageFloat cannot be converted to type {dtype}")

class ImageBinary(BaseType):
    data_type = DataType.ImageBinary
    description = "Data type to hold multi-dimensional arrays for images as either 1 or 0"
    numpy = np.uint8
    is_array = True
    min_val = 0
    max_val = 1
    allowed_subdtypes = (int, np.integer, np.bool, bool)

    def to(self, dtype):
        if dtype == DataType.ImageFloat:
            return ImageFloat(self.value)
        elif dtype == DataType.ImageInt:
            return ImageInt(self.value)
        else:
            raise TypeError(f"ImageBinary cannot be converted to type {dtype}")
        
class ValueInt(BaseType):
    data_type = DataType.ValueInt
    description = "Data type to hold single variables as integers"
    numpy = np.uint8
    allowed_subdtypes = (int, np.integer)

    def to(self, dtype):
        if dtype == DataType.ValueFloat:
            return ValueFloat(self.value)
        else:
            raise TypeError(f"ValueInt cannot be converted to type {dtype}")

class ValueFloat(BaseType):
    data_type = DataType.ValueFloat
    description = "Data type to hold single variables as floats"
    numpy = np.float64
    allowed_subdtypes = (numbers.Number, np.number)

    def to(self, dtype):
        if dtype == DataType.ValueInt:
            return ValueInt(round(self.value))
        else:
            raise TypeError(f"ValueFloat cannot be converted to type {dtype}")

class ArrayInt(BaseType):
    data_type = DataType.ArrayInt
    description = "Data type to hold variables lists as ints"
    numpy = np.uint8
    allowed_subdtypes = (int, np.integer)

    def to(self, dtype):
        if dtype == DataType.ArrayFloat:
            return ArrayFloat(self.value)
        else:
            raise TypeError(f"ArrayInt cannot be converted to type {dtype}")

class ArrayFloat(BaseType):
    data_type = DataType.ArrayFloat
    description = "Data type to hold variables lists as floats"
    numpy = np.float64
    allowed_subdtypes = (numbers.Number, np.number)

    def to(self, dtype):
        if dtype == DataType.ArrayInt:
            return ArrayInt(round(self.value))
        else:
            raise TypeError(f"ArrayFloat cannot be converted to type {dtype}")

def sample_data(dtype, shape = None, zero = False):
    # used for generating sample data sets of given type
    if not isinstance(dtype, DataType):
        raise TypeError (f"Expected Image data type (see constants.py) got {dtype}")
    if dtype.is_array:
        if shape == None:
            raise TypeError (f"Array data type ({dtype}) supplied without shape")
        if zero:
            return dtype(dtype.numpy(np.zeros(shape)))
        else:
            range = dtype.max_value - dtype.min_value
            random_array = np.random.random(size = shape) # gives random array between 0 and 1 of desired shape
            random_array = (random_array * range) + dtype.min_value # gets array between min and max values
            return dtype(dtype.numpy(random_array)) # returns array in correct format
    else:
        if zero:
            return dtype(dtype.numpy(0))
        else:
            range = dtype.max_value - dtype.min_value
            return dtype(dtype.numpy(np.random.random() * range + dtype.min_value))