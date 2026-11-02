
"""standard imports required for all ImageOperation"""
from core.image_operation import ImageOperation
from core.metadata import ImageMetadata, ParameterMetadata
from core.shape import Shape
from core.constants import DataPolicy

"""specific imports required for this function"""

from scipy import ndimage
import numpy as np

version = "1.0.0"


class SelectChannel(ImageOperation):
    
    def __init__(self):
        super().__init__(
            name="Select Channel",
            id="select_channel", 
            category="",
            version="",
            # An explanation to the user of what the function does and what its inputs are
            docs= "Selects a single channel from a multi-channel image input",
            alerts=None, 
           
           
            
           
            input_image_metadata={ "input":  ImageMetadata(dtype=DataPolicy.ImageInt, 
                                                  image_shape_constraints=Shape(c=-1, z=-1, y=-1, x=-1), 
                                                  image_map=Shape(c=0, z=1, y=2, x=3))},
            input_parameter_metadata={"channel": ParameterMetadata(dtype=DataPolicy.ValueInt, 
                                                                 user_input=True,
                                                                 ui_element="text",
                                                                 ui_element_options=None)},
            output_image_metadata={ "output": ImageMetadata(dtype=DataPolicy.ImageInt,
                                                     image_shape_constraints=Shape(c=1, z=-1, y=-1, x=-1),
                                                     image_map=Shape(c=0, z=1, y=2, x=3))},

            )
        
        self.test_input_parameters = {"channel": np.uint8(1)} 
            
    def execute(self):
        """ get inputs from input dictionaries:"""
        input_image = self.input_image["input"]
        channel = self.input_parameter["channel"]
        """check channel parameter is valid"""
        if channel < 0:
            raise ValueError(f"channel selected must have index greater than 0")
        input_c,_,_,_ = input_image.shape
        if channel >= input_c:
            raise ValueError(f"channel selected not present in input image")
        
        single_channel = input_image[channel]
        output_image = np.expand_dims(single_channel, axis=0)
        self.output_image={"output": output_image}







