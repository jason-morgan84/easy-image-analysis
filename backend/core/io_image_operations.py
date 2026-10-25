from core.image_operation import ImageOperation
from core.metadata import ImageMetadata, ParameterMetadata
from core.shape import Shape, transpose
from core.constants import DataPolicy
import tifffile
from core.error_handling import ExportError
from core.data_checks import sample_data
import os


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
            input_parameter_metadata={"path": ParameterMetadata(dtype=DataPolicy.ValueString, user_input=True, ui_element="load"), 
                                      "shape": ParameterMetadata(dtype=DataPolicy.ValueString, user_input=True,ui_element = "text")},
            output_image_metadata={ "output": ImageMetadata(dtype=DataPolicy.ImageInt,
                                                     image_shape_constraints=Shape(c=-1, z=-1, y=-1, x=-1),
                                                     image_map=Shape(c=0, z=1, y=2, x=3))}, 
            )
    def execute(self):
        path = self.input_parameter["path"]
        shape = self.input_parameter["shape"].lower()

        # check file type
        _, file_type = os.path.splitext(path)
        if file_type != ".tif":
            raise ImportError(f"loading of non .tif files not currently implemented")
        # import image file
        try:
            imported_image = tifffile.imread(path)
        except Exception as e:
            raise ImportError(f"failed to import image from tiff file: {e}")

        # convert image file to correct dtype
        try:
            # validate image meets type definition
            self.output_image_metadata["output"].dtype.validate(imported_image)
            imported_image = self.output_image_metadata["output"].dtype.numpy(imported_image)
            
            
        except Exception as e:
            raise ImportError(f"failed to convert imported image into defined dtype: {e}")

        """loaded image could have 2, 3 or 4 dimensions. This is defined by shape, which is a string made up of the included dimensions in order.
        For use in WorkFlow, the image must be converted to 4 dimensions, with currently missing dimensions of size 1"""
        # check number of image dimensions matches shape input
        if len(shape) != len(imported_image.shape):
            raise ValueError(f"when loading image, number of dimensions in image pixel array does not match expected shape: '{shape}' does is not of length {(len(imported_image.shape))}")

        # check shape only includes expected dimension identifiers (given list in Shape.dimensions)
        for dimension in shape:
            if dimension not in Shape.dimensions:
                raise ValueError(f"when loading image, shape includes unexpected dimension identifier '{dimension}'")

        # check each dimension identifier only appears once
        for dimension in Shape.dimensions:
            if shape.count(dimension) > 1:
                raise ValueError(f"when loading image, shape includes duplicated dimension identifier '{dimension}")
        
        # check for missing dimensions and add to end 
        image_map = Shape(c=shape.find("c"), z=shape.find("z"), y=shape.find("y"), x=shape.find("x"))

        # loop through dimensions
        try:
            for dimension in Shape.dimensions:
                # if a dimension is not present (-1)
                if getattr(image_map, dimension) == -1:
                    new_shape = list(imported_image.shape)
                    new_shape.append(1)
                    imported_image = imported_image.reshape(new_shape)
                    setattr(image_map, dimension, len(imported_image.shape) - 1)
        except Exception as e:
            raise ImportError(f"error reshaping loaded image: {e}")

        # transpose to shape defined in output metadata
        try:
            imported_image = transpose(value=imported_image,
                                    current_shape=image_map,
                                    new_shape=self.output_image_metadata["output"].image_map)
        except Exception as e:
            raise ImportError(f"error transposing loaded image: {e}")

        self.output_image={"output":imported_image}
    
    def load_image(self, path, shape):
        self.input_parameter = {"path": path, "shape": shape}
        try:
            self.run_code()
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
                                      "shape": ParameterMetadata(dtype=DataPolicy.ArrayInt, user_input=True, ui_element = "text")},
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




class SaveImage(ImageOperation):
        def __init__(self):
            super().__init__(
                name="Save Image",
                id="save_image",
                category="Input/Output",
                version="1.0.0",
                docs="Saves an image given to a path",
                alerts=None,
                input_image_metadata={"input": ImageMetadata(dtype=DataPolicy.ImageInt,
                                                        image_shape_constraints=Shape(c=-1, z=-1, y=-1, x=-1),
                                                        image_map=Shape(c=0, z=1, y=2, x=3))}, 
                input_parameter_metadata={"path": ParameterMetadata(dtype=DataPolicy.ValueString, user_input=True, ui_element="load")},
                )

        def execute(self):
            path = self.input_parameter["path"]
            image = self.input_image["input"]

            # check file type
            _, file_type = os.path.splitext(path)
            if file_type != ".tif":
                raise ImportError(f"saving non .tif files not currently implemented")

            # transpose to correct output order for imagej output
            output_image = transpose(value=image,
                                     current_shape=Shape(c=0, z=1, y=2, x=3),
                                     new_shape=Shape(c=1, z=0, y=2, x=3))
            
            try:
                tifffile.imwrite(path, output_image, metadata={'axes': 'ZCYX'},imagej=True)
            except Exception as e:
                raise ExportError(f"failed saving image: {e}")
            
        def save_image(self, image, path):
            self.input_parameter = {"path": path}
            self.input_image = {"input": image}
            try:
                self.run_code()
            except Exception as e:
                raise ImportError(f"failed to save image {path}: {e}")

start_nodes = ["load_image","test_load_image"]

io_imageoperations = {"load_image": LoadImage(),"test_load_image":TestLoadImage(), "save_image": SaveImage()}