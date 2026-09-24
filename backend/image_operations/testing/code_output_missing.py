from core.image_operation import ImageOperation, ImageParcel
from core.shape import Shape
from core.constants import DataType

version = "0.1.0"

class CodeOutputMissing(ImageOperation):
    def __init__(self):
        super().__init__(
            name = "Code no output",
            category = "Testing",
            version = "0.1",
            docs = "Doesn't provide an output",
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
        self.output_parameter = {}
        self.output_image = {}
