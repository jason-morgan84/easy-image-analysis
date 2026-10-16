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
    
class Port:
    """
    The port class acts as a buffer between a Node and an ImageOperation. 
    Its role is to hold metadata requirements of the ImageOperation and cache input or output data.
    """
    def __init__(self, port_id, node_id, metadata, is_input, data = None):
        self.port_id = port_id          # own ID value, set during instatiation
        self.node_id = node_id          # Nodes identifier, set during instantiation
        self.metadata = metadata
        self.data = data
        self.is_input = is_input


    @property
    def port_id(self):
        return self._port_id

    @port_id.setter
    def port_id(self, id):
        # check that port_id exists
        if not id:
            raise ValueError(f"port_id required for port instantiation")
        self._port_id = id

    @property
    def node_id(self):
        return self._node_id

    @node_id.setter
    def node_id(self, id):
        # check that node_id exists
        if not id:
            raise ValueError(f"node_id required for port instantiation")
        self._node_id = id

    @property
    def is_input(self):
        return self._is_input

    @is_input.setter
    def is_input(self, flag):
        # check that flag is boolean
        if flag is None:
            raise ValueError(f"is_input flag not set for port '{self.port_id}'")
        if not isinstance(flag, bool):
            raise TypeError(f"is_input flag expected boolean, got {type(flag)}")
        self._is_input = flag

    @property
    def metadata(self):
        return self._metadata

    @metadata.setter
    def metadata(self, meta):
        # check that metadata is set as valid class (ImageMetadata or ParameterMetadata)
        # Metadata class checks its own arguements are valid.
        if not isinstance(meta, ImageMetadata) and not isinstance(meta, ParameterMetadata):
            raise TypeError(f"meta data expected as ImageMetadata or ParameterMetadata class for {self.port_id}, got: {type(meta)}")
        self._metadata = meta

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        # if metadata defines dtype as a value type, expect a scalar value of type dtype.numpy
        if value is not None:
            if self.metadata.dtype.is_array is False and self.metadata.dtype.is_image is False:
                if not isinstance(value, self.metadata.dtype.numpy):
                    raise TypeError(f"data passed to port with unexpected dtype; for port {self.port_id} expected {self.metadata.dtype.numpy}, got {type(value)}")
            # if metadata defines dtype as an array type or image type, expect a numpy array.
            elif self.metadata.dtype.is_array is True or self.metadata.dtype.is_image is True:
                if not isinstance (value, np.ndarray):
                    raise TypeError(f"data passed to port with unexpected dtype; for port {self.port_id} expected np.ndarray, got {type(value)}")
                # of type metadata.dtype.numpy
                if value.dtype != self.metadata.dtype.numpy:
                    raise TypeError(f"data passed to port with unexpected dtype; for port {self.port_id} expected {self.metadata.dtype.numpy}, got {value.dtype}")
                # with a shape that matches constraints of metadata
                # for ImageTypes: metadata.image_shape_constraints and metadata.image_map
                if self.metadata.dtype.is_image is True:
                    # goes through each dimension in Shape.dimensions (should be c,z,y,x)
                    for dim in Shape.dimensions:
                        # gets constrain and mapping value for that dimension
                        try:
                            dim_constraint = getattr(self.metadata.image_shape_constraints, dim)
                            dim_map = getattr(self.metadata.image_map, dim)
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

                # for ArrayTypes: metadata.shape
                elif self.metadata.dtype.is_array is True:
                    if value.shape != tuple(self.metadata.shape):
                        raise ValueError(f"array_type data passed to port with incorrect shape; for port {self.port_id}, expected {self.metadata.shape}, got {value.shape}")

            # if metadata defines dtype as something else, raise value error for metadata.dtype
            # this should never be raised as metadata.dtype is checked by MetaData class
            else:
                raise TypeError(f"port MetaData defines unexpected dtype; for port {self.port_id} expected DataType member, got {self.metadata.dtype}")
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
        for key, value in self.image_operation.input_image_metadata.items():
            port_id = "image." + str(key)
            input_metadata = ImageMetadata(dtype = value.dtype,
                                           image_shape_constraints=value.image_shape_constraints,
                                           image_map=value.image_map)
            self.input_ports[port_id] = Port(is_input = True,
                                             metadata=input_metadata,
                                             port_id = port_id,
                                             node_id = self.node_id)
        if self.image_operation.input_parameter_metadata is not None:
            for key, value in self.image_operation.input_parameter_metadata.items():
                port_id = "parameter." + str(key)
                input_metadata = ParameterMetadata(dtype=value.dtype,
                                                shape=value.shape)
                self.input_ports[port_id] = Port(is_input = True,
                                                metadata=input_metadata,
                                                port_id = port_id,
                                                node_id = self.node_id)
    # on Node instantiation, initialises the Node output Ports by creating a Port for each input_image and input_parameter in
    # the associated ImageOperation
    def initialise_output_ports(self):
        if self.image_operation.output_image_metadata is not None:
            for key, value in self.image_operation.output_image_metadata.items():
                port_id = "image." + str(key)
                output_metadata = ImageMetadata(dtype = value.dtype,
                                                image_shape_constraints=value.image_shape_constraints,
                                                image_map=value.image_map)
                self.output_ports[port_id] = Port(is_input = False,
                                                  metadata=output_metadata,
                                                  port_id = port_id,
                                                  node_id = self.node_id)
        if self.image_operation.output_parameter_metadata is not None:
            for key, value in self.image_operation.output_parameter_metadata.items():
                port_id = "parameter." + str(key)
                output_metadata = ParameterMetadata(dtype=value.dtype,
                                                    shape=value.shape)
                self.output_ports[port_id] = Port(is_input = False,
                                                  metadata=output_metadata,
                                                  port_id = port_id,
                                                  node_id = self.node_id)

    def activate_node(self):
        # only activate node if ready
        if self.is_ready == False:
            raise ActivationError(f"node activated when is_ready set to False: '{self.node_id}'")
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
        image_inputs = {}
        parameter_inputs = {}
        for port_id, port in self.input_ports.items():
            # port ids are made up of type.name. Split into type and name
            try:
                port_type, port_name = port_id.split(".")
            except:
                raise ValueError(f"invalid port_id for input port '{port_id}', node '{self.node_id}'")
            #if port.data == None:
             #   raise ValueError(f"input port contains no data '{port_id}', node '{self.node_id}'")
            # if port is for an image
            if port_type == "image":
                # if port_name is not a valid reference to a key in the image_operation input_image dictionary, raise an error
                if port_name not in self.image_operation.input_image_metadata.keys():
                    raise ActivationError(f"node activated where input port name not present in ImageOperation input dictionary: port '{port_id}' in node '{self.node_id}'")
                # if the input port contains data, set the relevant image_operation input_image to a reference to the port data
                if port.data is not None:
                    image_inputs[port_name] = port.data
                # else raise an error
                else:
                    raise ActivationError(f"node activated when input not present: port '{port_id}' in node '{self.node_id}'")

            # if port is for a parameter
            elif port_type == "parameter":
                # if port_name is not a valid reference to a key in the image_operation input_image dictionary, raise an error
                if port_name not in self.image_operation.input_parameter_metadata.keys():
                    raise ActivationError(f"node activated where input port name not present in ImageOperation input dictionary: port '{port_id}' in node '{self.node_id}'")
                # if the input port contains value data, set the relevant image_operation input_image value to a reference to the port output
                if port.data is not None:
                    parameter_inputs[port_name] = port.data
                else:
                    # else raise an error
                    raise ActivationError(f"node activated when input value not present: port '{port_id}' in node '{self.node_id}'")
        self.image_operation.input_image = image_inputs if len(image_inputs) > 0 else None
        self.image_operation.input_parameter = parameter_inputs if len(parameter_inputs) > 0 else None
    def cache_output_data(self):
        # go through each output port
        for port_id, port in self.output_ports.items():
            # port ids are made up of type.name. Split into type and name
            try:
                port_type, port_name = port_id.split(".")
            except:
                raise ValueError(f"invalid port_id for output port '{port_id}', node '{self.node_id}'")
             # if port is for an image
            if port_type == "image":
                # if port_name is not a valid reference to a key in the image_operation output_image dictionary, raise an error
                if port_name not in self.image_operation.output_image.keys():
                    raise ActivationError(f"node activated where output image port name not present in ImageOperation output dictionary: port '{port_id}' in node '{self.node_id}'")
                image_to_cache = self.image_operation.output_image[port_name]
                # if the image_operation output dictionary contains data set the relevant output_port.data
                if image_to_cache is not None:
                    port.data = image_to_cache.copy() 
                # else raise an error
                else:
                    raise ActivationError(f"node activated but expected output data not present: port '{port_id}' in node '{self.node_id}'")
            elif port_type == "parameter":
                # if port_name is not a valid reference to a key in the image_operation output_image dictionary, raise an error
                if port_name not in self.image_operation.output_parameter.keys():
                    raise ActivationError(f"node activated where output parameter port name not present in ImageOperation output dictionary: port '{port_id}' in node '{self.node_id}'")
                parameter_to_cache = self.image_operation.output_parameter[port_name]
                # if the image_operation output dictionary contains data, set the relevant output_port to a copy of the output
                if parameter_to_cache is not None:
                    port.data = parameter_to_cache.copy()

                # else raise an error
                else:
                    raise ActivationError(f"node activated but expected output value not created: port '{port_id}' in node '{self.node_id}'")