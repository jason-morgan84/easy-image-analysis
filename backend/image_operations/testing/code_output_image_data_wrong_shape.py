from core.image_operation import ImageOperation
from core.metadata import ImageMetadata
from core.shape import Shape
from core.constants import DataPolicy
import numpy as np

version = "1.0.0"
class CodeOutputImageDataWrongShape(ImageOperation):
    
    def __init__(self):
        super().__init__(
            name="code output image data wrong shape",
            id="code_output_image_data_wrong_shape",
            category="",
            version="1.0.1",
            docs="Has an output image with wrong shape",
            alerts=None,
            input_image_metadata={ "input":  ImageMetadata(dtype=DataPolicy.ImageInt,
                                                  image_shape_constraints=Shape(c=-1, z=-1, y=-1, x=-1),
                                                  image_map=Shape(c=0, z=1, y=2, x=3))},
            output_image_metadata={ "output": ImageMetadata(dtype=DataPolicy.ImageInt,
                                                     image_shape_constraints=Shape(c=1, z=-1, y=-1, x=-1),
                                                     image_map=Shape(c=0, z=1, y=2, x=3))}, 
            )
    def execute(self):
        random_array = np.random.random(size = [5,5,5,5])
        random_array = (random_array * 255) 
        output = np.uint8(random_array)
        self.output_image = {"output": output}

        

