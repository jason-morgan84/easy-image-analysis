from core.image_operation_directory import ImageOperationDirectory
from core.image_operation import ImageOperation
from core.interface_classes import Node, Connection, Port
from core.error_handling import ConnectionError, log

class WorkFlow:
    def __init__(self, logger, image_operation_directiory):
        self.image_operation_directiory = image_operation_directiory

        self.nodes = {}
        self.connections = {}

        self.update_on_change = True # if True, updates whole graph every time theres a change. If False, waits for update call
        
        self.max_id = 0 # highest used ID value for new nodes/connections
        self.starting_node = self.initialise_start_node() # creates a load_image node as graph start point and returns node id

        self.workflow_logger = logger
    
    @property
    def image_operation_directiory(self):
        return self._image_operation_directiory

    @image_operation_directiory.setter
    def image_operation_directiory(self, directory):
        if not isinstance(directory,ImageOperationDirectory):
            raise TypeError (f"expected ImageOperationDirectory class on WorkFlow instantiation, got {type(directory)}")
        self._image_operation_directory = directory

    # creates a load_image node as graph start point
    def initialise_start_node(self):
        return None
    
    """
    add_node(ImageOperation) function adds a key/value pair to nodes dictionary where dictionary key is node.ImageOperation.UniqueID
    """
    def add_node(self, image_operation):

        if not isinstance(image_operation,ImageOperation):
            log(self.workflow_logger,TypeError,f"new node requires ImageOperation class, not {type(image_operation)}","WorkFlow","add_node")

            #raise TypeError(f"new node requires ImageOperation class, not {type(image_operation)}")
        else:
            new_key = ".".join(("node",image_operation.id,str(self.max_id)))
            self.max_id += 1

            if new_key in self.nodes.keys():
                log(self.workflow_logger,ValueError,f"new node key already in nodes dictionary: {new_key}","WorkFlow","add_node")

                #raise TypeError(f"new node key already in nodes dictionary: {new_key}")
            else:
                self.nodes[new_key] = Node(image_operation = image_operation,
                                        node_id = new_key)
            

    """
    delete_node(id) function adds a key/value pair to nodes dictionary where dictionary key is node.ImageOperation.UniqueID
    """
    def delete_node(self, id):

        # checks if passed id is a value nodes key
        
        if id not in self.nodes.keys():
            log(self.workflow_logger,ValueError,f"id not in node list: {id}","WorkFlow","delete_node",id)

        else:

            # removes node from dictionary
            self.nodes.pop(id)

            # checks for connections to/from removed node. Adds to connections_for_deletions list
            connections_for_deletion = []
            for key, value in self.connections.items():
                if value.source_port.node_id == id or value.target_port.node_id == id:
                    connections_for_deletion.append(key)
            # deletes connections
            for connection in connections_for_deletion:
                self.delete_connection(connection)

    """
    add_connection(source_port, target_port) function adds a key/value pair to connections dictionary where dictionary key is connection.UniqueID
    """
    def add_connection(self, source_port, target_port):

        # checks if source_port and target_port are ports
        if not isinstance(source_port,Port):
            log(self.workflow_logger,TypeError,f"expected source_port as Port, not {type(source_port)}","WorkFlow","add_connection")
        elif not isinstance(target_port,Port):
            log(self.workflow_logger, TypeError,f"expected target_port as Port, not {type(target_port)}","WorkFlow","add_connection")

        # checks if source and target Nodes are in nodes dictionary
        elif source_port.node_id not in self.nodes.keys():
            log(self.workflow_logger, ConnectionError,f"source_node not in nodes dictionary: {source_port.node_id}","WorkFlow","add_connection",source_port.node_id)

        elif target_port.node_id not in self.nodes.keys():
            log(self.workflow_logger, ConnectionError,f"target_node not in nodes dictionary: {target_port.node_id}","WorkFlow","add_connection",target_port.node_id)
        else:
            # error checks (see workflow_error_checking.svg)
            self.structure_check(source_port, target_port)
            self.shape_check(source_port, target_port)
            self.type_check(source_port, target_port)

            # create key in the form connection.ID
            new_key = ".".join(("connection",str(self.max_id)))
            self.max_id += 1
            # add new connection to connections dictionary
            self.connections[new_key] = Connection(connection_id = new_key,
                                                source_port = source_port,
                                                target_port = target_port)

    """
    delete_connection(id) function deletes a key/value pair of key "id" from connections dictionary
    """
    def delete_connection(self, id):

        # checks if passed id is a value connections key
        if id not in self.connections.keys():
            log(self.workflow_logger, ValueError, f"id not in node list: {id}", "WorkFlow", "delete_connection", id)
        else:
            # removes node from dictionary
            self.connections.pop(id)

    def structure_check(self, source_port, target_port):
        pass

    def shape_check(self, source_port, target_port):
        pass

    def type_check(self, source_port, target_port):
        pass

"""copied from connection for data conversion etc"""
"""
    @property
    def output_data(self):
        """"""Converts input data on demand.""""""
        
      
        #if self.source_port.output_data is None or \
            #(isinstance(self.source_port.output_data, Parameter) and self.source_port.output_data.value is None) or \
               # (isinstance(self.source_port.output_data, Image) and self.source_port.output_data.pixel_array is None):
           # raise ConnectionError(f"attempt to get output where source_port.output_data has no data present: {self.port_id}")
        output = self.source_port.output_data
        print("\n\noutput\n\n", output)
        # if tranpose is not None and the source data is an image, transpose it
        #if self.transpose and isinstance(output, Image):
         #   output = output.transpose(self.transpose)
        print("\n\noutput\n\n", output)
        # if convert is not None, convert it
        if self.convert:
            output = output.convert(self.convert)
        print("\n\noutput\n\n", output)
        return output

    @output_data.setter
    def output_data(self, value):
        self._output_data = value
    
    """"""Copied from Image Class""""""
    
    #def convert(self, convert):
       # if convert not in DataType.image_types():
       #     raise TypeError(f"images can only be converted to image_types, not {convert}")
       # return Image(data = self.data.to(convert), image_metadata = self.image_metadata)

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
       # return Image(data = current_dtype(transposed_array),
           ##          image_metadata = ImageMetadata(dtype = self.image_metadata.dtype,
            #                                        image_shape_constraints = self.image_metadata.image_shape_constraints,
             #                                       image_map = new_shape))

             """