from core.image_operation import ImageOperation
from core.metadata import ImageMetadata, ParameterMetadata
from core.shape import Shape
from core.constants import DataPolicy

version = "1.0.0"
class CodeOutputParameterNotDictionary(ImageOperation):
    
    def __init__(self):
        super().__init__(
            name="code output parameter not dictionary",
            id="code_output_parameter_not_dictionary",
            category="",
            version="1.0.1",
            docs="Returns an identical image to that inserted",
            alerts=None,
            input_image_metadata={ "input":  ImageMetadata(dtype=DataPolicy.ImageInt,
                                                  image_shape_constraints=Shape(c=-1, z=-1, y=-1, x=-1),
                                                  image_map=Shape(c=0, z=1, y=2, x=3))},
            output_parameter_metadata={ "output": ParameterMetadata(dtype=DataPolicy.ValueInt)}
            )
    def execute(self):
        self.output_parameter = 2
       

