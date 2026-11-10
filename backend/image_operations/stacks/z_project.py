
"""standard imports required for all ImageOperation"""
from core.image_operation import ImageOperation
from core.metadata import ImageMetadata, ParameterMetadata
from core.shape import Shape
from core.constants import DataPolicy

"""specific imports required for this function"""

from scipy import ndimage
import numpy as np

version = "1.0.0"


class ZProject(ImageOperation):
    
    def __init__(self):
        super().__init__(
            name="Z-Project",
            id="z_project", 
            category="",
            version="",
            # An explanation to the user of what the function does and what its inputs are
            docs= "Flattens a z-stack image to a single slice. Either uses the maximum intensity, minimum intensity, sum of the intensity or mean intensities across slices",
            alerts=None, 
           
           
            
           
            input_image_metadata={ "input":  ImageMetadata(dtype=DataPolicy.ImageInt, 
                                                  image_shape_constraints=Shape(c=-1, z=-1, y=-1, x=-1), 
                                                  image_map=Shape(c=0, z=1, y=2, x=3))},
            input_parameter_metadata={"method": ParameterMetadata(dtype=DataPolicy.ValueString, 
                                                                 user_input=True,
                                                                 ui_element="dropdown",
                                                                 ui_element_options={"values":["Sum intensity", "Mean intensity", "Min intensity", "Max intensity" ]})},
            output_image_metadata={ "output": ImageMetadata(dtype=DataPolicy.ImageInt,
                                                     image_shape_constraints=Shape(c=-1, z=1, y=-1, x=-1),
                                                     image_map=Shape(c=0, z=1, y=2, x=3))},

            )
        
        self.test_input_parameters = {"method": "Mean intensity"} 
            
    def execute(self):
        """ get inputs from input dictionaries:"""
        input_image = self.input_image["input"]
        method = self.input_parameter["method"]

        """check method parameter is valid"""
        projection_methods = {"Sum intensity": self.sum_project,
                              "Mean intensity": self.mean_project,
                              "Min intensity": self.min_project,
                              "Max intensity": self.max_project}

        if method not in projection_methods.keys():
            raise ValueError(f"invalid projection method provided")
        input_c,input_z,input_y,input_x = input_image.shape
        if input_z == 1:
            raise ValueError(f"can't z-project a single z-slice image")

        # craete empty output image

        output_image = np.zeros([input_c,1,input_y, input_x],np.uint8)
        for c, channel in enumerate(input_image):
            output_image[c][0] = projection_methods[method](channel)
            

        self.output_image={"output": output_image}

    def sum_project(self, image):
        z_slices, _, _ = image.shape
        summed_image = np.sum(image, axis = 0)
        output = (summed_image/z_slices).astype(np.uint8)
        return output

    def max_project(self, image):
        max_image = np.max(image, axis = 0).astype(np.uint8)
        return max_image

    def min_project(self, image):
        min_image = np.min(image, axis = 0).astype(np.uint8)
        return min_image

    def mean_project(self, image):
        mean_image = np.mean(image, axis = 0).astype(np.uint8)
        return mean_image








