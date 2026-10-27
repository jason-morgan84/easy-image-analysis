from core.image_operation import ImageOperation
from core.metadata import ImageMetadata
from core.shape import Shape
from core.constants import DataPolicy

version = "1.0.0"
class CodeFailsRandomTesting(ImageOperation):
    
    def __init__(self):
        super().__init__(
            name="Code fails random testing",
            id="code_fails_random_testing",
            category="",
            version="1.0.1",
            docs="Functional code but produces invalid value",
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
        output = input_image_array.copy()
        output = output/255
        output[0][0][0][0] = 25.12
        print("AStATST", output[0][0][0][0] )
        self.output_image={"output":output}

