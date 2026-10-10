from core.image_operation import ImageOperation
from core.metadata import ImageMetadata
from core.shape import Shape
from core.constants import DataType

version = "1.0.0"
class CodeCorrectImageOnly(ImageOperation):
    
    def __init__(self):
        super().__init__(
            name="Code Correct Image Only",
            id="code_correct_image_only",
            category="",
            version="1.0.0",
            docs="Correct code that only returns an image",
            alerts=None,
            input_image_metadata={"input":  ImageMetadata(dtype=DataType.ImageInt,
                                                          image_shape_constraints=Shape(c=-1, z=-1, y=-1, x=-1),
                                                          image_map=Shape(c=0, z=1, y=2, x=3))},
            input_parameter = None,
            output_image_metadata = { "output": ImageMetadata(dtype=DataType.ImageInt,
                                                              image_shape_constraints=Shape(c=-1, z=-1, y=-1, x=-1),
                                                              image_map=Shape(c=0, z=1, y=2, x=3))},
            output_parameter = None
            )
    def execute(self):
        input_image_array = self.input_image["input"]
        output = input_image_array.copy()
        self.output_image={"output":output}