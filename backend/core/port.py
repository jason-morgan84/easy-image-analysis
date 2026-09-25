from core.image import Image
from core.parameter import Parameter
from core.image_operation import ImageParcel, ParameterParcel
from constants import DataType

class Port:
    def __init__(self,is_node_input,image_operation_ID):
        self.is_node_input = is_node_input
        self.image_operation_ID = image_operation_ID
        self.connection_id = None
        self.input = None
        self.output = None

    @property
    def is_node_input(self):
        return self._is_node_input

    @is_node_input.setter
    def is_node_input(self, flag):
        if not isinstance(flag, bool):
            raise TypeError(f"expected type bool for is_node_input flag, got {type(flag)}")

        self._is_node_input = flag

    @property
    def output(self):
        """Converts input data on demand."""
        if self._input is None:
            return None

        return self.convert()

    def convert(self):
        """Function to convert input data to correct output data type"""
        """First, checks if this Port is connected to a node input or output"""
        if self.is_node_input is True:
            """if its an input, self.input will be Image or Parameter class"""
            # if its Image class, give output as ImageParcel
            if isinstance(input,Image):
                image_dtype = getattr(input.pixel_array, "data_type")
                image_pixel_array = input.pixel_array.to_numpy()
                image_map = input.image_map
                output = ImageParcel(dtype = image_dtype,
                                          pixel_array = image_pixel_array,
                                          mapping = image_map)

            # if input is Parameter class, give output as ParameterParcel
            elif isinstance(input,Parameter):
                parameter_dtype = getattr(input.value, "data_type")
                parameter_value = input.value.to_numpy()
                parameter_shape = parameter_value.shape if parameter_dtype in DataType.array_types() else None
                output = ParameterParcel(dtype = parameter_dtype,
                                              value = parameter_value,
                                              shape = parameter_shape)
            else:
                raise TypeError(f"Expected input of Image or Parameter class, got {type(input)}")
        elif self.is_node_input is False:
            """if its an output, self.input will be ImageParcel or ParamaterPackage class"""
            # if its ImageParcel class, give output as Image
            if isinstance(input,ImageParcel):
                image_dtype = input.dtype
                image_pixel_array = image_dtype(input.pixel_array)
                image_map = input.mapping
                output = Image(pixel_array = image_pixel_array,
                                    image_map = image_map)

            # if input is ParameterParcel class, give output as Parameter
            elif isinstance(input,Parameter):
                parameter_dtype = input.dtype
                parameter_value = image_dtype(input.value)
                parameter_name = self.image_operation_ID
                output = Parameter(value = parameter_value,
                                        name = parameter_name)
            else:
                raise TypeError(f"Expected input of Image or Parameter class, got {type(input)}")
        else:
            raise ValueError(f"expected True of False for is_node_input flag, got {self.is_node_input}")
        return output
