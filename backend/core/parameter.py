"""### 3.2.4 Parameters Class
The parameter class holds information for ImageOperations defining the required inputs, from the user and from the workflow.
The aim is to allow data to be passed to and from an ImageOperation in the relevant standard numpy formats, and, where user input is required,
to have the necessary information for the frontend to automatically create a dialogue box for the user to enter values,
without each ImageOperation requiring its own hardcoded UI elements. """

from core.constants import DataType


class Parameter:
    def __init__ (self, name, value):

        self.name = name # name of the parameter
        self.value = value # value of parameter
        

    # checks that value is of DataType.value_type or DataType.array_type classes
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        try:
            val_dtype = getattr(val,"data_type")
        except:
            raise TypeError(f"Expected type member of DataType, got{type(val)}")
        
        if not val_dtype in DataType.value_types() and not val_dtype in DataType.array_types():
            raise TypeError (f"Expected type member of DataType.value_types or DataType.array_types, got{type(val)}")
           
        self._value = val

