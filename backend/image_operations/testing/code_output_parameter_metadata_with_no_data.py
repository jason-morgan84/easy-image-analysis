from core.image_operation import ImageOperation
from core.metadata import ImageMetadata, ParameterMetadata
from core.shape import Shape
from core.constants import DataPolicy

version = "1.0.0"
class CodeOutputParameterMetadataWithNoData(ImageOperation):
    
    def __init__(self):
        super().__init__(
            name="code output parameter metadata with no data",
            id="code_output_parameter_metadata_with_no_data",
            category="",
            version="1.0.1",
            docs="Has parameter metadata without an output parameter",
            alerts=None,
            input_image_metadata={ "input":  ImageMetadata(dtype=DataPolicy.ImageInt,
                                                  image_shape_constraints=Shape(c=-1, z=-1, y=-1, x=-1),
                                                  image_map=Shape(c=0, z=1, y=2, x=3))},
            output_image_metadata={ "output": ImageMetadata(dtype=DataPolicy.ImageInt,
                                                     image_shape_constraints=Shape(c=-1, z=-1, y=-1, x=-1),
                                                     image_map=Shape(c=0, z=1, y=2, x=3))},
            output_parameter_metadata={"output2": ParameterMetadata(dtype=DataPolicy.ValueInt)}
            )
    def execute(self):
        input_image_array = self.input_image["input"]
        output = input_image_array.copy()
        self.output_image = {"output": output}
        

