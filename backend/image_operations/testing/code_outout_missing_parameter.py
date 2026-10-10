from core.image_operation import ImageOperation
from core.metadata import ImageMetadata, ParameterMetadata
from core.shape import Shape
from core.constants import DataType

version = "1.0.0"
class CodeOutputMissingArguementParameterValue(ImageOperation):
    
    def __init__(self):
        super().__init__(
            name="Code output missing parameter",
            id="code_output_missing_parameter",
            category="",
            version="1.0.0",
            docs="Returns an output image but not parameter",
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
        input_image_array = self.input_image["input"]
        output = input_image_array.copy()
        self.output_image={"output":output}

