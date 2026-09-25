from core.constants import DataType
from core.shape import Shape
import numpy as np
import copy
import inspect

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
    def shape(self):
        return self._shape
    @shape.setter
    def shape(self, shp):
        if not isinstance(shp, Shape) and shp is not None:
            raise TypeError(f"Expected shape to be of class Shape, got {type(shp)}")
        self._shape = shp.copy() if shp is not None else None

    # check that mapping is of type Shape
    @property
    def mapping(self):
        return self._mapping
    @mapping.setter
    def mapping(self, map):
        if not isinstance(map, Shape) and map is not None:
            raise TypeError(f"Expected map to be of class Shape, got {type(map)}")
        self._mapping = None if map is None else map.copy()


    @property
    def pixel_array(self):
        return self._pixel_array

    @pixel_array.setter
    def pixel_array(self, array):
         # on instantiation, pixel_array values for inputs and outputs will be None - only check values once data is present
        if array is not None and self.dtype in DataType.image_types():
            if not isinstance(array, np.ndarray):
                raise TypeError(f"Expected pixel array as numpy array, got {type(array)}")
            # check that pixel_array is of the expected numpy data type given dtype
            if array.dtype != self.dtype.numpy:
                raise TypeError(f"Expected pixel array data as {self.dtype.numpy} (defined by {self.dtype}.numpy), got {array.dtype}")
        self._pixel_array = None if array is None else array.copy()

# simple class to hold parameter inputs and outputs
class ParameterParcel:
    def __init__(self, dtype, value = None, shape = None):
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
                if isinstance(val,(tuple,list)):
                    val = np.array(val)
                if val.dtype != self.dtype.numpy:
                    raise TypeError(f"Expected value as {self.dtype.numpy} (defined by {self.dtype}.numpy), got {val.dtype}")
            # else if dtype is a scalar type
            elif self.dtype in DataType.value_types():
                # check val is of expected type
                if type(val) != self.dtype.numpy:
                    raise TypeError(f"Expected value as {self.dtype.numpy} (defined by {self.dtype}.numpy), got {type(val)}")
            else:
                raise TypeError(f"Expected dtype as member of DataType.array_types or DataType.value_types, got {self.dtype}")
        self._value = None if val is None else val.copy()

    @property
    def shape(self):
        return self._shape
    @shape.setter
    def shape(self, shp):
        if not isinstance(shp, (np.ndarray,list,tuple)) and shp is not None:
            raise TypeError(f"Parameter array shape expected as tuple, list or np.ndarray, got {type(shp)}")

        #if shape is a np array, set as copy of array, else convert to np array
        self._shape = shp.copy() if isinstance(shp, np.ndarray) else np.array(shp).copy()


class ImageOperation:
    def __init__(self, name, category, version, docs, alerts, input_image={}, input_parameter={}, output_image = {}, output_parameter = {}, ):
        self._input_image = input_image
        self._output_image = output_image
        self.name = name
        self.category = category
        self.version = version
        self.docs = docs
        self.alerts = alerts 
        self.input_image = input_image if input_image else {} # input images as dictionary of ImageParcels   { "name":  ImageParcel}
        self.input_parameter = input_parameter if input_parameter else {}# other inputs as dictionary of ParameterParcels {   "name":  ParameterParcel}
        self.output_image = output_image if output_image else {}# Output images as dictionary, as input_image
        self.output_parameter = output_parameter if output_parameter else {}# other outputs as dictionary, as input_parameter

    # check input_image and output_image are dictionaries of ImagePackages
    @property
    def input_image(self):
        return self._input_image
    
    @input_image.setter
    def input_image(self, input):
        self.check_data(dictionary = input, 
                       dtype = ImageParcel,
                       identifier = "input_image")
        self._input_image = input if input else {}

    @property
    def output_image(self):
        return self._output_image
    @output_image.setter
    def output_image(self, output):
        self.check_data(dictionary = output, 
                       dtype = ImageParcel,
                       identifier = "output_image")
        self._output_image = output if output else {}

    # check input parameter and output parameter are dictionaries of ParameterPackages
    @property
    def input_parameter(self):
        return self._input_parameter

    @input_parameter.setter
    def input_parameter(self, input):
        self.check_data(dictionary = input, 
                       dtype = ParameterParcel,
                       identifier = "input_parameter")
        self._input_parameter = input if input else {}

    @property
    def output_parameter(self):
        return self._output_parameter

    @output_parameter.setter
    def output_parameter(self, output):
        self.check_data(dictionary = output, 
                       dtype = ParameterParcel,
                       identifier = "output_parameter")
        self._output_parameter = output if output else {}

    def check_data(self, dictionary, dtype, identifier):
        if not isinstance(dictionary, dict):
            raise TypeError(f"Expected {identifier} to be dictionary, not {type(dictionary)}")
        
        for key, item in dictionary.items():
            if not isinstance(item, dtype):
                   raise TypeError(f"Expected {identifier} to be dictionary of {dtype.type_name}, not {type(item)}")

    def execute(self):
        pass

    
    def run_code(self):

        # check code exists:
        self.check_code()

        # carry out pre-execution tests
        if len(self.input_image) != 0:
            self.check_image(self.input_image,"input")
        else:
            raise ValueError(f"input_image expected, got none")

        self.check_parameter(self.input_parameter, "input")

        # For output images, check that Shape is present (pixel array and mapping can be defined based on actual code) 
        # and set values to None (to allow that outputs have been created)
        for key, image in self.output_image.items():
            if image.shape is None:
                raise ValueError(f"expected image shape constraints for output_image {key} not present")
            image.pixel_array = None
                    
        # set output parameter values to None
        if self.output_parameter:
            for item in self.output_parameter.values():
                item.value = None

        # save current input values (to allow for checking that inputs have not been changed):
        current_input_image = copy.deepcopy(self.input_image)
        current_input_parameter = copy.deepcopy(self.input_parameter) if self.input_parameter else None

        # run compiled code on given inputs
        try:
            self.execute()
        except Exception as e:
            raise RuntimeError(f"error executing operation '{self.name}': {e}")


        # check output generated
        if not self.output_image and not self.output_parameter:
            raise RuntimeError(f"operation did not generate an output ({self.name})")

        # check output pixel_arrays match shape and mapping
        self.check_image(self.output_image,"output")

        # check output parameter arrays have shape
        self.check_parameter(self.output_parameter,"output")
           
        # check inputs have not changed
        input_changed = False
        for key, item in self.input_image.items():
            if not np.array_equal(item.pixel_array,current_input_image[key].pixel_array):
                input_changed = True

        for key, item in self.input_parameter.items():
            if item.value is not None:
                if not isinstance(item.value,np.ndarray) and item.value != current_input_parameter[key].value:
                    input_changed = True
                if isinstance(item.value,np.ndarray) and not np.array_equal(item.value,current_input_parameter[key].value):
                    input_changed = True

        if input_changed:
            raise RuntimeError(f"operation altered input values ({self.name})")
        
    def check_code(self):
        function = getattr(self, "execute")
        code_by_line = inspect.getsource(function).split("\n")
        if code_by_line[1].rstrip().lstrip() == "pass":
            raise RuntimeError(f"no code exists for ImageOperation {self.name}")

    def check_image(self, check_images, descriptor):
        """ 
        Does image exist?
            If not:
                Value Error.
            If so:
                It's value has already been checked.
                Do all image dictionary members have an associated pixel map?
                Do all the pixel maps match the expected shape given shape/mapping values?
                NOTE for shapes: For inputs to ImageOperations, the actual image shape is not strictly defined.
        """
        for key, image in check_images.items():
            if not isinstance(image, ImageParcel):
                raise TypeError(f"Expected {descriptor} to be dictionary of ImageParcel, not {type(image)}")
            if image.pixel_array is None:
                raise ValueError(f"No image pixel array given for {descriptor} {key}")
            if image.mapping is None: # note - for mapping and shape, if they exist their type has already been checked
                raise ValueError(f"No image mapping data given for {descriptor} {key}")
            if image.shape is None: 
                raise ValueError(f"No image shape data given for {descriptor} {key}")

            pixel_array_shape = image.pixel_array.shape
            # loops through dimensions in order c, z, y, x
            for index, dimension in enumerate(image.shape):
                current_dimension_identifier = Shape.dimensions[index]
                # if the dimension is -1, the image doesn't care about that dimension
                if dimension != -1:
                    # gets pixel_array dimension of current image dimension
                    array_dim = image.mapping[current_dimension_identifier]
                    # checks dimensions sizes match
                    if pixel_array_shape[array_dim] != dimension:
                        raise ValueError(f"For {descriptor} image {key}, pixel_array dimension {current_dimension_identifier}, expected {dimension} but got {array_dim}")

    def check_parameter(self,check_parameters,descriptor):
        """
        Does input_parameter exist?
            If not:
                Not a problem, not required.
            If so:
                Do all the input_parameter dictionary members have an associated value?
                Where that input_parameter is an array_value, does its shape match the defined shape?
        """

        for key, parameter in check_parameters.items():
            if not isinstance(parameter, ParameterParcel):
                raise TypeError(f"Expected {descriptor} to be dictionary of ParameterParcel, not {type(parameter)}")
            if parameter.value is None:
                raise ValueError(f"No value given for parameter {descriptor} {key}")
            if parameter.dtype in DataType.array_types() and not np.array_equal(np.array(parameter.value.shape), parameter.shape):
                raise ValueError(f"For parameter {descriptor} {key}, array shape {parameter.value.shape} does not match expected shape {parameter.shape}")   
                                
                                    

    
