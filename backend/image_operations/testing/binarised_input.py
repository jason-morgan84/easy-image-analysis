from core.image_operation import ImageOperation
from core.metadata import ImageMetadata
from core.shape import Shape
from core.constants import DataPolicy

version = "1.0.0"
class SameImage(ImageOperation):
    
    def __init__(self):
        super().__init__(
            name="binarised input",
            id="binarised_input",
            category="",
            version="1.0.0",
            docs="For Workflow testing, requires Binary input",
            alerts=None,
            input_image_metadata={ "input":  ImageMetadata(dtype=DataPolicy.ImageBinary,
                                                  image_shape_constraints=Shape(c=-1, z=-1, y=-1, x=-1),
                                                  image_map=Shape(c=0, z=1, y=2, x=3))},
            output_image_metadata={ "output": ImageMetadata(dtype=DataPolicy.ImageInt,
                                                     image_shape_constraints=Shape(c=-1, z=-1, y=-1, x=-1),
                                                     image_map=Shape(c=0, z=1, y=2, x=3))}, 
            )
    def execute(self):
        input_image_array = self.input_image["input"]
        output = DataPolicy.ImageBinary._convert(value=input_image_array,dtype=DataPolicy.ImageInt)
        self.output_image={"output":output}

