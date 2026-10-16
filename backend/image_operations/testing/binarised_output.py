from core.image_operation import ImageOperation
from core.metadata import ImageMetadata
from core.shape import Shape
from core.constants import DataPolicy
import numpy as np

version = "1.0.0"
class BinarisedOutput(ImageOperation):
    
    def __init__(self):
        super().__init__(
            name="Binarised output",
            id="binarised_output",
            category="",
            version="1.0.0",
            docs="Returns a binary image of same size as input",
            alerts=None,
            input_image_metadata={ "input":  ImageMetadata(dtype=DataPolicy.ImageInt,
                                                  image_shape_constraints=Shape(c=-1, z=-1, y=-1, x=-1),
                                                  image_map=Shape(c=0, z=1, y=2, x=3))},
            output_image_metadata={ "output": ImageMetadata(dtype=DataPolicy.ImageBinary,
                                                     image_shape_constraints=Shape(c=-1, z=-1, y=-1, x=-1),
                                                     image_map=Shape(c=0, z=1, y=2, x=3))}, 
            )
    def execute(self):
        input_image_array = self.input_image["input"]
        output = []
        for c in input_image_array:
            newc=[]
            for z in c:
                newz = []
                for y in z:
                    newy = []
                    for x in y:
                        newy.append(np.uint8(round(x/255)))
                    newz.append(newy)
                newc.append(newz)
            output.append(newc)
        self.output_image={"output":np.array(output,np.uint8)}

