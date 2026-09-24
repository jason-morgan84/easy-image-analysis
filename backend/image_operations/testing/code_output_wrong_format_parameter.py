from core.image_operation import ImageOperation, ImageParcel,ParameterParcel
from core.shape import Shape
from core.constants import DataType

version = "0.1.0"
class CodeOutputWrongFormatParameter(ImageOperation):
    
    def __init__(self):
        super().__init__(
            name = "Code output wrong format parameter",
            category = "",
            version = "0.2",
            docs = "Returns an int as output parameter, not ParameterParcel class",
            alerts = None,
            input_image = { "input":  ImageParcel(pixel_array = None,
                                                  dtype = DataType.ImageInt,
                                                  shape = Shape(-1,-1,-1,-1),
                                                  mapping = Shape(0,1,2,3))},
            input_parameter = None,
            output_image = None,
            output_parameter = {"output": ParameterParcel(value = None,
                                                          dtype=DataType.ValueInt)}
            )
    def execute(self):
        self.output_parameter["output"] = 15

