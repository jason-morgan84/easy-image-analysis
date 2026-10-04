import numpy as np
from core.constants import DataType
from core.shape import Shape


class ImageMetadata:
    def __init__(self, dtype, image_shape_constraints = None, image_map = None):
        self.dtype = dtype
        self.image_shape_constraints = image_shape_constraints
        self.image_map = image_map

    @property
    def dtype(self):
        return self._dtype
    @dtype.setter
    def dtype(self, typ):
        # check that dtype is a member of DataType.image_types (although the pixel_array isn't of a custom class, this is still used to define the expected
        # numpy data type of pixel_array)
        if typ not in DataType.image_types():
            raise TypeError(f"expected type from DataType.image_type, got: {typ} ")
        self._dtype = typ

    # check that image_shape_constraints is of type Shape
    @property 
    def image_shape_constraints(self):
        return self._image_shape_constraints
    @image_shape_constraints.setter
    def image_shape_constraints(self, shp):
        if not isinstance(shp, Shape) and shp is not None:
            raise TypeError(f"for ImageMetadata class, expected image_shape_constraints to be of class Shape, got {type(shp)}")
        self._image_shape_constraints = shp.copy() if shp is not None else None

    # check that image_map is of type Shape
    @property
    def image_map(self):
        return self._image_map
    @image_map.setter
    def image_map(self, map):
        if not isinstance(map, Shape) and map is not None:
            raise TypeError(f"for ImageMetadata class, expected image_map to be of class Shape, got {type(map)}")
        self._image_map = None if map is None else map.copy()


# simple class to hold parameter inputs and outputs
class ParameterMetadata:
    def __init__(self, dtype, shape = None, user_input = False, ui_element = None, ui_element_options = None):
        self.dtype = dtype
        self.shape = shape                              # array shape where dtype is an array_type
        self.user_input = user_input                    # flag for user input - if True, expect parameter via UI not through graph input
        self.ui_element = ui_element                    # definition of UI element required for user input, if relevant
        self.ui_element_options = ui_element_options    # any options associated with that UI element (such as min/max values for sliders, list options for lists)        

    type_name = "ParameterParcel"

    @property
    def dtype(self):
        return self._dtype
    @dtype.setter
    def dtype(self, typ):
        # check that dtype is a member of DataType.array_types/value_types (although the pixel_array isn't of a custom class, this is still used to define the expected
        # numpy data type of pixel_array)
        if typ not in DataType.array_types() and typ not in DataType.value_types():
            raise TypeError(f"expected type from DataType.value_type or DataType.array_type, got: {typ} ")
        self._dtype = typ

    @property
    def shape(self):
        return self._shape
    @shape.setter
    def shape(self, shp):
        if not isinstance(shp, (np.ndarray,list,tuple)) and shp is not None:
            raise TypeError(f"Parameter array shape expected as tuple, list or np.ndarray, got {type(shp)}")

        #if shape is a np array, set as copy of array, else convert to np array
        self._shape = shp.copy() if isinstance(shp, np.ndarray) else np.array(shp).copy()

    @property
    def user_input(self):
        return self._user_input
    @user_input.setter
    def user_input(self, flag):
        # check that flag is boolean
        if not isinstance(flag, bool):
            raise TypeError(f"user_input flag expected to be boolean, not {type(flag)}")
        self._user_input = flag

    @property
    def ui_element(self):
        return self._ui_element
    @ui_element.setter
    def ui_element(self, element):
        # check if user_input flag is set, check ui_element exists
        if self.user_input:
            if element == None:
                raise ValueError(f"defined UI element required where user_input flag is True")
        self._ui_element = element