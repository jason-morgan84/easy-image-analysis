from core.image_operation import ImageOperation, ImageParcel
from core.shape import Shape
from core.constants import DataType

version = "0.1.0"

class MissingInputImage(ImageOperation):
    def __init__(self):
        super().__init__(
            name = "Missing Input Image",
            category = "Testing",
            version = "0.1",
            docs = "Contains no input_image",
            alerts = None,
            input_image = None,
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