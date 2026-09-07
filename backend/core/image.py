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
        # for each dimension, check that if, for example, image shape says channel c has size 4 and image mapping says channel c maps to array dimension 0,
        # array dimension 0 also has size 4, else return ValueError
        
        array_shape = self.array.value.shape
        for dimension in Shape.dimensions:
            dimension_array_shape = array_shape[getattr(map, dimension)]
            dimension_image_shape = getattr(self.image_shape,dimension)
            if dimension_array_shape != dimension_image_shape:
                raise ValueError (f"{dimension} dimension of size {dimension_image_shape} is mapped to array dimension of size {dimension_array_shape}")

        self._image_mapping = map

    def transpose(self, new_shape):

        # expect a list/tuple with four, non-duplicate string elements which are members of Shape.dimension_order
        if not isinstance(new_shape, tuple) and not isinstance(new_shape,list):
            raise TypeError (f"Expected tuple/list of channel names, got {type(new_shape)}")

        if len(new_shape)>Shape.max_image_dimensions or len(new_shape)<Shape.min_image_dimensions:
            raise ValueError (f"Expected 4 channel names, got {len(new_shape)}")

        if (len(new_shape)!=len(set(new_shape))):
            raise ValueError ("List/tuple describing new shape contains duplicate dimensions")

        if not isinstance(new_shape[0],str):
            raise TypeError (f"Expected tuple/list of strings, got {type(new_shape[0])}")

        for item in new_shape:
                if not any(dim == item.lower() for dim in Shape.dimensions):
                    raise ValueError (f"List/tuple describing new shape contains incorrect dimension {item} dimensions")


        transpose =[]
        new_map = []

        # receives input of new channel order, such as z,c,y,x
        # to use numpy transpose, needs to go from string z to array map for that dimension and append to list transpose
        # transpose used as input for np.transpose


        #for n, item in enumerate(new_shape):
        #    for dim in self.image_mapping:
        #        if Shape.dimensions[dim] == item.lower():
        #            transpose.append(dim)

        # convert new dimension order in new_shape as strings to same order in transpose as integers
        transpose = [self.image_mapping[item] for item in new_shape]

        # get new shape map - ie, get the position of c,z,y,x in new_shape
        shape_index_lookup = {item.lower(): idx for idx, item in enumerate(new_shape)}
        new_map = [shape_index_lookup[item] for item in Shape.dimensions]

        
        transposed_array = np.transpose(self.array.to_numpy(),transpose)

        return Image(array = self.array_dtype(transposed_array),
                     array_dtype = self.array_dtype,
                     image_shape = self.image_shape,
                     #image_shape = Shape(*transposed_array.shape),
                     image_mapping = Shape(*new_map))




        
        







