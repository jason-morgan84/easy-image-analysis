import numpy as np
from core.constants import DataType
from core.shape import Shape

class Image:
    def __init__(self, pixel_array, image_map):
        self.pixel_array = pixel_array                      # the multi-dimensional array that holds the pixel data
        self.image_map = image_map                          # mapping of image dimensions (c,z,y,x) to Array dimensions (0,1,2,3 etc)

    @property
    def pixel_array(self):
        return self._pixel_array

    @pixel_array.setter
    def pixel_array(self, arr):
        # check array is of one of the acceptable data types defined by DataType.image_types() in constants.py
        array_dtype = getattr(arr, "data_type", None)

        if array_dtype not in DataType.image_types() or array_dtype == None:
            raise TypeError (f"Expected Image data type (see constants.py) got {type(arr)}")

        # check array has correct number of dimensions
        array_size = len(arr.value.shape)
        if array_size > Shape.max_image_dimensions or array_size < Shape.min_image_dimensions:
            raise ValueError (f"array should have {Shape.min_image_dimensions}-{Shape.max_image_dimensions} dimensions but has {array_size}")

        self._pixel_array = arr

    @property
    def image_map(self):
        return self._image_map

    @image_map.setter
    def image_map(self, map):
        if not isinstance(map, Shape):
            raise TypeError (f"Expected image_map of Shape class, got {type(map)}")
        # check image_map is a Shape class

        self._image_map = map

    def get_image_shape(self):
        return Shape(c = self.pixel_array.value.shape[self.image_map.c],
                     z = self.pixel_array.value.shape[self.image_map.z],
                     y = self.pixel_array.value.shape[self.image_map.y],
                     x = self.pixel_array.value.shape[self.image_map.x])

    # tranpose to be moved to WorkFlow
    """def transpose(self, new_shape):

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
                     image_mapping = Shape(*new_map))"""




        
        







