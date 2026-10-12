from core.image_operation import ImageOperation
from core.metadata import ImageMetadata
from core.shape import Shape
from core.constants import DataType

version = "1.0.0"
class SingleChannelInput(ImageOperation):
    
    def __init__(self):
        super().__init__(
            name="Single Channel Input",
            id="single_channel_input",
            category="",
            version="1.0.0",
            docs="Returns an identical image to that inserted but with a single channel input expected",
            alerts=None,
            input_image_metadata={ "input":  ImageMetadata(dtype=DataType.ImageInt,
                                                  image_shape_constraints=Shape(c=1, z=-1, y=-1, x=-1),
                                                  image_map=Shape(c=0, z=1, y=2, x=3))},
            output_image_metadata={ "output": ImageMetadata(dtype=DataType.ImageInt,
                                                     image_shape_constraints=Shape(c=-1, z=-1, y=-1, x=-1),
                                                     image_map=Shape(c=0, z=1, y=2, x=3))}, 
            )
    def execute(self):
        input_image_array = self.input_image["input"]
        output = input_image_array.copy()
        self.output_image={"output":output}

