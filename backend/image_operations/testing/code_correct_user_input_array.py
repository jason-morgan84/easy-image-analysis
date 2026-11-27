from core.image_operation import ImageOperation
from core.metadata import ImageMetadata, ParameterMetadata
from core.shape import Shape
from core.constants import DataPolicy

version = "1.0.0"
class CodeCorrectUserInputArray(ImageOperation):  
    def __init__(self):
        super().__init__(
            name="Code Correct User Input Array",
            id="code_correct_user_input_array",
            category="",
            version="1.0.0",
            docs="Correct code that only returns an image with a user input parameter for an array",
            alerts=None,
            input_image_metadata={"input":  ImageMetadata(dtype=DataPolicy.ImageInt,
                                                          image_shape_constraints=Shape(c=-1, z=-1, y=-1, x=-1),
                                                          image_map=Shape(c=0, z=1, y=2, x=3))},
            input_parameter_metadata = {"parameter": ParameterMetadata(dtype=DataPolicy.ArrayInt,
                                                              user_input=True,
                                                              ui_element="slider",
                                                              ui_element_options={"default": [2,1]})},
            output_image_metadata = { "output": ImageMetadata(dtype=DataPolicy.ImageInt,
                                                              image_shape_constraints=Shape(c=-1, z=-1, y=-1, x=-1),
                                                              image_map=Shape(c=0, z=1, y=2, x=3))},
            output_parameter = None
            )
    def execute(self):
        input_image_array = self.input_image["input"]
        output = input_image_array.copy()
        self.output_image={"output":output}