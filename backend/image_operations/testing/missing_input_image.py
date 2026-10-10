from core.image_operation import ImageOperation
from core.metadata import ImageMetadata
from core.shape import Shape
from core.constants import DataType

version = "1.0.0"

class MissingInputImage(ImageOperation):
    def __init__(self):
        super().__init__(
            name="Missing Input Image",
            id="missing_input_image",
            version = "1.0.0",
            category="Testing",
            docs="Contains no input_image",
            alerts=None,
            input_image_metadata=None, # this is required
            output_image={ "output": ImageMetadata(dtype = DataType.ImageInt,
                                                     image_shape_constraints = Shape(c=-1, z=-1, y=-1, x=-1),
                                                     image_map = Shape(c=0, z=1, y=2, x=3))}, 
            )
    def execute(self):
        input_image_array = self.input_image["input"]
        
        output = input_image_array.copy()

        self.output_image={"output":output}