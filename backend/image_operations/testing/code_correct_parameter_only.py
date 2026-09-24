from core.image_operation import ImageOperation, ImageParcel,ParameterParcel
from core.shape import Shape
from core.constants import DataType
import numpy as np

version = "0.1.0"
class CodeCorrectParameterOnly(ImageOperation):
    
    def __init__(self):
        super().__init__(
            name = "Code Correct Parameter Only",
            category = "",
            version = "0.2",
            docs = "Correct code that returns only a parameter",
            alerts = None,
            input_image = { "input":  ImageParcel(pixel_array = None,
                                                  dtype = DataType.ImageInt,
                                                  shape = Shape(-1,-1,-1,-1),
                                                  mapping = Shape(0,1,2,3))},
            input_parameter = None,
            output_image = None,
            output_parameter = {"output2": ParameterParcel(value=None,
                                                           dtype = DataType.ValueInt)}
            )
    def execute(self):
        self.output_parameter["output2"].value = np.uint8(2)