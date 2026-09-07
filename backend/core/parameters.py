"""### 3.2.4 Parameters Class
The parameter class holds information for ImageOperations defining the required user inputs (as opposed to image/values inputted via the workflow). The aim is to allow the frontend to automatically create a dialogue box for the user to enter values, without each ImageOperation requiring its own hardcoded UI elements. 
* Name – the name of the parameter
* dtype – the data type of the parameter
* value – its value
* ui_element – the desired UI element for input (text box, drop down box, check box, slider etc)
* ui_element_options – Dictionary of other options related to that UI element (slider min/max, drop down box options etc)."""
from core.constants import DataType

class Parameters:
    def __init__ (self, name, dtype, ui_element, value = 0, ui_element_options = {}):
        self.name = name
        self.dtype = dtype
        self.ui_element = ui_element
        self.value = value
        self.ui_element_options = ui_element_options

    @property
    def dtype(self):
        return self._dtype

    @dtype.setter
    def dtype(self, type):
        if type not in DataType.value_types():
            raise TypeError (f"Expected value_type, got {type}")
        self._dtype = type


    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = self.dtype(val)

