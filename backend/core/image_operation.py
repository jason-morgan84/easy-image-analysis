from core.constants import DataType
from core.metadata import ImageMetadata, ParameterMetadata
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



class ImageOperation:
    def __init__(self, 
                 name,
                 id,
                 category, 
                 version, 
                 docs, 
                 alerts,
                 input_image_metadata,
                 output_image_metadata = None,
                 input_parameter_metadata = None,
                 output_parameter_metadata = None,
                 input_parameter = None, 
                 output_parameter = None,
                 input_image = None, 
                 output_image = None):
        
        self._input_image = input_image
        self._output_image = output_image
        self.name = name
        self.id = id
        self.category = category
        self.version = version
        self.docs = docs
        self.alerts = alerts 
        self.input_image = input_image # dictionary of input image data - None on instantiation
        self.input_parameter = input_parameter # dictionary of input parameters - None on instantiation
        self.input_image_metadata = input_image_metadata # dictionary of input image metadata - required on instantiation
        self.input_parameter_metadata = input_parameter_metadata # dictionary of input parameter metadata - required on instantiation if parameters are required

        self.output_image = output_image # dictionary of output image data - None on instantiation
        self.output_parameter = output_parameter # dictionary of output parameters - None on instantiation
        self.output_image_metadata = output_image_metadata # dictionary of output image metadata - required on instantiation if imgaes are output
        self.output_parameter_metadata = output_parameter_metadata # dictionary of output parameter metadata - required on instantiation if parameters are output

    # check input_image_metadata exists and is a dictionary of class ImageMetadata
    @property
    def input_image_metadata(self):
        return self._input_image_metadata
    
    @input_image_metadata.setter
    def input_image_metadata(self, metadata):
        if metadata is None:
            raise ValueError(f"for ImageOperation, input_metadata is required")
        else: 
            self.check_metadata(dictionary = metadata,
                                dtype = ImageMetadata,
                                identifier = "input_image_metadata")
        self._input_image_metadata = metadata
    # if output_image_metadata exists, check its a dictionary of class ImageMetadata
    @property
    def output_image_metadata(self):
        return self._output_image_metadata
    
    @output_image_metadata.setter
    def output_image_metadata(self, metadata):
        if metadata is not None:
            self.check_metadata(dictionary = metadata,
                                dtype = ImageMetadata,
                                identifier = "input_image_metadata")
        self._output_image_metadata = metadata if metadata else None
    # if input_parameter_metadata exists, check its a dictionary of class ParameterMetadata
    @property
    def input_parameter_metadata(self):
        return self._input_parameter_metadata
    
    @input_parameter_metadata.setter
    def input_parameter_metadata(self, metadata):
        if metadata is not None:
            self.check_metadata(dictionary = metadata,
                                dtype = ImageMetadata,
                                identifier = "input_image_metadata")
        self._input_parameter_metadata = metadata if metadata else None
    # if output_parameter_metadata exists, check its a dictionary of class ParameterMetadata
    @property
    def output_parameter_metadata(self):
        return self._output_parameter_metadata
    
    @output_parameter_metadata.setter
    def output_parameter_metadata(self, metadata):
        if metadata is not None:
            self.check_metadata(dictionary = metadata,
                                dtype = ImageMetadata,
                                identifier = "input_image_metadata")
        self._output_parameter_metadata = metadata if metadata else None

    # if input_image or output_image exist, check that they are dictionaries with values of type np.ndarray and np.dtype of metadata.dtype.numpy
    # if they're None, leave them as None - presence of inputs when required will be checked before execution.
    @property
    def input_image(self):
        return self._input_image
    
    @input_image.setter
    def input_image(self, input):
        if input is not None:
            self.check_data(dictionary = input, 
                        metadata = self.input_image_metadata,
                        identifier = "input_image")
        self._input_image = input if input else None

    @property
    def output_image(self):
        return self._output_image
    @output_image.setter
    def output_image(self, output):
        if output is not None:
            self.check_data(dictionary = output, 
                        metadata = self.output_image_metadata,
                        identifier = "output_image")
        self._output_image = output if output else None

    # if input_parameter or output_parameter exist, check that they are:
    #   - if parameter dtype is array type, dictionaries with values of type np.ndarray and np.dtype of metadata.dtype.numpy
    #   - if parameter dtype is value type, dictionaries with values of metadata.dtype.numpy
    @property
    def input_parameter(self):
        return self._input_parameter

    @input_parameter.setter
    def input_parameter(self, input):
        if input is not None:
            self.check_data(dictionary = input, 
                            metadata = self.input_parameter_metadata,
                            identifier = "input_parameter")
        self._input_parameter = input if input else None

    @property
    def output_parameter(self):
        return self._output_parameter

    @output_parameter.setter
    def output_parameter(self, output):
        self.check_data(dictionary = output, 
                        metadata = self.output_parameter_metadata,
                        identifier = "output_parameter")
        self._output_parameter = output if output else None

    # checks data dictionaries are dictionaries, has associated metadata, matches a meta data key and matches metadata dtype
    def check_data(self, dictionary, metadata, identifier):
        # check dictionary is a dictionary
        if not isinstance(dictionary, dict):
            raise TypeError(f"expected {identifier} to be dictionary, not {type(dictionary)}")

        for key, item in dictionary.items():
            # check metadata exists
            if not metadata:
                raise ValueError(f"{identifier} present with no meta_data")
            if key not in metadata.keys():
                # check key is present in relevant metadata
                raise ValueError(f"key present in {identifier} but not in metadata: {key} ")
            item_dtype = metadata[key].dtype
            if not isinstance(item, item_dtype):
                   # check value is of correct type
                   raise TypeError(f"dictionary value of incorrect type: for {key} in {identifier} expected {item_dtype}, not {type(item)}")

    # checks metadata dictionaries are dictionaries and values are of ImageMetadata or ParameterMetadata types
    def check_metadata(self,dictionary,dtype,identifier):
        # check dictionary is a dictionary
        if not isinstance(dictionary, dict):
            raise TypeError(f"expected {identifier} to be dictionary, not {type(dictionary)}")
        
        for value in dictionary.values():
            # check values are of correct type
            if not isinstance(value, dtype):
                raise TypeError(f"for metadata {identifier}, expected values of type {dtype}, got {type(value)}")
            
    def execute(self):
        pass

    
    def run_code(self):

        """carry out pre-execution tests"""
        # check code exists:
        self.check_code()

        # check input_image exists and is in the correct format
        if len(self.input_image) != 0:
            self.check_image(self.input_image,"input")
        else:
            raise ValueError(f"input_image expected, got none")

        # check input parameter format, if they exist
        self.check_parameter(self.input_parameter, "input")

        # For output images, check that Shape is present (pixel array and image_map can be defined based on actual code) 
        for key, image in self.output_image.items():
            if image.shape is None:
                raise ValueError(f"expected image shape constraints for output_image {key} not present")

        """reset output values"""
        self.reset_output()

        # save current input values (to allow for checking that inputs have not been changed):
        current_input_image = copy.deepcopy(self.input_image)
        current_input_parameter = copy.deepcopy(self.input_parameter) if self.input_parameter else None

        # run compiled code on given inputs
        try:
            self.execute()
        except Exception as e:
            raise RuntimeError(f"error executing operation '{self.name}': {e}")

        """carry out post-execution tests"""
        # check output generated
        if not self.output_image and not self.output_parameter:
            raise RuntimeError(f"operation did not generate an output ({self.name})")

        # check output pixel_arrays match shape and image_map
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

    def reset_input(self):
        # set input image values and parameters to None
        self.input_image = None
        self.input_parameter_metadata = None

    def reset_output(self):
        # set output image and parameters  to None
        self.output_image = None
        self.output_parameter = None
        
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
                Do all the pixel maps match the expected shape given shape/image_map values?
                NOTE for shapes: For inputs to ImageOperations, the actual image shape is not strictly defined.

        If metadata exists, does dictionary exist?
            - if dictionary exists, it will have been type checked by the setter
        For each item in metadata:
            - Does a relevant item in dictionary exist?
            - If the dictionary exist, does it have the correct type?
        """
        for key, image in check_images.items():
            if not isinstance(image, ImageParcel):
                raise TypeError(f"Expected {descriptor} to be dictionary of ImageParcel, not {type(image)}")
            if image.pixel_array is None:
                raise ValueError(f"No image pixel array given for {descriptor} {key}")
            if image.image_map is None: # note - for image_map and shape, if they exist their type has already been checked
                raise ValueError(f"No image image_map data given for {descriptor} {key}")
            if image.shape is None: 
                raise ValueError(f"No image shape data given for {descriptor} {key}")

            pixel_array_shape = image.pixel_array.shape
            # loops through dimensions in order c, z, y, x
            for index, dimension in enumerate(image.shape):
                current_dimension_identifier = Shape.dimensions[index]
                # if the dimension is -1, the image doesn't care about that dimension
                if dimension != -1:
                    # gets pixel_array dimension of current image dimension
                    array_dim = image.image_map[current_dimension_identifier]
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
                                
                                    

    
