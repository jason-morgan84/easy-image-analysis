from core.image_operation import ImageOperation
from core.metadata import ImageMetadata, ParameterMetadata
from core.shape import Shape
from core.constants import DataPolicy

version = "1.0.0"
class CodeOutputParameterDataNoMetadataKey(ImageOperation):
    
    def __init__(self):
        super().__init__(
            name="code output parameter data with no metadata key",
            id="code_output_parameter_data_with_no_metadata_key",
            category="",
            version="1.0.1",
            docs="Has an output parameter without corresponding metadata key",
            alerts=None,
            input_image_metadata={ "input":  ImageMetadata(dtype=DataPolicy.ImageInt,
                                                  image_shape_constraints=Shape(c=-1, z=-1, y=-1, x=-1),
                                                  image_map=Shape(c=0, z=1, y=2, x=3))},
            output_parameter_metadata={ "output": ParameterMetadata(dtype=DataPolicy.ValueInt)}
            )
    def execute(self):
        self.output_parameter = {"output": 2, "output2": 3}

        

