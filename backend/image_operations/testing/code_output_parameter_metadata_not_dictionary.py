from core.image_operation import ImageOperation
from core.metadata import ImageMetadata, ParameterMetadata
from core.shape import Shape
from core.constants import DataPolicy

version = "1.0.0"

class CodeOutputParameterMetadataNotDictionary(ImageOperation):
    def __init__(self):
        super().__init__(
            name = "Code output_parameter_metadata not dictionary",
            id="code_output_parameter_metadata_not_dictionary",
            category="",
            version="1.0.1",
            docs = "Output parameter metadata not a dictionary",
            alerts=None,
            input_image_metadata={ "input":  ImageMetadata(dtype=DataPolicy.ImageInt,
                                                  image_shape_constraints=Shape(c=-1, z=-1, y=-1, x=-1),
                                                  image_map=Shape(c=0, z=1, y=2, x=3))},
            output_parameter_metadata=ParameterMetadata(dtype=DataPolicy.ValueInt)
            )
    def execute(self):
        self.output_parameter = {}
        self.output_image = {}
