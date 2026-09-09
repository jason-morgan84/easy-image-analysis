"""### 3.2.4 Parameters Class
The parameter class holds information for ImageOperations defining the required inputs, from the user and from the workflow.
The aim is to allow data to be passed to and from an ImageOperation in the relevant standard numpy formats, and, where user input is required,
to have the necessary information for the frontend to automatically create a dialogue box for the user to enter values,
without each ImageOperation requiring its own hardcoded UI elements. """

from core.constants import DataType
from core.shape import Shape
import numpy as np

class Parameter:
    def __init__ (self, name, dtype, value = 0, shape = None, ui_element = None, ui_element_options = None):
        self.name = name # name of the parameter
        self.dtype = dtype # relevant data type from DataType
        self.value = value # value of parameter
        self.shape = shape
        self.ui_element = ui_element # definition of UI element required for user input, if relevant
        self.ui_element_options = ui_element_options # any options associated with that UI element (such as min/max values for sliders, list options for lists)

    @property
    def dtype(self):
        return self._dtype

    # checks that dtype is in DataType
    @dtype.setter
    def dtype(self, type):
        if type not in DataType.value_types() and type not in DataType.image_types():
            raise TypeError (f"For dtype, expected a DataType member, got {type}")
        self._dtype = type

    # checks that shape is of Shape class
    @property
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, shp):
        if self.dtype in DataType.image_types():
            if not isinstance(shp, Shape):
                raise TypeError (f"For shape, expected Shape class, got {type(shp)}")
        self._shape = shp



    # Because the Parameter class deals with inputs and outputs to ImageOperations, which work with standard numpy data types, 
    # type checking for "value" is to ensure it is of type DataType.dtype.numpy.
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        if self.dtype in DataType.image_types():
            if not isinstance(val, np.ndarray):
                raise TypeError (f"For dtype {self.dtype}, expected np.ndarray, got{type(val)}")
            if not isinstance(val[0],self.dtype.numpy):
                raise TypeError (f"For dtype {self.dtype}, expected array of {self.dtype.numpy}, got {type(val[0])}")
            if (self.shape == None):
                raise ValueError (f"For dtype {self.dtype}, array shape is expected")
        elif self.dtype in DataType.value_types():
            if not isinstance(val,self.dtype.numpy):
                raise TypeError (f"For dtype {self.dtype}, expected {self.dtype.numpy}, got {type(val)}")
            
        self._value = val

