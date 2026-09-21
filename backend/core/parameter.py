"""### 3.2.4 Parameters Class
The parameter class holds information for ImageOperations defining the required inputs, from the user and from the workflow.
The aim is to allow data to be passed to and from an ImageOperation in the relevant standard numpy formats, and, where user input is required,
to have the necessary information for the frontend to automatically create a dialogue box for the user to enter values,
without each ImageOperation requiring its own hardcoded UI elements. """

from core.constants import DataType
import numpy as np

class Parameter:
    def __init__ (self, name, value, ui_element = None, ui_element_options = None):

        self.name = name # name of the parameter
        self.value = value # value of parameter
        self.ui_element = ui_element # definition of UI element required for user input, if relevant
        self.ui_element_options = ui_element_options # any options associated with that UI element (such as min/max values for sliders, list options for lists)

    # checks that value is of DataType.value_type or DataType.array_type classes
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):

        if not val in DataType.value_types and not val in DataType.array_types:
            raise TypeError (f"Expected type member of DataType.value_types or DataType.array_types, got{type(val)}")
           
        self._value = val

