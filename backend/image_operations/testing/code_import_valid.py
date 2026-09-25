from core.image_operation import ImageOperation, ImageParcel
from core.shape import Shape
from core.constants import DataType
import math
from numpy import ndarray

version = "0.1.0"
class SameImage(ImageOperation):
    
    def __init__(self):
        super().__init__(
            name = "Same Image",
            category = "",
            version = "0.2",
            docs = "Returns an identical image to that inserted",
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
            output_parameter = None
            )
    def execute(self):
        input_image_array = self.input_image["input"].pixel_array
        self.output_image["output"].pixel_array = input_image_array.copy()
        self.output_image["output"].mapping = Shape(0,1,2,3)
