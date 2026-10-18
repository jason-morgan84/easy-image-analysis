from core.image_operation import ImageOperation
from core.metadata import ImageMetadata, ParameterMetadata
from core.shape import Shape
from core.constants import DataPolicy
import tifffile


class LoadImage(ImageOperation):
    def __init__(self):
        super().__init__(
            name="Load Image",
            id="load_image",
            category="Input/Output",
            version="1.0.0",
            docs="Loads an image given a path (as string) and shape as array of integers defining array dimensions of c, z, y and x in order",
            alerts=None,
            input_image_metadata={},
            input_parameter_metadata={"path": ParameterMetadata(dtype=DataPolicy.ValueString, user_input=True, ui_element="load"), "shape": ParameterMetadata(dtype=DataPolicy.ArrayInt, user_input=True,ui_element = "text")},
            output_image_metadata={ "output": ImageMetadata(dtype=DataPolicy.ImageInt,
                                                     image_shape_constraints=Shape(c=-1, z=-1, y=-1, x=-1),
                                                     image_map=Shape(c=0, z=1, y=2, x=3))}, 
            )
    def execute(self):
        path = self.input_parameter["path"]

        try:
            imported_image = tifffile.imread(path)
        except:
            raise ImportError(f"failed to import image from tiff file")

        try:
            imported_image = self.output_image_metadata["output"].dtype.numpy(imported_image)
        except:
            raise ImportError(f"failed to convert imported image into defind dtype")
        
        shape = self.input_parameter["shape"]
        if shape is not None:
            if len(shape) != len(Shape.dimensions):
                raise ValueError(f"for load image, shape parameter has incorrect length")

            imported_image.transpose(self.input_parameter["shape"])

        self.output_image={"output":imported_image}

start_nodes = ["load_image"]

io_imageoperations = {"load_image": LoadImage()}