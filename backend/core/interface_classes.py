import numpy as np
from core.error_handling import ConnectionError, ActivationError, MissingDataError
from core.metadata import ImageMetadata, ParameterMetadata
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
    
    """Copied from Image Class"""
    
    def convert(self, convert):
        if convert not in DataType.image_types():
            raise TypeError(f"images can only be converted to image_types, not {convert}")
        return Image(data = self.data.to(convert), image_metadata = self.image_metadata)

    # tranpose to be moved to WorkFlow
    def transpose(self, new_shape):
        # expect a Shape class
        if not isinstance(new_shape, Shape):
            raise TypeError (f"expected Shape class, got {type(new_shape)}")

        for item in new_shape:
            if item < 0 or item > Shape.max_image_dimensions:
                raise ValueError (f"passed shape dimensions out of range, must be 0-{Shape.max_image_dimensions}")


        # receives Shape class member with new dimensions indices of each array (c,z,y,x)
        # needs to create transpose list with values c,z,y,x in order of old_c,old_z,old_y,old_x
        transpose = [self.data[item] for item in new_shape]

        # receives input of new channel order, such as z,c,y,x
        # to use numpy transpose, needs to go from string z to array map for that dimension and append to list transpose
        # transpose used as input for np.transpose

        # get new shape map - ie, get the position of c,z,y,x in new_shape
        
        transposed_array = np.transpose(self.data.to_numpy(),transpose)

        current_dtype = getattr(self.data, "data_type")

        #self.pixel_array = current_dtype(transposed_array)
        #self.image_map = new_shape
        return Image(data = current_dtype(transposed_array),
                     image_metadata = ImageMetadata(dtype = self.image_metadata.dtype,
                                                    image_shape_constraints = self.image_metadata.image_shape_constraints,
                                                    image_map = new_shape))
    

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
    
    def __init__(self, port_id, node_id, meta_data, data = None, input_connection = None, output_connection = None):
        self.port_id = port_id          # own ID value, set during instatiation
        self.node_id = node_id          # Nodes identifier, set during instantiation
        self.meta_data = meta_data
        self.data = data

    @property
    def meta_data(self):
        return self._meta_data

    @meta_data.setter
    def meta_data(self, meta):
        # check that meta_data is set as valid class (ImageMetadata or ParameterMetadata)
        # Metadata class checks its own arguements are valid.
        if not isinstance(meta, ImageMetadata) and not isinstance(meta, ParameterMetadata):
            raise TypeError(f"meta data expected as ImageMetadata or ParameterMetadata class for {self.port_id}, got: {type(meta)}")
        self._meta_data = meta

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        # checks if meta_data set - can't set or check data without defining meta-data present
        if not self.meta_data:
            raise MissingDataError(f"attempt to set port data with missing meta_data: {self.port_id}")
        # if meta_data defines dtype as a value type, expect a scalar value of type dtype.numpy
        if self.meta_data.dtype in DataType.value_types():
            if not isinstance(value, self.meta_data.dtype.numpy):
                raise TypeError(f"data passed to port with unexpected dtype; for port {self.port_id} expected {self.meta_data.dtype}, got {type(value)}")
        # if meta_data defines dtype as an array type or image type, expect a numpy array.
        elif self.meta_data.dtype in DataType.image_types() or self.meta_data.dtype in DataType.array_types():
            if not isinstance (value, np.ndarray):
                raise TypeError(f"data passed to port with unexpected dtype; for port {self.port_id} expected np.ndarray, got {type(value)}")
            # of type meta_data.dtype.numpy
            if value.dtype is not self.meta_data.dtype.numpy:
                raise TypeError(f"data passed to port with unexpected dtype; for port {self.port_id} expected {self.meta_data.dtype.numpy}, got {value.dtype}")
            # with a shape that matches constraints of meta_data
            # for ImageTypes: meta_data.image_shape_constraints and meta_data.image_map
            if self.meta_data.dtype in DataType.image_types():
                # goes through each dimension in Shape.dimensions (should be c,z,y,x)
                for dim in Shape.dimensions:
                    # gets constrain and mapping value for that dimension
                    try:
                        dim_constraint = getattr(self.meta_data.image_shape_constraints, dim)
                        dim_map = getattr(self.meta_data.image_map, dim)
                    except:
                        # raises a ValueError if that dimension isn't present. This should NEVER happen, if it does, fix Shape.dimensions to match the Shape class instance arguements
                        raise ValueError(f"dimension present in Shape.dimensions that is not a Shape arguement, {dim}")
                    # if the constraint is not -1 (where -1 = don't care about shape)
                    if dim_constraint!= -1:
                        # check the array dimension that maps to the constrained dimension matches the expected size
                        if value.shape[dim_map] != dim_constraint:
                            # if not, raise ValueError
                            raise ValueError(f"image_type passed to port with incorrect shape; for port {self.port_id}, \
                                             expected {dim} = {dim_constraint}, got {dim} = {value.shape[dim_map]}")

            # for ArrayTypes: meta_data.shape
            elif self.meta_data.dtype in DataType.array_types():
                if value.shape != tuple(self.meta_data.shape):
                    raise ValueError(f"array_type data passed to port with incorrect shape; for port {self.port_id}, expected {self.meta_data.shape}, got {value.shape}")

        # if meta_data defines dtype as something else, raise value error for meta_data.dtype
        # this should never be raised as meta_data.dtype is checked by MetaData class
        else:
            raise ValueError(f"port MetaData defines unexpected dtype; for port {self.port_id} expected DataType member, got {self.meta_data.dtype}")
        self._data = value

    
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