##############################
# Sample ImageOperation File #
##############################

# For more information on ImageOperation format and requirements, see image_operations.md in the docs folder

"""standard imports required for all ImageOperation"""
from core.image_operation import ImageOperation
from core.metadata import ImageMetadata, ParameterMetadata
from core.shape import Shape
from core.constants import DataPolicy

"""specific imports required for this function 
(check image_operation_directory.py and permitted_imports for allowed imports)"""
from scipy import ndimage
import numpy as np

"""version number ImageOperation is designed for.
This is required for modules to be imported, must be in major.minor.patch format
"""
version = "1.0.0"


class GuassianFilter(ImageOperation):
    
    def __init__(self):
        super().__init__(
            name="Gaussian filter", # this is the name that will be seen by a user
            id="gaussian_filter", # this will be set on import based on the file name
            category="", # this will be set on import based on the folder its saved in
            version="", # this will be set on import based on the version above
            # An explanation to the user of what the function does and what its inputs are
            docs= "Applies a gaussian filter to the image, smoothing it and reducing noise. Sigma controls the area over which the filter is applied. The larger the sigma, the heavier the blurring. A good starting value is sigma = 3.",
            alerts=None, # for this function, no alerts are necessary. This could be used if, for example, certain parameters could lead to an exessively high processing time.        
           
            #The metadata describes the expected inputs and outputs. You can't provide an input or get an output without metadata defining it.
            #Metadata must be in a dictionary format. Any data provided to or from the function must also be a dictionary and the keys must match.
            #This means input_image_metadata with key "input" describes the format of an image that will be provided in input_data dictionary and key "input"
            
            #Metadata dictionary values must be either ImageMetadata class (for image inputs/outputs) or ParameterMetadata class (for non-image inputs/outputs)  
            input_image_metadata={ "input":  ImageMetadata(dtype=DataPolicy.ImageInt, # dtype describes the format the image should be in, and must be a member of constants.DatapPolicy
                                                  image_shape_constraints=Shape(c=-1, z=-1, y=-1, x=-1), # this describes constraints on the size of the input image. For example, if it must be single channel c should equal 1. -1 represents no constraints.
                                                  image_map=Shape(c=0, z=1, y=2, x=3))}, # this describes the dimension of the pixel array that corresponds to each image dimension
            input_parameter_metadata={"sigma": ParameterMetadata(dtype=DataPolicy.ValueInt, # dtype describes the format the parameter should be in
                                                                 user_input=True, # if a parameter comes from the UI, this should be True. If its passed from another ImageOperation, it should be False
                                                                 ui_element="text", # if the parameter comes from user input, this defines what sort of UI element should be used
                                                                 ui_element_options=None)}, # any UI element options, such as options for a drop-down box, min/max values for a slider etc
            output_image_metadata={ "output": ImageMetadata(dtype=DataPolicy.ImageInt,
                                                     image_shape_constraints=Shape(c=-1, z=-1, y=-1, x=-1),
                                                     image_map=Shape(c=0, z=1, y=2, x=3))},
            # actual inputs and outputs will be provided as a dictionary, but this doesn't need to be set in advance
            input_image=None, 
            input_parameter=None,

            )
        self.test_input_parameters = {"sigma": np.uint8(3)} # when testing this function, input images are generated but input parameters need to be provided
            
    # the execute function defines the code that will be run when the ImageOperation is executed
    def execute(self):
        """ get inputs from input dictionaries:"""
        # input images will always be provided as an np.ndarray of a data type defined by the metadata dtype
        # in this case, input_image["input"] is an ImageInt, which defines its numpy type as np.uint8
        input_image = self.input_image["input"]

        # input parameters can be prvoded as an array, a np.ndarray, or a scalar value, with numpy type defined by the metadata dtype
        sigma = self.input_parameter["sigma"]

        """ apply function to image """
        blurred_image = []
        # loops through channels and slices, applying gaussian blur to each image.
        # images will always be provided with 4 dimensions, c, z, y and x.
        # depending on metadata, some of these dimensions may be of size 1.

        # the image metadata also defines the order of the dimensions in image_map, in this case CZYX
        for channel in input_image:
            new_channel = []
            for slice in channel:
                new_channel.append(ndimage.gaussian_filter(slice, sigma).copy())
            blurred_image.append(new_channel)


        """ provide output as dictionary (if this isn't done, the ImageOperation will not be imported) """
        self.output_image={"output": np.array(blurred_image,np.uint8)}

    """ code can be tested by saving into the image_operations directory and running:

    python backend/core/image_operation_tests.py function_name
    
    in terminal. This will reproduce all the tests done on import of an ImageOperation and provide text feedback on the results in image_operations/image_operation_test_output.
    It will also run the operation on a sample image which will be saved to the same folder.

    """

    # For more information on ImageOperation format and requirements, see image_operations.md in the docs folder





