from core.error_handling import ConnectionError, ActivationError
from core.image import Image
from core.parameter import Parameter
from core.image_operation import ImageParcel, ParameterParcel
from core.constants import DataType
from core.image_operation import ImageOperation
from core.shape import Shape

class Connection:
    """Connection is an extremely simple class that exists only to point an output Port from one Node to the input Port of the next.
    It has an input (expected Node class), an output (expected Node class) and an ID (defined by the WorkFlow class on the Connection's instantiation)"""
    def __init__(self, connection_id, source_port, target_port, transpose = None, convert = None):
        self.connection_id = connection_id
        self.source_port = source_port
        self.target_port = target_port
        self.transpose = transpose # Shape class member describing any transpositions required on input to produce output
        self.convert = convert # Target DataType member for any conversions required on input to produce output

    @property
    def source_port(self):
        return self._source_port

    @source_port.setter
    def source_port(self, port):
        if not isinstance(port, Port):
            raise ConnectionError(f"port class expected as source for connection {self.connection_id}, not {type(port)}")

        self._source_port = port

    @property
    def target_port(self):
        return self._target_port

    @target_port.setter
    def target_port(self, port):
        if not isinstance(port, Port):
            raise ConnectionError(f"port class expected as target for connection {self.connection_id}, not {type(port)}")

        self._target_port = port

    @property
    def transpose(self):
        return self._transpose

    @transpose.setter
    def transpose(self,shape):
        if shape and not isinstance(shape, Shape):
            raise TypeError(f"shape class expected for transpose, not {type(shape)}")
        self._transpose = shape

    @property
    def convert(self):
        return self._convert

    @convert.setter
    def convert(self, convert_type):
        
        if convert_type and convert_type not in DataType.types():
            raise TypeError(f"datatype class expected for transpose, not {type(convert_type)}")
        self._convert = convert_type

    @property
    def output_data(self):
        """Converts input data on demand."""

        if self.source_port.output_data is None or \
            (isinstance(self.source_port.output_data, Parameter) and self.source_port.output_data.value is None) or \
                (isinstance(self.source_port.output_data, Image) and self.source_port.output_data.pixel_array is None):
            raise ConnectionError(f"attempt to get output where source_port.output_data has no data present: {self.port_id}")
        output = self.source_port.output_data
        print("\n\noutput\n\n", output)
        # if tranpose is not None and the source data is an image, transpose it
        if self.transpose and isinstance(output, Image):
            output = output.transpose(self.transpose)
        print("\n\noutput\n\n", output)
        # if convert is not None, convert it
        if self.convert:
            output = output.convert(self.convert)
        print("\n\noutput\n\n", output)
        return output

    @output_data.setter
    def output_data(self, value):
        self._output_data = value


class Port:
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
        if self.input_data is None or \
            (isinstance(self.input_data, ImageParcel) and self.input_data.pixel_array is None) or \
                (isinstance(self.input_data, ParameterParcel) and self.input_data.value is None):
            raise ConnectionError(f"attempt to get port output where no input present: {self.port_id}")
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
                                          image_map = image_map)

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
                image_map = data_to_convert.image_map
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

class Node:
    """
    The Node class is a hanger for an ImageOperation and its associated inputs/outputs.
    It is responsible for positioning an ImageOperation in the WorkFlow. 
    There can be multiple nodes containing the same ImageOperation. 
    On instantiation, the Node creates Ports to provide inputs and outputs to the associated ImageOperation. 
    Data travels through these Ports to the ImageOperation; the Node class itself does not handle any data.
    """
    def __init__(self, image_operation, node_id):
        self.node_id = node_id
        self.image_operation = image_operation
        self.is_ready = False
        self.needs_update = True

        self.input_ports = {}
        self.initialise_input_ports()

        self.output_ports = {}
        self.initialise_output_ports()

    # checks that image_operation arguement is a valid member of ImageOperation class on setting
    @property
    def image_operation(self):
        return self._image_operation

    @image_operation.setter
    def image_operation(self, operation):
        if not isinstance (operation, ImageOperation):
            raise TypeError(f"ImageOperation class expected for image_operation for {self.node_id}, got {type(operation)}")
        self._image_operation = operation

    # on Node instantiation, initialises the Node input Ports by creating a Port for each input_image and input_parameter in
    # the associated ImageOperation
    def initialise_input_ports(self):
        for key in self.image_operation.input_image.keys():
            port_id = "image." + str(key)
            self.input_ports[port_id] = Port(is_input = True,
                                              port_id = port_id,
                                              node_id = self.node_id)
            
        for key in self.image_operation.input_parameter.keys():
            port_id = "parameter." + str(key)
            self.input_ports[port_id] = Port(is_input = True,
                                              port_id = port_id,
                                              node_id = self.node_id)
    # on Node instantiation, initialises the Node output Ports by creating a Port for each input_image and input_parameter in
    # the associated ImageOperation
    def initialise_output_ports(self):
        for key in self.image_operation.output_image.keys():
            port_id = "image." + str(key)
            self.output_ports[port_id] = Port(is_input = False,
                                              port_id = port_id,
                                              node_id = self.node_id)
            
        for key in self.image_operation.output_parameter.keys():
            port_id = "parameter." + str(key)
            self.output_ports[port_id] = Port(is_input = False,
                                              port_id = port_id,
                                              node_id = self.node_id)

    def activate_node(self):
        # only activate node if ready
        if self.is_ready is False:
            raise ActivationError(f"node activated when is_ready set to False: {self.node_id}")
        else:
            # Reset ImageOperation inputs and outputs
            self.image_operation.reset_input()
            self.image_operation.reset_output()

            # Give ImageOperation inputs references to outputs from relevant Ports
            self.reference_input_data()

            # Run ImageOperation
            self.image_operation.run_code()

            # Cache ImageOperation output to inputs of relevant output Ports
            self.cache_output_data()

            # Reset ImageOperation inputs and outputs
            self.image_operation.reset_input()
            self.image_operation.reset_output()
  
    def reference_input_data(self):
        # go through each input port
        for port_id, port in self.input_ports.items():
            # port ids are made up of type.name. Split into type and name
            try:
                port_type, port_name = port_id.split(".")
            except:
                raise ValueError(f"invalid port_id for input port {port_id}, node {self.node_id}")

            # if port is for an image
            if port_type == "image":
                # if port_name is not a valid reference to a key in the image_operation input_image dictionary, raise an error
                if port_name not in self.image_operation.input_image.keys():
                    raise ActivationError(f"node activated where input port name not present in ImageOperation input dictionary: port {port_id} in node {self.node_id}")
                # if the input port contains pixel_array data, set the relevant image_operation input_image pixel_array to a reference to the port output
                if port.output_data.pixel_array is not None:
                    self.image_operation.input_image[port_name].pixel_array = port.output_data.pixel_array
                # else raise an error
                else:
                    raise ActivationError(f"node activated when input pixel_array not present: port {port_id} in node {self.node_id}")
                # if the input port contains image_map data, set the relevant image_operation input_image image_map to a reference to the port output
                if port.output_data.image_map is not None:
                    self.image_operation.input_image[port_name].image_map = port.output_data.image_map
                else:
                    # else raise an error
                    raise ActivationError(f"node activated when input image_map not present: port {port_id} in node {self.node_id}")

            # if port is for a parameter
            elif port_type == "parameter":
                # if port_name is not a valid reference to a key in the image_operation input_image dictionary, raise an error
                if port_name not in self.image_operation.input_parameter.keys():
                    raise ActivationError(f"node activated where input port name not present in ImageOperation input dictionary: port {port_id} in node {self.node_id}")
                # if the input port contains value data, set the relevant image_operation input_image value to a reference to the port output
                if port.output_data.value:
                    self.image_operation.input_parameter[port_name].value = port.output_data.value
                else:
                        # else raise an error
                        raise ActivationError(f"node activated when input value not present: port {port_id} in node {self.node_id}")
   
    def cache_output_data(self):
        # go through each output port
        for port_id, port in self.output_ports.items():
            # port ids are made up of type.name. Split into type and name
            try:
                port_type, port_name = port_id.split(".")
            except:
                raise ValueError(f"invalid port_id for output port {port_id}, node {self.node_id}")
             # if port is for an image
            if port_type == "image":
                # if port_name is not a valid reference to a key in the image_operation output_image dictionary, raise an error
                if port_name not in self.image_operation.output_image.keys():
                    raise ActivationError(f"node activated where output image port name not present in ImageOperation output dictionary: port {port_id} in node {self.node_id}")
                image_to_cache = self.image_operation.output_image[port_name]
                # if the image_operation output dictionary contains pixel_array, shape and image_map data, 
                # set the relevant output_port to an ImageParcel with those variables.
                if image_to_cache.pixel_array is not None and image_to_cache.image_map is not None and image_to_cache.shape is not None:
                    port.input_data = ImageParcel(dtype = image_to_cache.dtype,
                                                  pixel_array = image_to_cache.pixel_array,
                                                  image_map = image_to_cache.image_map,
                                                  shape = image_to_cache.shape)
                # else raise an error
                else:
                    raise ActivationError(f"node activated but expected output data not complete: port {port_id} in node {self.node_id}")
                # if the image_operation output dictionary contains image_map data, 
                # set the relevant output_port image_map to a copy of the ImageOperation output
            elif port_type == "parameter":
                # if port_name is not a valid reference to a key in the image_operation output_image dictionary, raise an error
                if port_name not in self.image_operation.output_parameter.keys():
                    raise ActivationError(f"node activated where output parameter port name not present in ImageOperation output dictionary: port {port_id} in node {self.node_id}")
                parameter_to_cache = self.image_operation.output_parameter[port_name]
                # if the image_operation output dictionary contains value data, 
                # set the relevant output_port pixel_array to a copy of the ImageOperation output
                if parameter_to_cache.value is not None:
                    port.input_data = ParameterParcel(dtype = parameter_to_cache.dtype,
                                                      value = parameter_to_cache.value,
                                                      shape = parameter_to_cache.shape)
                # else raise an error
                else:
                    raise ActivationError(f"node activated but expected output value not created: port {port_id} in node {self.node_id}")