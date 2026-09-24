from core.image_operation import ImageOperation, ImageParcel,ParameterParcel
from core.shape import Shape
from core.constants import DataType

version = "0.1.0"
class CodeOutputMissingArguementParameterValue(ImageOperation):
    
    def __init__(self):
        super().__init__(
            name = "Code output missing arguement parameter value",
            category = "",
            version = "0.2",
            docs = "Returns an output parameter as ParameterParcel class with missing value",
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
        print("no output parameter value set")

