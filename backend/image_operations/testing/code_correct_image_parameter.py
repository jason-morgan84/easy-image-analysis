from core.image_operation import ImageOperation, ImageParcel,ParameterParcel
from core.shape import Shape
from core.constants import DataType
import numpy as np

version = "0.1.0"
class CodeCorrectImageParameter(ImageOperation):
    
    def __init__(self):
        super().__init__(
            name = "Code Correct Image Parameter",
            category = "",
            version = "0.2",
            docs = "Correct code that returns an image and a parameter",
            alerts = None,
            input_image = { "input":  ImageParcel(pixel_array = None,
                                                  dtype = DataType.ImageInt,
                                                  shape = Shape(-1,-1,-1,-1),
                                                  mapping = Shape(0,1,2,3))},
            input_parameter = None,
            output_image = { "output": ImageParcel(pixel_array = None,
                                                   dtype = DataType.ImageInt,
                                                   shape = Shape(-1,-1,-1,-1),
                                                   mapping = None)}, 
            output_parameter = {"output2": ParameterParcel(value=None,
                                                           dtype = DataType.ValueInt)}
            )
    def execute(self):
        input_image_array = self.input_image["input"].pixel_array
        self.output_image["output"].pixel_array = input_image_array.copy()
        self.output_image["output"].mapping = Shape(0,1,2,3)
        self.output_parameter["output2"].value =np.uint8(2)