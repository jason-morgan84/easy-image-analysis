from core.image_operation import ImageOperation
from core.metadata import ImageMetadata
from core.shape import Shape
from core.constants import DataPolicy

version = "1.0.0"
class CodeAltersInput(ImageOperation):
    
    def __init__(self):
        super().__init__(
            name="Code alters input",
            id="code_alters_input",
            category="",
            version="1.0.1",
            docs="Changes input values",
            alerts=None,
            input_image_metadata={ "input":  ImageMetadata(dtype=DataPolicy.ImageInt,
                                                  image_shape_constraints=Shape(c=-1, z=-1, y=-1, x=-1),
                                                  image_map=Shape(c=0, z=1, y=2, x=3))},
            output_image_metadata={ "output": ImageMetadata(dtype=DataPolicy.ImageInt,
                                                     image_shape_constraints=Shape(c=-1, z=-1, y=-1, x=-1),
                                                     image_map=Shape(c=0, z=1, y=2, x=3))}, 
            )
    def execute(self):
        self.input_image["input"][0][0][0][0] += 1

        input_image_array = self.input_image["input"]
        output = input_image_array.copy()
        self.output_image={"output":output}

