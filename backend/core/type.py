import numpy as np

class ImageInt:
    def __init__(self, value:int):
        self.value = value

    @property
    def value(self) -> int:
        return self.value

    @value.setter
    def value(self,val:int):
        if not isinstance(val,int):
            raise TypeError (f"Expected integer, got {type(val)}")
        if not (0<=val<=255):
            raise ValueError(f"Value {val} out of bounds (must be 0-255)")
        self.value = val

    def to_ImageFloat(self):
        return ImageFloat(self.value/255)

    def to_ImageBinary(self):
        return ImageBinary(self.value)

    def to_uint8(self):
        return self.value.astype(np.uint8)

class ImageFloat:
    def __init__(self, value:float):
        self.value = value

    @property
    def value(self) -> float:
        return self.value

    @value.setter
    def value(self,val:int):
        if not isinstance(val,float):
            raise TypeError ("Value must be a float.")
        if not (0<=val<=1):
            raise ValueError(f"Value {val} out of bounds (must be 0-1)")
        self.value = val

    def to_ImageInt(self):
        return ImageInt(round(self.value * 255))

    def to_ImageBinary(self):
        return ImageBinary(self.value)

    def to_float64(self):
        return self.value.astype(np.float64)


class ImageBinary:
    def __init__(self, value:int):
        self.value = value

    @property
    def value(self) -> int:
        return self.value

    @value.setter
    def value(self,val:int):
        if not isinstance(val,int):
            raise TypeError ("Value must be an integer.")
        if not (0<=val<=1):
            raise ValueError(f"Value {val} out of bounds (must be 0 or 1)")
        self.value = val

    def to_ImageFloat(self):
        return ImageFloat(self.value)

    def to_ImageInt(self):
        return ImageInt(self.value)

    def to_uint8(self):
        return self.value.astype(np.uint8)

    def to_boolean(self):
        return self.value.astype(np.bool)