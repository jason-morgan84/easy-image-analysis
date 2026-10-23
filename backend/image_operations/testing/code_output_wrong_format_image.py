from core.image_operation import ImageOperation
from core.metadata import ImageMetadata
from core.shape import Shape
from core.constants import DataPolicy

version = "1.0.0"
class CodeOutputWrongFormatImage(ImageOperation):
    
    def __init__(self):
        super().__init__(
            name="Code Output Wrong Format Image",
            id="code_output_wrong_format_image",
            category="",
            version="1.0.0",
            docs="Returns an output image in the wrong format (just a pixel array rather than ImagePackage class)",
            alerts=None,
            input_image_metadata={ "input":  ImageMetadata(dtype=DataPolicy.ImageInt,
                                                  image_shape_constraints=Shape(c=-1, z=-1, y=-1, x=-1),
                                                  image_map=Shape(c=0, z=1, y=2, x=3))},
            output_image_metadata={ "output": ImageMetadata(dtype=DataPolicy.ImageFloat,
                                                     image_shape_constraints=Shape(c=-1, z=-1, y=-1, x=-1),
                                                     image_map=Shape(c=0, z=1, y=2, x=3))}, 
            )
    def execute(self):
        input_image_array = self.input_image["input"]
        self.output_image = {"output": input_image_array.copy()}
