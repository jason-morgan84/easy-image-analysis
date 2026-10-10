from core.image_operation import ImageOperation
from core.metadata import ImageMetadata,ParameterMetadata
from core.shape import Shape
from core.constants import DataType
import numpy as np


version = "1.0.0"
class CodeCorrectParameterOnly(ImageOperation):
    
    def __init__(self):
        super().__init__(
            name="Code Correct Parameter Only",
            id="code_correct_parameter_only",
            category="",
            version="1.0.0",
            docs="Correct code that returns only a parameter",
            alerts=None,
            input_image_metadata={ "input":  ImageMetadata(dtype=DataType.ImageInt,
                                                            image_shape_constraints=Shape(c=-1, z=-1, y=-1, x=-1),
                                                            image_map=Shape(c=0, z=1, y=2, x=3))},
            input_parameter_metadata = None,
            output_image_metadata = None,
            output_parameter_metadata = {"output2": ParameterMetadata(dtype = DataType.ValueInt)}
            )
    def execute(self):
        self.output_parameter = {"output2": np.uint8(2)}