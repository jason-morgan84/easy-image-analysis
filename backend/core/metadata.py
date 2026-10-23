import numpy as np
from core.constants import DataPolicy
from core.shape import Shape


class ImageMetadata:
    def __init__(self, dtype, image_shape_constraints, image_map):
        self.dtype = dtype
        self.image_shape_constraints = image_shape_constraints
        self.image_map = image_map

    @property
    def dtype(self):
        return self._dtype
    @dtype.setter
    def dtype(self, typ):
        # check that dtype is a member of DataType.types and that dtype is_image flag is set to True
        if typ not in DataPolicy.policies():
            raise TypeError(f"expected ImageMetadata dtype from DataType.types: {typ} ")
        if typ.is_image is not True:
            raise TypeError(f"expected ImageMetadata dtype to have is_image flag set to True")
        self._dtype = typ

    # check that image_shape_constraints is of type Shape
    @property 
    def image_shape_constraints(self):
        return self._image_shape_constraints
    @image_shape_constraints.setter
    def image_shape_constraints(self, shp):
        if not isinstance(shp, Shape):
            raise TypeError(f"expected ImageMetadata image_shape_constraints to be of class Shape, got {type(shp)}")
        self._image_shape_constraints = shp.copy()
        
    # check that image_map is of type Shape
    @property
    def image_map(self):
        return self._image_map
    @image_map.setter
    def image_map(self, map):
        if not isinstance(map, Shape):
            raise TypeError(f"expected ImageMetadata image_map to be of class Shape, got {type(map)}")
        self._image_map = map.copy()


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
        # check that dtype is a member of DataType.types and dtype is_image flag is set to False
        if typ not in DataPolicy.policies():
            raise TypeError(f"expected ParameterMetadata dtype from DataType.types, got: {typ} ")
        if typ.is_image is True:
            raise TypeError(f"expected ParameterMetadata dtype to have is_image flag set to False")
        self._dtype = typ

    @property
    def shape(self):
        return self._shape
    @shape.setter
    def shape(self, shp):
        if not isinstance(shp, (np.ndarray,list,tuple)) and shp is not None:
            raise TypeError(f"expected ParameterMetadata shape as tuple, list or np.ndarray, got {type(shp)}")

        #if shape is a np array, set as copy of array, else convert to np array
        if shp is not None:
            self._shape = shp.copy() if isinstance(shp, np.ndarray) else np.array(shp).copy()
        else:
            self._shape = None

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