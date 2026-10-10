from core.image_operation import ImageOperation
from core.metadata import ImageMetadata, ParameterMetadata
from core.shape import Shape
from core.constants import DataType

version = "1.0.0"
class CodeOutputWrongFormatParameter(ImageOperation):
    
    def __init__(self):
        super().__init__(
            name="Code output wrong format parameter",
            id="code_output_wrong_format_parameter",
            category="",
            version="1.0.0",
            docs="Returns an int as output parameter, not ParameterParcel class",
            alerts=None,
            input_image_metadata={ "input":  ImageMetadata(dtype=DataType.ImageInt,
                                                            image_shape_constraints=Shape(c=-1, z=-1, y=-1, x=-1),
                                                            image_map=Shape(c=0, z=1, y=2, x=3))},
            output_parameter_metadata={"output": ParameterMetadata(dtype=DataType.ValueFloat)}
            )
    def execute(self):
        
        self.output_parameter={"output": 15}

