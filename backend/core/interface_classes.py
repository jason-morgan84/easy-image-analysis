from core.error_handling import ConnectionError
from core.image import Image
from core.parameter import Parameter
from core.image_operation import ImageParcel, ParameterParcel
from core.constants import DataType
from core.image_operation import ImageOperation

"""Connection is an extremely simple class that exists only to point an output Port from one Node to the input Port of the next.
It has an input (expected Node class), an output (expected Node class) and an ID (defined by the WorkFlow class on the Connection's instantiation)"""

class Connection:
    def __init__(self, connection_id, input_port, output_port, input_data, output_data):
        self.connection_id = connection_id
        self.input_port = input_port
        self.output_port = output_port
        self.input_data = input_data
        self.output_data = output_data

    @property
    def input_port(self):
        return self._input_port

    @input_port.setter
    def input_port(self, port):
        if not isinstance(port, Port):
            raise ConnectionError(f"port class expected as input_port to connection {self.connection_id}, not {type(port)}")

        self._input = port

    @property
    def output_port(self):
        return self._output_port

    @output_port.setter
    def output_port(self, port):
        if not isinstance(port, Port):
            raise ConnectionError(f"port class expected as output_port to connection {self.connection_id}, not {type(port)}")

        self._output_port = port



"""A port converts data to/from DataTypes used in data transport through the graph and equivalent numpy types used in ImageOperations.
They are instantiated by Nodes, with respect to the inputs and outputs required by the Node's ImageOperation.

There are key differences between input ports (is_input = True) and output ports (is_input = False).
Output ports:
    - cache their input (as an Package class)
    - convert their input to a DataType
    - cache their output.
Input ports:
    - input is a reference to where their data can be found (an output of an output node, via a Connection). 
    - convert their input to a Package class containing a standard numpy data type.
    - cache their output.
"""
class Port:
    def __init__(self, is_input, port_id, node_id, input_connection = None, output_connection = None, input_data = None, output_data = None):
        self.is_input = is_input        # flags as an input (True) or output (False) 
        self.port_id = port_id          # own ID value, set during instatiation
        self.node_id = node_id          # Nodes identifier, set during instantiation
        self.input_connection = input_connection
        self.output_connection = output_connection
        self.input_data = input_data
        self.output_data = output_data

    @property
    def is_input(self):
        return self._is_input

    @is_input.setter
    def is_input(self, flag):
        if not isinstance(flag, bool):
            raise TypeError(f"expected type bool for is_input flag, got {type(flag)}")

        self._is_input = flag

    @property
    def input_connection(self):
        return self._input_connection

    @input_connection.setter
    def input_connection(self, value):
        if value:
            """check the input_connection. if is_input, input_connection should be a connection. if !is_input, input should be an ImageOperation class."""
            if self.is_input:
                if not isinstance(value, Connection):
                    raise TypeError(f"for an input port, expected input_connection as connection class, not {type(value)}; port: {self.port_id}")

            else:
                if not isinstance(value, ImageOperation):
                    raise TypeError(f"for an output port, expected input_connection as ImageOpeartion class not {type(value)}; port: {self.port_id}")

        self._input_connection = value

    @property
    def output_connection(self):
        return self._output_connection

    @output_connection.setter
    def output_connection(self, value):
        if value:
            """check the output_connection. if is_input, output_connection should be a ImageOperation. if !is_input, input should be a Connection class."""
            if self.is_input:
                if not isinstance(value, ImageOperation):
                    raise TypeError(f"for an input port, expected output_connection as ImageOperation class, not {type(value)}; port: {self.port_id}")

            else:
                if not isinstance(value, Connection):
                    raise TypeError(f"for an output port, expected output_connection as Connection class not {type(value)}; port: {self.port_id}")

        self._output_connection = value



    @property
    def output_data(self):
        """Converts input data on demand."""
        if self.input_data is None:
            return None
        return self.convert()

    @output_data.setter
    def output_data(self, value):
        self._output_data = value

    def convert(self):
        """Function to convert input data to correct output data type"""
        """First, checks if this Port is connected to a node input or output"""
        if self.is_input is True:
            data_to_convert = self.input_data
            """if its an input, self.input will be Image or Parameter class"""
            # if its Image class, give output as ImageParcel
            if isinstance(data_to_convert, Image):
                image_dtype = getattr(data_to_convert.pixel_array, "data_type")
                image_pixel_array = data_to_convert.pixel_array.to_numpy()
                image_map = data_to_convert.image_map
                output = ImageParcel(dtype = image_dtype,
                                          pixel_array = image_pixel_array,
                                          mapping = image_map)

            # if input is Parameter class, give output as ParameterParcel
            elif isinstance(data_to_convert,Parameter):
                parameter_dtype = getattr(data_to_convert.value, "data_type")
                parameter_value = data_to_convert.value.to_numpy()
                parameter_shape = parameter_value.shape if parameter_dtype in DataType.array_types() else None
                output = ParameterParcel(dtype = parameter_dtype,
                                              value = parameter_value,
                                              shape = parameter_shape)
            else:
                raise TypeError(f"Expected input of Image or Parameter class, got {type(data_to_convert)}")
        elif self.is_input is False:
            data_to_convert = self.input_data
            """if its an output, self.input will be ImageParcel or ParamaterPackage class"""
            # if its ImageParcel class, give output as Image
            if isinstance(data_to_convert,ImageParcel):
                image_dtype = data_to_convert.dtype
                image_pixel_array = image_dtype(data_to_convert.pixel_array)
                image_map = data_to_convert.mapping
                output = Image(pixel_array = image_pixel_array,
                                    image_map = image_map)

            # if input is ParameterParcel class, give output as Parameter
            elif isinstance(data_to_convert,ParameterParcel):
                parameter_dtype = data_to_convert.dtype
                parameter_value = parameter_dtype(data_to_convert.value)
                parameter_name = self.node_id
                output = Parameter(value = parameter_value,
                                        name = parameter_name)
            else:
                raise TypeError(f"Expected input of ImageParcel or ParameterParcel class, got {type(data_to_convert)}")
        else:
            raise ValueError(f"expected True of False for is_input flag, got {self.is_node_input}")
        return output
