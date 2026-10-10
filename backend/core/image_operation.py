from core.metadata import ImageMetadata, ParameterMetadata
from core.data_checks import check_metadata, check_data_dictionaries, check_data
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

        self.output_image_metadata = output_image_metadata # dictionary of output image metadata - required on instantiation if imgaes are output
        self.output_parameter_metadata = output_parameter_metadata # dictionary of output parameter metadata - required on instantiation if parameters are output
        
        self.output_image = output_image # dictionary of output image data - None on instantiation
        self.output_parameter = output_parameter # dictionary of output parameters - None on instantiation
      

    # check input_image_metadata exists and is a dictionary of class ImageMetadata
    @property
    def input_image_metadata(self):
        return self._input_image_metadata
    
    @input_image_metadata.setter
    def input_image_metadata(self, metadata):
        if metadata is None:
            raise ValueError(f"for ImageOperation, input_metadata is required")
        else: 
            check_metadata(metadata=metadata, 
                           dtype=ImageMetadata,
                           identifier="input_image_metadata")
        self._input_image_metadata = metadata

    # if output_image_metadata exists, check its a dictionary of class ImageMetadata
    @property
    def output_image_metadata(self):
        return self._output_image_metadata
    
    @output_image_metadata.setter
    def output_image_metadata(self, metadata):
        if metadata is not None:
            check_metadata(metadata=metadata, 
                           dtype=ImageMetadata,
                           identifier="output_image_metadata")
        self._output_image_metadata = metadata if metadata else None

    # if input_parameter_metadata exists, check its a dictionary of class ParameterMetadata
    @property
    def input_parameter_metadata(self):
        return self._input_parameter_metadata
    
    @input_parameter_metadata.setter
    def input_parameter_metadata(self, metadata):
        if metadata is not None:
            check_metadata(metadata=metadata, 
                           dtype=ParameterMetadata,
                           identifier="input_parameter_metadata")
        self._input_parameter_metadata = metadata if metadata else None
    # if output_parameter_metadata exists, check its a dictionary of class ParameterMetadata
    @property
    def output_parameter_metadata(self):
        return self._output_parameter_metadata
    
    @output_parameter_metadata.setter
    def output_parameter_metadata(self, metadata):
        if metadata is not None:
            check_metadata(metadata=metadata, 
                           dtype=ParameterMetadata,
                           identifier="output_parameter_metadata")
        self._output_parameter_metadata = metadata if metadata else None

    # if input_image or output_image exist, check that they are dictionaries with associated metadata
    @property
    def input_image(self):
        return self._input_image
    
    @input_image.setter
    def input_image(self, input):
        if input is not None:
            check_data_dictionaries(data=input,
                                    metadata=self.input_image_metadata,
                                    dtype=ImageMetadata,
                                    identifier="input_image")
        self._input_image = input if input else None

    @property
    def output_image(self):
        return self._output_image
    @output_image.setter
    def output_image(self, output):
        if output is not None:
            check_data_dictionaries(data=output,
                                    metadata=self.output_image_metadata,
                                    dtype=ImageMetadata,
                                    identifier="output_image")
        self._output_image = output if output else None

    # if input_parameter or output_parameter exist, check that they are dictionaries with matching metadata
    @property
    def input_parameter(self):
        return self._input_parameter

    @input_parameter.setter
    def input_parameter(self, input):
        if input is not None:
            check_data_dictionaries(data=input,
                                    metadata=self.input_parameter_metadata,
                                    dtype=ParameterMetadata,
                                    identifier="input_parameter")
        self._input_parameter = input if input else None

    @property
    def output_parameter(self):
        return self._output_parameter

    @output_parameter.setter
    def output_parameter(self, output):
        if output is not None:
            check_data_dictionaries(data=output,
                                    metadata=self.output_parameter_metadata,
                                    dtype=ParameterMetadata,
                                    identifier="output_parameter")
        self._output_parameter = output if output else None

   
            
    def execute(self):
        pass

    
    def run_code(self):

        """carry out pre-execution tests"""
        # check code exists:
        self.check_code()

        # check input_image exists and is in the correct format
        check_data(data=self.input_image,
                   metadata=self.input_image_metadata,
                   dtype=ImageMetadata,
                   identifier="input_image")

        # if input_parameter exists, check its format
        if self.input_parameter_metadata is not None or self.input_parameter is not None:
            check_data(data=self.input_parameter,
                       metadata=self.input_parameter_metadata,
                       dtype=ParameterMetadata,
                       identifier="input_parameter")

        # check that at least one output is defined:
        if self.output_image_metadata is None and self.output_parameter_metadata is None:
            raise RuntimeError(f"no defined outputs present for ImageOperation {self.name}")

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

        # check output images match image_shape_constraints and image_map
        if self.output_image is not None or self.output_image_metadata is not None:
            check_data(data=self.output_image,
                       metadata=self.output_image_metadata,
                       dtype=ImageMetadata,
                       identifier="output_image")

        # check output parameter arrays have shape
        if self.output_parameter is not None or self.output_parameter_metadata is not None:
            check_data(data=self.output_parameter,
                       metadata=self.output_parameter_metadata,
                       dtype=ParameterMetadata,
                       identifier="output_parameter")
           
        # check inputs have not changed
        input_changed = False
        for key, value in self.input_image.items():
            if not np.array_equal(value,current_input_image[key]):
                input_changed = True

        if self.input_parameter is not None:
            for key, value in self.input_parameter.items():
                if not isinstance(value,np.ndarray) and value != current_input_parameter[key]:
                    input_changed = True
                if isinstance(value,np.ndarray) and not np.array_equal(value,current_input_parameter[key]):
                    input_changed = True

        if input_changed:
            raise RuntimeError(f"operation altered input values ({self.name})")

    def reset_input(self):
        # set input image values and parameters to None
        self.input_image = None
        self.input_parameter = None

    def reset_output(self):
        # set output image and parameters  to None
        self.output_image = None
        self.output_parameter = None
        
    def check_code(self):
        function = getattr(self, "execute")
        if function is None:
            raise RuntimeError(f"no code exists for ImageOperation {self.name}")
        code_by_line = inspect.getsource(function).split("\n")
        if code_by_line[1].rstrip().lstrip() == "pass":
            raise RuntimeError(f"no code exists for ImageOperation {self.name}")



   
                                
                                    

    
