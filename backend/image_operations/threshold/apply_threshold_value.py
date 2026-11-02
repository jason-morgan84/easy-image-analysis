
"""standard imports required for all ImageOperation"""
from core.image_operation import ImageOperation
from core.metadata import ImageMetadata, ParameterMetadata
from core.shape import Shape
from core.constants import DataPolicy

"""specific imports required for this function"""
import numpy as np
import skimage as ski
import math

version = "1.0.0"


class ApplyThresholdValue(ImageOperation):
    
    def __init__(self):
        super().__init__(
            name="Apply Threshold Value",
            id="apply_threshold_value", 
            category="",
            version="",
            # An explanation to the user of what the function does and what its inputs are
            docs= "Applys a given threshold value to all channels and stacks in image, results in a binary output.",
            alerts=None, 

            input_image_metadata={ "input":  ImageMetadata(dtype=DataPolicy.ImageInt, 
                                                  image_shape_constraints=Shape(c=-1, z=-1, y=-1, x=-1), 
                                                  image_map=Shape(c=0, z=1, y=2, x=3))},
            input_parameter_metadata={"threshold": ParameterMetadata(dtype=DataPolicy.ValueInt)},
            output_image_metadata={ "output": ImageMetadata(dtype=DataPolicy.ImageBinary,
                                                     image_shape_constraints=Shape(c=-1, z=-1, y=-1, x=-1),
                                                     image_map=Shape(c=0, z=1, y=2, x=3))},

            )
        
        self.test_input_parameters = {"threshold": np.uint8(10)} 
            
    def execute(self):
        """ get inputs from input dictionaries:"""
        input_image = self.input_image["input"]
        threshold = self.input_parameter["threshold"]

        
        """check threshold parameter is valid"""
        if threshold < 0 or threshold > 255:
            raise ValueError(f"invalid threshold value provided")

        # create output image as array of 0s of same shape as input image
        output_image = np.zeros_like(input_image, np.uint8)

        # binarise output image using threshold
        output_image = input_image > threshold

        self.output_image = {"output": output_image.astype(np.uint8)}












