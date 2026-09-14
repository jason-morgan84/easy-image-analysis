import numpy as np
from core.constants import DataType
from core.shape import Shape
from core.parameter import Parameter
from core.image import Image

class ImageOperation:
    def __init__(self, name, category, excecute, version, docs, alerts, input_image = {}, input_parameter={}, output_image = {}, output_parameter = {}, ):
        self.name = name
        self.category = category
        self.excecute = excecute
        self.version = version
        self.docs = docs
        self.alerts = alerts 
        self.input_image = input_image # input images as dictionary of dictionaries   { "name":  {  dtype: member of DataType.image_types,
                                                                            #                       pixel_array: value of type DataType.dtype.numpy(),
                                                                            #                       shape: Shape class defining constraints on input image shape,
                                                                            #                       map: Shape class defining mapping from value array to image dimension}}
        self.input_parameter = input_parameter # other inputs as dictionary of dictionaries {   "name":  {  dtype: member of DataType.value_types or array_types
                                                                            #                               value: value of type DataType.dtype.numpy()
                                                                            #                               shape: shape of array if required as tuple, else None}}
        self.output_image = output_image # Output images as dictionary, as input_image
        self.output_parameter = output_parameter # other outputs as dictionary, as input_parameter



    """Note for types: For input type checking, ImageOperation will be a part of a Node. Data will flow into the Node through a Port, which will transmit the data
    to the ImageOperation class. 

    Ports will carry out type conversions of any inputted data from custom DataTypes used to manage types in data transmission to standard numpy data types
    used in actual image analysis.
    
    This means that while input["input_name"].dtype will be of a DataType class, the actual input data will be off DataType.numpy type, and should be checked against
    that data type"""

    """Note for shapes: For inputs to ImageOperations, the actual image shape is not strictly defined.
    
    This means that input["input_name"].shape does not give array dimensions, but desired array dimensions - a specific value if a strict size is needed for that
    dimension, or -1 if the analysis function is indifferent to size in that dimension."""

    # uses check_image function to check input_image and output_image dictionaries
    @property
    def input_image(self):
        return self._input_image

    @input_image.setter
    def input_image(self, input):
        input = self.check_image(self, input, "Input")
        self._input = input

    @property
    def output_image(self):
        return self._output_image

    @output_image.setter
    def output_image(self, output):
        output = self.check_image(self, output, "Output")
        self._output = output

    @property
    def input_parameter(self):
        return self._input_parameter

    @input_parameter.setter
    def input_parameter(self, input):
        input = self.check_parameter(self, input, "Input")
        self._input_parameter = input

    @property
    def output_parameter(self):
        return self._output_parameter

    @output_parameter.setter
    def output_parameter(self, output):
        output = self.check_parameter(self, output, "Output")
        self._output_parameter = output


    def check_image(self, data, descriptor):
        # check that data is a dictionary
        if not isinstance(data,dict):
            raise TypeError(f"{descriptor} should be passed as a dictionary, not {type(data)}")
        for key, item in data.items():
            dtype = item["dtype"]
            pixel_array = item["pixel_array"]
            shape = item["shape"]
            map = item["map"]

            # check that dtype is a member of DataType.image_types (although the pixel_array isn't of a custom class, this is still used to define the expected
            # numpy data type of pixel_array)
            if dtype not in DataType.image_types:
                raise TypeError(f"For {descriptor} {key}, expected dtype to be member of DataTypes.image_types, got {dtype}")



            # check that shape is of type Shape
            if not isinstance(shape, Shape):
                raise TypeError(f"For {descriptor} {key}, expected shape to be of class Shape, got {type(shape)}")

            # check that map is of type Shape
            if not isinstance(map, Shape):
                raise TypeError(f"For {descriptor} {key},expected map to be of class Shape, got {type(map)}")

            # on instantiation, pixel_array values for inputs and outputs will be None - only check values once data is present
            if pixel_array is not None:

                # check that pixel_array is of the expected numpy data type given dtype
                if not isinstance(pixel_array, dtype.numpy):
                    raise TypeError(f"For {descriptor} {key}, given dtype of {dtype}, expected pixel_array of type {dtype.numpy}, got {type(pixel_array)}")

                # check that image matches constrains given by shape
                # NOTE for shapes: For inputs to ImageOperations, the actual image shape is not strictly defined."""  
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
                            raise ValueError(f"For {descriptor} {key}, pixel_array dimension {current_dimension_identifier}, expected {dimension} but got {array_dim}")
        return data

    def check_parameter(self, data, descriptor):
        # check that data is a dictionary
        if not isinstance(data,dict):
            raise TypeError(f"{descriptor} should be passed as a dictionary, not {type(data)}")
        for key, item in data.items():
            dtype = item["dtype"]
            value = item["value"]
            shape = item["shape"]

            # check that dtype is a member of DataTypes.value_types or DataTypes.array_types 
            if dtype not in DataType.value_types and dtype not in DataType.array_types:
                raise TypeError(f"For {descriptor} {key}, expected dtype to be member of DataTypes.value_types or DataTypes.array_types, got {dtype}")

            if value is not None:
                # check that value is of the expected numpy data type given dtype
                if not isinstance(value, dtype.numpy):
                    raise TypeError(f"For {descriptor} {key}, given dtype of {dtype}, expected value of type {dtype.numpy}, got {type(value)}")

                # check whether value is an array data type. 
                if value in DataType.array_types:
                    # if it is, checks that shape is a tuple or a list
                    if not isinstance(shape, (tuple,list)):
                        raise TypeError(f"For {descriptor} {key}, expected shape to be a tuple or list, got {type(shape)}")
                    if tuple(value.value.shape) != tuple(shape):
                        raise ValueError(f"For {descriptor} {key}, shape of value {value.value.shape} does not match expected shape {tuple(shape)}")

       
        return data


  