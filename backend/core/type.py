import numpy as np
import numbers
from core.constants import DataType



class ImageInt:
    data_type = DataType.ImageInt
    def __init__(self, value):
        self.value = value

    def __getitem__(self, index):
        return self.value[index]

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        if not isinstance(val, np.ndarray):
            if not isinstance(val, list):
                raise TypeError (f"Expected list or np.array, got {type(val)}")
        val = np.array(val)

        if not np.issubdtype(val.dtype, np.integer):
            raise TypeError (f"Expected integer, got {val.dtype}")
        
        if val.max() > 255 or val.min() < 0:
            raise ValueError(f"Value out of bounds (must be 0-255)")
        
        self._value = val

    @property
    def shape(self):
        return self.value.shape

    def to_ImageFloat(self):
        return ImageFloat(self.value/255)

    def to_ImageBinary(self):
        return ImageBinary(self.value)

    def to_uint8(self):
        return np.array(self.value,np.uint8)

class ImageFloat:
    data_type = DataType.ImageFloat

    def __init__(self, value):
        self.value = value

    def __getitem__(self, index):
        return self.value[index]

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        if not isinstance(val, np.ndarray):
            if not isinstance(val, list):
                raise TypeError (f"Expected list or np.array, got {type(val)}")
        val = np.array(val)

        if not np.issubdtype(val.dtype, np.number):
            raise TypeError (f"Expected number, got {val.dtype}")
        
        if val.max() > 1 or val.min() < 0:
            raise ValueError(f"Value out of bounds (must be 0-1)")
        
        self._value = val

    @property
    def shape(self):
        return self.value.shape

    def to_ImageInt(self):
        return ImageInt(np.uint8(np.round(self.value * 255)))

    def to_ImageBinary(self):
        return ImageBinary(self.value)

    def to_float64(self):
        return np.array(self.value,np.float64)

class ImageBinary:

    data_type = DataType.ImageBinary
    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        if not isinstance(val, np.ndarray):
            if not isinstance(val, list):
                raise TypeError (f"Expected list or np.array, got {type(val)}")
        val = np.array(val)

        if not np.issubdtype(val.dtype, np.number):
            raise TypeError (f"Expected number, got {val.dtype}")
        
        if np.any(~np.isin(val, [0, 1])):
            raise ValueError(f"Value out of bounds (must be 0 or 1)")
        
        self._value = val

    @property
    def shape(self):
        return self.value.shape

    def to_ImageFloat(self):
        return ImageFloat(self.value)

    def to_ImageInt(self):
        return ImageInt(self.value)

    def to_uint8(self):
        return np.array(self.value,np.uint8)

    def to_boolean(self):
        return np.array(self.value,np.bool)

class ValueInt:

    data_type = DataType.ValueInt

    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self,val):
        if not isinstance(val,int):
            raise TypeError (f"Expected integer, got {type(val)}")
        self._value = val

    def to_ValueFloat(self):
        return ValueFloat(self.value)

    def to_uint8(self):
        return np.uint8(self.value)

class ValueFloat:

    data_type = DataType.ValueFloat

    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self,val):
        if not isinstance(val,(np.number,numbers.Number)):
            raise TypeError ("Value must be a number.")
        self._value = np.float64(val)

    def to_ValueInt(self):
        return ValueInt(round(self.value))

    def to_float64(self):
        return np.float64(self.value)

     