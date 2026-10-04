import numpy as np
from core.constants import DataType
from core.shape import Shape
from core.metadata import ImageMetadata

class Image:
    def __init__(self, data, image_metadata):
        self.data = data                            # the multi-dimensional array that holds the pixel data
        self.image_metadata = image_metadata        # image_map of image dimensions (c,z,y,x) to Array dimensions (0,1,2,3 etc)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        # check data is of one of the acceptable data types defined by DataType.image_types() in constants.py
        dtype = getattr(value, "data_type", None)

        if dtype not in DataType.image_types() or dtype == None:
            raise TypeError (f"expected data of image_type data type (see constants.py) got {type(value)}")

        # check array has correct number of dimensions
        array_size = len(value.value.shape)
        if array_size > Shape.max_image_dimensions or array_size < Shape.min_image_dimensions:
            raise ValueError (f"image array should have {Shape.min_image_dimensions}-{Shape.max_image_dimensions} dimensions but has {array_size}")

        self._pixel_array = value

    @property
    def image_metadata(self):
        return self._image_metadata

    @image_metadata.setter
    def image_metadata(self, meta):
        if not isinstance(meta, ImageMetadata):
            raise TypeError (f"Expected image_metadata of Image Metadata class, got {type(map)}")
        # check image_map is a Shape class

        self._image_metadata = meta

    def get_image_shape(self):
        return Shape(c = self.pixel_array.value.shape[self.image_map.c],
                     z = self.pixel_array.value.shape[self.image_map.z],
                     y = self.pixel_array.value.shape[self.image_map.y],
                     x = self.pixel_array.value.shape[self.image_map.x])

    def convert(self, convert):
        if convert not in DataType.image_types():
            raise TypeError(f"images can only be converted to image_types, not {convert}")
        return Image(data = self.data.to(convert), image_metadata = self.image_metadata)

    # tranpose to be moved to WorkFlow
    def transpose(self, new_shape):
        # expect a Shape class
        if not isinstance(new_shape, Shape):
            raise TypeError (f"expected Shape class, got {type(new_shape)}")

        for item in new_shape:
            if item < 0 or item > Shape.max_image_dimensions:
                raise ValueError (f"passed shape dimensions out of range, must be 0-{Shape.max_image_dimensions}")


        # receives Shape class member with new dimensions indices of each array (c,z,y,x)
        # needs to create transpose list with values c,z,y,x in order of old_c,old_z,old_y,old_x
        transpose = [self.data[item] for item in new_shape]

        # receives input of new channel order, such as z,c,y,x
        # to use numpy transpose, needs to go from string z to array map for that dimension and append to list transpose
        # transpose used as input for np.transpose

        # get new shape map - ie, get the position of c,z,y,x in new_shape
        
        transposed_array = np.transpose(self.data.to_numpy(),transpose)

        current_dtype = getattr(self.data, "data_type")

        #self.pixel_array = current_dtype(transposed_array)
        #self.image_map = new_shape
        return Image(data = current_dtype(transposed_array),
                     image_metadata = ImageMetadata(dtype = self.image_metadata.dtype,
                                                    image_shape_constraints = self.image_metadata.image_shape_constraints,
                                                    image_map = new_shape))






        
        







