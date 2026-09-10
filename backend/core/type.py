import numpy as np
import numbers
from core.constants import DataType



class ImageInt:
    data_type = DataType.ImageInt
    numpy = np.uint8
    description = "Data type to hold multi-dimensional arrays for images as integers in the range 0 - 255 inclusive"

    def __init__(self, value):
        self.value = value

    def __getitem__(self, index):
        return self.value[index]

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):

        # checks whether val is a member of any of another type defined as an image_types in constants.py
        value_dtype = getattr(val, "data_type", None)
        if value_dtype in DataType.image_types() and value_dtype != ImageInt:
            # if it is, call relevant function converting to int
            val = val.to_ImageInt()
        else:
            # if not an np.array or list, give type error
            if not isinstance(val, np.ndarray):
                if not isinstance(val, list):
                    raise TypeError (f"Expected list or np.array, got {type(val)}")

                # if its a list, convert to np.array
                val = np.array(val)
            else:
                # if it is a np array, create a copy; for lists, conversion to np.array is sufficient for immutability but np.arrays need to be copied
                val = val.copy()
            
            # if elements aren't integers or np.integers, type error
            if not np.issubdtype(val.dtype, np.integer):
                raise TypeError (f"Expected integer, got {val.dtype}")

            # if it contains elements > 255 or < 0, value error
            if val.max() > 255 or val.min() < 0:
                raise ValueError(f"Value out of bounds (must be 0-255)")
        
        self._value = val

    # returns a test variable of size "shape" of random integers between 0 and 255
    def test_sample(shape, zero = False):
        if not isinstance(shape, list) and not isinstance(shape, tuple):
            raise TypeError(f"Expected shape as list or tuple, got  {type(shape)}")
        elif not isinstance(shape[0],int) and not isinstance(shape[0],np.integer):
            raise TypeError(f"Expected shape as as integers, got  {type(shape[0])}")
        elif zero == True:
            return ImageInt(np.uint8(np.zeros(shape)))
        else:
            return ImageInt(np.random.randint(low=0, high=255, size=shape))

    @property
    def shape(self):
        return self.value.shape

    def to_ImageFloat(self):
        return ImageFloat(self.value/255)

    def to_ImageBinary(self):
        return ImageBinary(self.value)

    def to_numpy(self):
        return np.array(self.value, self.numpy)

    def to_uint8(self):
        return np.array(self.value,np.uint8)

class ImageFloat:
    data_type = DataType.ImageFloat
    numpy = np.float64
    description = "Data type to hold multi-dimensional arrays for images as floats in the range 0 - 1 inclusive"

    def __init__(self, value):
        self.value = value

    def __getitem__(self, index):
        return self.value[index]

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        # checks whether input val is a member of any of the Image data types defined as image_types in constants.py
        value_dtype = getattr(val, "data_type", None)
        if value_dtype in DataType.image_types() and value_dtype != ImageFloat:
            # if it is, call relevant function converting to int
            val = val.to_ImageFloat()
        else:
            # if not an np.array or list, give type error
            if not isinstance(val, np.ndarray):
                if not isinstance(val, list):
                    raise TypeError (f"Expected list or np.array, got {type(val)}")
                # if its a list, convert to np.array
                val = np.array(val)
            else:
                # if it is a np array; for lists, conversion to np.array is sufficient for immutability but np.arrays need to be copied
                val = val.copy()
            # if elements aren't integers or np.integers, type error
            if not np.issubdtype(val.dtype, np.number):
                raise TypeError (f"Expected number, got {val.dtype}")
            
            # if it contains elements > 1 or < 0, value error
            if val.max() > 1 or val.min() < 0:
                raise ValueError(f"Value out of bounds (must be 0-1)")
        
        self._value = val

    # returns a test variable of size "shape" of random integers between 0 and 1
    def test_sample(shape, zero = False):
        if not isinstance(shape, list) and not isinstance(shape, tuple):
            raise TypeError(f"Expected shape as list or tuple, got  {type(shape)}")
        elif not isinstance(shape[0],int) and not isinstance(shape[0],np.integer):
            raise TypeError(f"Expected shape as as integers, got  {type(shape[0])}")
        elif zero == True:
            return ImageFloat(np.zeros(shape))
        else:
            return ImageFloat(np.random.random(size=shape))

    @property
    def shape(self):
        return self.value.shape

    def to_ImageInt(self):
        return ImageInt(np.uint8(np.round(self.value * 255)))

    def to_ImageBinary(self):
        return ImageBinary(self.value)

    def to_numpy(self):
        return np.array(self.value,self.numpy)

    def to_float64(self):
        return np.array(self.value,np.float64)

class ImageBinary:

    data_type = DataType.ImageBinary
    numpy = np.uint8
    description = "Data type to hold multi-dimensional arrays for images as either 1 or 0"

    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):

        # checks whether input val is a member of any of the Image data types defined as image_types in constants.py
        value_dtype = getattr(val, "data_type", None)
        if value_dtype in DataType.image_types() and value_dtype != ImageBinary:
            # if it is, call relevant function converting to int
            val = val.to_ImageBinary()
        else:
            # if not an np.array or list, give type error
            if not isinstance(val, np.ndarray):
                if not isinstance(val, list):
                    raise TypeError (f"Expected list or np.array, got {type(val)}")
                
                # if its a list, convert to np.array
                val = np.array(val)
            else:
                # if it is a np array; for lists, conversion to np.array is sufficient for immutability but np.arrays need to be copied
                val = val.copy()

            # if elements aren't integers or np.integers, type error
            if not np.issubdtype(val.dtype, np.number):
                raise TypeError (f"Expected number, got {val.dtype}")
            
            # if it contains elements > 255 or < 0, value error
            if np.any(~np.isin(val, [0, 1])):
                raise ValueError(f"Value out of bounds (must be 0 or 1)")
        
        self._value = val

    # returns a test variable of size "shape" of random integers either 0 or 1
    def test_sample(shape, zero = False):
        if not isinstance(shape, list) and not isinstance(shape, tuple):
            raise TypeError(f"Expected shape as list or tuple, got  {type(shape)}")
        elif not isinstance(shape[0],int) and not isinstance(shape[0],np.integer):
            raise TypeError(f"Expected shape as as integers, got  {type(shape[0])}")
        elif zero == True:
            return ImageBinary(np.uint8(np.zeros(shape)))
        else:
            return ImageBinary(np.random.randint(low=0, high=1, size=shape))

    @property
    def shape(self):
        return self.value.shape

    def to_ImageFloat(self):
        return ImageFloat(self.value)

    def to_ImageInt(self):
        return ImageInt(self.value)

    def to_numpy(self):
        return np.array(self.value,self.numpy)

    def to_uint8(self):
        return np.array(self.value,np.uint8)

    def to_boolean(self):
        return np.array(self.value,np.bool)

class ValueInt:

    data_type = DataType.ValueInt
    numpy = np.uint8
    description = "Data type to hold single variables as integers"

    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self,val):
        value_dtype = getattr(val, "data_type", None)
        if value_dtype in DataType.value_types() and value_dtype != ValueInt:
            # if it is, call relevant function converting to int
            val = val.to_ValueInt()
        else:

            if not isinstance(val,int) and not isinstance(val,np.integer):
                raise TypeError (f"Expected integer, got {type(val)}")
            self._value = val


    # returns a test variable
    def test_sample(zero = False):
        if zero:
            return ValueInt(0)
        else:
            return ValueInt(np.random.randint(low = 0, high = 255))

    def to_ValueFloat(self):
        return ValueFloat(self.value)

    def to_numpy(self):
        return self.numpy(self.value)

    def to_uint8(self):
        return np.uint8(self.value)

class ValueFloat:

    data_type = DataType.ValueFloat
    numpy = np.float64
    description = "Data type to hold single variables as floats"

    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self,val):
        value_dtype = getattr(val, "data_type", None)
        if value_dtype in DataType.value_types() and value_dtype != ValueFloat:
            # if it is, call relevant function converting to int
            val = val.to_ValueFloat()
        else:
            if not isinstance(val,(np.number,numbers.Number)):
                raise TypeError ("Value must be a number.")
            self._value = np.float64(val)

    # returns a test variable
    def test_sample(zero = False):
        if zero:
            return ValueFloat(0)
        else:
            return ValueFloat(np.random.random())

    def to_ValueInt(self):
        return ValueInt(round(self.value))

    def _to_numpy(self):
        return self.numpy(self.value)

    def to_float64(self):
        return np.float64(self.value)

     