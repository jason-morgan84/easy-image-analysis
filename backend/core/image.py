import numpy as np
from core.constants import DataType
from core.shape import Shape

class Image:
    def __init__(self, array, array_dtype, image_shape, image_mapping):
        self.array = array                      # the multi-dimensional array that holds the pixel data
        self.array_dtype = array_dtype          # the DataType used to store the pixel data
        self.image_shape = image_shape          # the shape of the *image* - note: this is distinct from the size of the array
        self.image_mapping = image_mapping      # mapping of image dimensions (c,z,y,x) to Array dimensions (0,1,2,3 etc)

    @property
    def array(self):
        return self._array

    @array.setter
    def array(self, arr):
        # check array is of one of the acceptable data types defined by DataType.image_types() in constants.py
        array_dtype = getattr(arr, "data_type", None)

        if array_dtype not in DataType.image_types() or array_dtype == None:
            raise TypeError (f"Expected Image data type (see constants.py) got {type(arr)}")

        # check array has 4 dimensions
        array_size = len(arr.value.shape)
        if array_size != 4:
            raise ValueError (f"array should have 4 dimensions (c,z,y,x) but has {array_size}")

        self._array = arr

    @property
    def array_dtype(self):
        return self._array_dtype

    @array_dtype.setter
    def array_dtype(self, dtype):
        # check defined array_dtype matches actual array data type
        if dtype != self.array.data_type:
            raise TypeError (f"array_dtype {dtype} does not match array data type {type(self.array)}")

        self._array_dtype = dtype

    @property 
    def image_shape(self):
        return self._image_shape

    @image_shape.setter
    def image_shape(self, shape):
        ndim = 0
        # checks the number of defined image dimensions in image_shape matches the actual size of the array
        ndim += sum(1 for item in shape if item > 0)
        array_size = len(self.array.value.shape)

        # give ValueError if they don't match
        if (ndim != array_size):
            raise ValueError (f"image_shape {shape} defines {ndim} dimensions but array contains {array_size}")

        self._image_shape = shape

    @property
    def image_mapping(self):
        return self._image_mapping

    @image_mapping.setter
    def image_mapping(self, map):
        # check that if, for example, image shape says channel c has size 4 and image mapping says channel c maps to array dimension 0,
        # array dimension 0 also has size 4, else return ValueError
        
        array_shape = self.array.value.shape
        if array_shape[map.c] != self.image_shape.c:
            raise ValueError (f"c dimension of size {self.image_shape.c} is mapped to array dimension of size {array_shape[map.c]}")

        if array_shape[map.z] != self.image_shape.z:
            raise ValueError (f"z dimension of size {self.image_shape.z} is mapped to array dimension of size {array_shape[map.z]}")

        if array_shape[map.y] != self.image_shape.y:
            raise ValueError (f"y dimension of size {self.image_shape.y} is mapped to array dimension of size {array_shape[map.y]}")

        if array_shape[map.x] != self.image_shape.x:
            raise ValueError (f"x dimension of size {self.image_shape.x} is mapped to array dimension of size {array_shape[map.x]}")

        self._image_mapping = map






