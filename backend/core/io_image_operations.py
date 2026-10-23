from core.image_operation import ImageOperation
from core.metadata import ImageMetadata, ParameterMetadata
from core.shape import Shape
from core.constants import DataPolicy
import tifffile
from core.data_checks import sample_data


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
        path = self.input_parameter_metadata["path"]

        try:
            imported_image = tifffile.imread(path)
        except Exception as e:
            raise ImportError(f"failed to import image from tiff file: {e}")

        try:
            imported_image = self.output_image_metadata["output"].dtype.numpy(imported_image)
        except Exception as e:
            raise ImportError(f"failed to convert imported image into defined dtype: {e}")

        # check for missing dimensions and add to front 
        shape = self.input_parameter_metadata["shape"]
        if shape:
            if len(shape) != len(Shape.dimensions):
                raise ValueError(f"for load image, shape parameter has incorrect length")

            imported_image.transpose(self.input_parameter_metadata["shape"])

        self.output_image={"output":imported_image}
    
    def load_image(self, path, shape):
        self.input_parameter_metadata["path"] = path
        self.input_parameter_metadata["shape"] = shape
        try:
            self.execute()
            return self.output_image["output"]
        except Exception as e:
            raise ImportError(f"failed to load image {path}: {e}")





class TestLoadImage(ImageOperation):
    def __init__(self):
        super().__init__(
            name="Test Load Image",
            id="test_load_image",
            category="Input/Output",
            version="1.0.0",
            docs="creates sample data based on input_parameters",
            alerts=None,
            input_image_metadata={},
            input_parameter_metadata={"dtype": ParameterMetadata(dtype=DataPolicy.ValueString, user_input=True, ui_element="load"), 
                                      "shape": ParameterMetadata(dtype=DataPolicy.ArrayInt, shape=[4], user_input=True,ui_element = "text")},
            output_image_metadata={ "output": ImageMetadata(dtype=DataPolicy.ImageInt,
                                                     image_shape_constraints=Shape(c=-1, z=-1, y=-1, x=-1),
                                                     image_map=Shape(c=0, z=1, y=2, x=3))}, 
            )
    def execute(self):
        dtype = self.input_parameter_metadata["dtype"]
        shape = self.input_parameter_metadata["shape"]
        if dtype == "DataPolicy.ImageInt":
            dtype == DataPolicy.ImageInt
        elif dtype == "DataPolicy.ImageFloat":
            dtype == DataPolicy.ImageFloat
        else:
            dtype == DataPolicy.ImageInt
        

        try:
            self.output_image={"output": sample_data(dtype=dtype,shape=shape)}
        except:
            self.output_image={"output": sample_data(dtype=DataPolicy.ImageInt,shape=(1,2,3,4))}


start_nodes = ["load_image","test_load_image"]

io_imageoperations = {"load_image": LoadImage(),"test_load_image":TestLoadImage()}