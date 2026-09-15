from core.constants import DataType
from core.shape import Shape
import numpy as np
from dataclasses import dataclass, field
from typing import Any, Optional

"""Note for types: For input type checking, ImageOperation will be a part of a Node. Data will flow into the Node through a Port, which will transmit the data
to the ImageOperation class. 

Ports will carry out type conversions of any inputted data from custom DataTypes used to manage types in data transmission to standard numpy data types
used in actual image analysis.

This means that while input["input_name"].dtype will be of a DataType class, the actual input data will be off DataType.numpy type, and should be checked against
that data type"""

"""Note for shapes: For inputs to ImageOperations, the actual image shape is not strictly defined.

This means that input["input_name"].shape does not give array dimensions, but desired array dimensions - a specific value if a strict size is needed for that
dimension, or -1 if the analysis function is indifferent to size in that dimension."""

# simple class to hold image inputs and outputs
class ImageParcel:
    def __init__(self, dtype, pixel_array = None, shape = None, mapping = None):
        self.dtype = dtype
        self.shape = shape
        self.mapping = mapping
        self.pixel_array = pixel_array

    type_name = "ImageParcel"

    @property
    def dtype(self):
        return self._dtype
    @dtype.setter
    def dtype(self, typ):
        # check that dtype is a member of DataType.image_types (although the pixel_array isn't of a custom class, this is still used to define the expected
        # numpy data type of pixel_array)
        if typ not in DataType.image_types():
            raise TypeError(f"{typ} is not a valid Image DataType.")
        self._dtype = typ

    # check that shape is of type Shape
    @property 
    def shape(self) -> Optional[Shape]:
        return self._shape
    @shape.setter
    def shape(self, shp: Optional[Shape]):
        if not isinstance(shp, Shape) and shp is not None:
            raise TypeError(f"Expected shape to be of class Shape, got {type(shp)}")
        self._shape = shp

    # check that mapping is of type Shape
    @property
    def mapping(self) -> Optional[Shape]:
        return self._mapping
    @mapping.setter
    def mapping(self, map: Optional[Shape]):
        if not isinstance(map, Shape) and map is not None:
            raise TypeError(f"Expected map to be of class Shape, got {type(map)}")
        self._mapping = map


    @property
    def pixel_array(self) -> Optional[np.ndarray]:
        return self._pixel_array

    @pixel_array.setter
    def pixel_array(self, array: Optional[np.ndarray]):
         # on instantiation, pixel_array values for inputs and outputs will be None - only check values once data is present
        if array is not None and self.dtype in DataType.image_types():
            if not isinstance(array, np.ndarray):
                raise TypeError(f"Expected pixel array as numpy array, got {type(array)}")
            # check that pixel_array is of the expected numpy data type given dtype
            if array.dtype != self.dtype.numpy:
                raise TypeError(f"Expected pixel array data as {self.dtype.numpy} (defined by {self.dtype}.numpy), got {array.dtype}")
        self._pixel_array = array

# simple class to hold parameter inputs and outputs
class ParameterParcel:
    def __init__(self, dtype, value = None, shape = None, mapping = None):
        self.dtype = dtype
        self.value = value
        self.shape = shape        

    type_name = "ParameterParcel"

    @property
    def dtype(self):
        return self._dtype
    @dtype.setter
    def dtype(self, typ):
        # check that dtype is a member of DataType.array_types/value_types (although the pixel_array isn't of a custom class, this is still used to define the expected
        # numpy data type of pixel_array)
        if typ not in DataType.array_types() and typ not in DataType.value_types():
            raise TypeError(f"{typ} is not a valid array or value DataType.")
        self._dtype = typ

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        if val is not None:
            # if dtype is an array,
            if self.dtype in DataType.array_types():
                # check value is actual ndarray
                if not isinstance(val, (np.ndarray, list, tuple)):
                    raise TypeError(f"Expected value as list, tuple or ndarray, got {type(val)}")
                # and that values inside array of correct type
                if val.dtype != self.dtype.numpy:
                    raise TypeError(f"Expected value as {self.dtype.numpy} (defined by {self.dtype}.numpy), got {val[0].dtype}")
            # else if dtype is a scalar type
            elif self.dtype in DataType.value_types():
                # check val is of expected type
                if type(val) != self.dtype.numpy:
                    raise TypeError(f"Expected value as {self.dtype.numpy} (defined by {self.dtype}.numpy), got {val.dtype}")
            else:
                raise TypeError(f"Expected dtype as member of DataType.array_types or DataType.value_types, got {self.dtype}")
        self._value = val


class ImageOperation:
    def __init__(self, name, category, compiled_code, version, docs, alerts, input_image = {}, input_parameter={}, output_image = {}, output_parameter = {}, ):
        self.name = name
        self.category = category
        self.compiled_code = compiled_code
        self.version = version
        self.docs = docs
        self.alerts = alerts 
        self.input_image = input_image # input images as dictionary of ImageParcels   { "name":  ImageParcel}
        self.input_parameter = input_parameter # other inputs as dictionary of ParameterParcels {   "name":  ParameterParcel}
        self.output_image = output_image # Output images as dictionary, as input_image
        self.output_parameter = output_parameter # other outputs as dictionary, as input_parameter

    # check input_image and output_image are dictionaries of ImagePackages
    @property
    def input_image(self):
        return self._input_image
    
    @input_image.setter
    def input_image(self, input):
        self.check_data(dictionary = input, 
                       dtype = ImageParcel,
                       identifier = "input_image")
        self._input = input

    @property
    def output_image(self):
        return self._output_image
    @output_image.setter
    def output_image(self, output):
        self.check_data(dictionary = output, 
                       dtype = ImageParcel,
                       identifier = "output_image")
        self._output = output

    # check input parameter and output parameter are dictionaries of ParameterPackages
    @property
    def input_parameter(self):
        return self._input_parameter

    @input_parameter.setter
    def input_parameter(self, input):
        self.check_data(dictionary = input, 
                       dtype = ParameterParcel,
                       identifier = "input_parameter")
        self._input_parameter = input

    @property
    def output_parameter(self):
        return self._output_parameter

    @output_parameter.setter
    def output_parameter(self, output):
        self.check_data(dictionary = output, 
                       dtype = ParameterParcel,
                       identifier = "output_parameter")
        self._output_parameter = output

    def check_data(self, dictionary, dtype, identifier):
        if dictionary is not None:
            if not isinstance(dictionary, dict):
                raise TypeError(f"Expected {identifier} to be dictionary, not {type(dictionary)}")
            for item in dictionary.items():
                if item is not None and not isinstance(item, dtype):
                    raise TypeError(f"Expected {identifier} to be dictionary of {dtype.type_name}, not {type(item)}")
        


    def run_code(self):

        #TODO - Carry out key checks that all input data is present and correct - for each image,
        #is the pixel array, shape and map there? does the shape and map fit the pixel array?
        """                # check that image matches constrains given by shape
        # NOTE for shapes: For inputs to ImageOperations, the actual image shape is not strictly defined.
        pixel_array_shape = pixel_array.value.shape


        # loops through dimensions in order c, z, y, x
        for index, dimension in enumerate(shape):
            
            current_dimension_identifier = Shape.dimensions[index]

            # if the dimension is -1, the input doesn't care about that dimension
            if dimension != -1:
            
                # gets pixel_array dimension of current image dimension
                array_dim = map[current_dimension_identifier]

                # checks dimensions sizes match
                if pixel_array_shape[array_dim] != dimension:
                    raise ValueError(f"For {descriptor} {key}, pixel_array dimension {current_dimension_identifier}, expected {dimension} but got {array_dim}")"""

        # set all output values to None
        for item in self.output_image.values():
            item["pixel_array"] = None

        for item in self.output_parameter.values():
            item["value"] = None

        # save current input values:
        current_input_image = self.input_image.copy()
        current_input_parameter = self.input_parameter.copy()

        # run compiled code on given inputs
        try:
            exec(self.compiled_code, {"input_image": self.input_image,
                                      "input_parameter":self.input_parameter,
                                      "output_image": self.output_image,
                                      "output_parameter":self.output_parameter})
        except Exception as e:
            raise RuntimeError(f"Error executing operation '{self.name}': {e}")

        # check output generated
        output_generated = False

        for item in self.output_image.values():
            if item["pixel_array"] is not None:
                output_generated = True

        for item in self.output_parameter.values():
            if item["value"] is not None:
                output_generated = True

        if output_generated == False:
            raise RuntimeError(f"Operation {self.name} did not generate an output.")


        # check inputs have not changed
        input_changed = False
        for key, item in self.input_image.items():
            if item["pixel_array"] != None:
                if not np.array_equal(item["pixel_array"],current_input_image[key]["pixel_array"]):
                    input_changed = True
        for key, item in self.input_parameter.items():
            if item["value"] != None:
                if item["value"] != current_input_parameter[key]["value"]:
                    input_changed = True

        if input_changed:
            raise RuntimeError(f"Operation {self.name} altered input values.")
                                      

        
  