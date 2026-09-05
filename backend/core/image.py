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
            # check array is of one of the acceptable data types
            if arr.data_type not in DataType.image_types:
                raise TypeError (f"Expected Image data type (see constants.py) got {type(arr)}")

            self._array = arr

        @property
        def array_dtype(self):
            return self._array_dtype

        @array_dtype.setter
        def array_dtype(self, dtype):
            # check dtype matches array type
            if dtype != self.array.data_type:
                raise TypeError (f"array_dtype {dtype} does not match array data type {type(self.array)}")

        @property 
        def image_shape(self):
            return self._image_shape

        @image_shape.setter
        def image_shape(self, shape):
            # checks the number of defined image dimensions in image_shape matches the size of the array
            ndim += sum(1 for item in [image_shape.c, image_shape.z, image_shape.y, image_shape.x] if item > 0)
            array_shape = len(self.array.value.shape)

            # give ValueError if they don't match
            if (ndim != array_shape):
                raise ValueError (f"image_shape {shape} defines {ndim} dimensions but array contains {array_shape}")




