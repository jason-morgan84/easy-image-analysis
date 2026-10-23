from core.image_operation import ImageOperation
from core.metadata import ImageMetadata
from core.shape import Shape
from core.constants import DataPolicy
import numpy as np

version = "1.0.0"
class MultiChannelOutput(ImageOperation):
    
    def __init__(self):
        super().__init__(
            name="Multi Channel Output",
            id="multi_channel_output",
            category="",
            version="1.0.0",
            docs="Has metadata for a multi-channel output",
            alerts=None,
            input_image_metadata={ "input":  ImageMetadata(dtype=DataPolicy.ImageInt,
                                                  image_shape_constraints=Shape(c=-1, z=-1, y=-1, x=-1),
                                                  image_map=Shape(c=0, z=1, y=2, x=3))},
            output_image_metadata={ "output": ImageMetadata(dtype=DataPolicy.ImageInt,
                                                     image_shape_constraints=Shape(c=4, z=-1, y=-1, x=-1),
                                                     image_map=Shape(c=0, z=1, y=2, x=3))}, 
            )
    def execute(self):
        random_array = np.random.random(size = (4,2,3,1))
        random_array *= 255
        self.output_image={"output":np.uint8(random_array)}
