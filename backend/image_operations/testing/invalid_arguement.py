from core.image_operation import ImageOperation
from core.shape import Shape
from core.constants import DataType
from core.metadata import ImageMetadata

version = "1.0.0"

class InvalidArguement(ImageOperation):
    def __init__(self):
        super().__init__(
            name="Invalid Arguement",
            category="Testing",
            version="1.0.0",
            docs="Contains an invalid arguement in input_image (dtype = int))",
            alerts=None,
            input_image_metadata={ "input":  ImageMetadata(dtype = int, # this is in the wrong format
                                                   shape = Shape(-1,-1,-1,-1),
                                                   image_map = Shape(0,1,2,3))},
            output_image_metadata={ "output": ImageMetadata(dtype = DataType.ImageInt,
                                                     image_shape_constraints = Shape(c=-1, z=-1, y=-1, x=-1),
                                                     image_map = Shape(c=0, z=1, y=2, x=3))}, 
            )
    def execute(self):
        input_image_array = self.input_image["input"]
        
        output = input_image_array.copy()

        self.output_image={"output":output}

