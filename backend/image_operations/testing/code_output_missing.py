from core.image_operation import ImageOperation
from core.metadata import ImageMetadata, ParameterMetadata
from core.shape import Shape
from core.constants import DataType

version = "1.0.0"

class CodeOutputMissing(ImageOperation):
    def __init__(self):
        super().__init__(
            name = "Code no output",
            id="code_no_output",
            category="",
            version="1.0.1",
            docs = "Doesn't provide an output",
            alerts=None,
            input_image_metadata={ "input":  ImageMetadata(dtype=DataType.ImageInt,
                                                  image_shape_constraints=Shape(c=-1, z=-1, y=-1, x=-1),
                                                  image_map=Shape(c=0, z=1, y=2, x=3))},
            output_image_metadata={ "output": ImageMetadata(dtype=DataType.ImageInt,
                                                     image_shape_constraints=Shape(c=-1, z=-1, y=-1, x=-1),
                                                     image_map=Shape(c=0, z=1, y=2, x=3))}, 
            output_parameter_metadata={"output2":ParameterMetadata(dtype=DataType.ValueInt)}
            )
    def execute(self):
        self.output_parameter = {}
        self.output_image = {}
