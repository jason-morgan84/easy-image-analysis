from core.image_operation import ImageOperation
from core.metadata import ImageMetadata,ParameterMetadata
from core.shape import Shape
from core.constants import DataPolicy
import numpy as np

version = "1.0.0"
class CodeInputParameterMetadataNotDictionary(ImageOperation):
    
    def __init__(self):
        super().__init__(
            name="Code input_parameter_metadata not dictionary",
            id="code_input_parameter_metadata_not_dictionary",
            category="",
            version="1.0.0",
            docs="Code where input_parameter_metadata is not a dictionary",
            alerts=None,
            input_image_metadata={ "input":  ImageMetadata(dtype=DataPolicy.ImageInt,
                                                          image_shape_constraints=Shape(c=-1, z=-1, y=-1, x=-1),
                                                          image_map=Shape(c=0, z=1, y=2, x=3))},
            input_parameter_metadata=ParameterMetadata(dtype = DataPolicy.ValueInt),
            output_image_metadata={ "output": ImageMetadata(dtype=DataPolicy.ImageInt,
                                                              image_shape_constraints=Shape(c=-1, z=-1, y=-1, x=-1),
                                                              image_map=Shape(c=0, z=1, y=2, x=3))},
            output_parameter_metadata={"output2": ParameterMetadata(dtype = DataPolicy.ValueInt)}
            )
    def execute(self):
        input_image_array = self.input_image["input"]
        self.output_image = {"output": input_image_array.copy()}
        self.output_parameter={"output2": np.uint8(2)}