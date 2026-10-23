from core.image_operation_directory import ImageOperationDirectory
from core.image_operation import ImageOperation
from core.interface_classes import Node, Connection, Port
from core.error_handling import ConnectionError, log, warn, GraphError
from core.shape import Shape
from core.constants import DataPolicy
import core.io_image_operations
import numpy as np
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
            log(self.workflow_logger,TypeError,f"add_node requires ImageOperation class, not {type(image_operation)}","WorkFlow","add_node")

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
    edit_node(id) - partial placeholder function. If a node is edited after creation, particularly by parameter changes via the UI, all downstream nodes need to 
    have needs_update flag set to true
    """
    def edit_node(self, input):
        # checks for string or Node input
        if not isinstance(input, (str,Node)):
            raise TypeError(f"edit_node requires input of Node class, or nodes dictionary key, not: {type(input)}")
        if isinstance(input, str):
            # if string is a key in self.nodes, get Node, else raise ValueError
            if input in self.nodes.keys():
                input = self.nodes[input]
            else: 
                raise ValueError(f"for string inputs, edit_node expects a node dictionary key: {input}")
        # if id is not of Node class, raise TypeError           
        if input not in self.nodes.values():
            raise ValueError(f"for node inputs, edit_node expects value from nodes dictionary")

        # set needs_update to True
        setattr(input, "needs_update", True)

        # get list of all donstream nodes
        downstream_list = self.get_downstream_nodes(input)

        # set needs_update flag for all downstream nodes to True
        for node in downstream_list:
            setattr(self.nodes[node], "needs_update", True)

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
            # structure checks - are their loops? is an input pointed at an output? is there more than one input?
            try:
                self.structure_check(source_port, target_port)
            except Exception as e:
                log(self.workflow_logger, ConnectionError, f"connection not created (failed at structure checks):{e}","WorkFlow","add_connection",".".join((source_port.port_id,target_port.port_id)))
                return

            # type checks - does source metadata give a dtype compatible with target metadata?
            try:
                conversion = self.type_check(source_port, target_port)
            except Exception as e:
                log(self.workflow_logger, ConnectionError, f"connection not created (failed at type checks):{e}","WorkFlow","add_connection",".".join((source_port.port_id,target_port.port_id)))
                return

            transpose = None
            # shape checks - does source metadat give a suitable shape for target metadata?
            try:
                transpose = self.shape_check(source_port, target_port)
            except Exception as e:
                log(self.workflow_logger, ConnectionError, f"connection not created (failed at shape checks):{e}","WorkFlow","add_connection",".".join((source_port.port_id,target_port.port_id)))
                return

            # if error checking is passed, create connection

            # create key in the form connection.ID
            new_key = ".".join(("connection",str(self.max_id)))
            self.max_id += 1
            # add new connection to connections dictionary
            self.connections[new_key] = Connection(connection_id = new_key,
                                                source_port = source_port,
                                                target_port = target_port,
                                                convert = conversion,
                                                transpose = transpose)

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
    """
    Checks for add_connection.
        - structure_check checks how the connection interacts with the shape of the graph
        - type_check checks that data passed will be of compatible types
        - shape_check checks that images passed will be of compatible shapes
    """

    def structure_check(self, source_port, target_port):
        # recursive function to look for loops between nodes in graph
        def loop_check(node_to_search, node_to_find, visited_nodes):
            if node_to_search not in visited_nodes:
                visited_nodes.add(node_to_search)
                target_list = self.get_next_nodes(self.nodes[node_to_search])
                if node_to_find in target_list:
                    raise ConnectionError(f"invalid connection: connection results in a loop")
                else:
                    for node in target_list:
                        loop_check(node, node_to_find, visited_nodes)

        # is source_port and target_port the same port?
        if source_port == target_port:
            raise ConnectionError(f"invalid connection: source port is target port: '{source_port.port_id}'")
        # is source_port an output and target_port an input?
        if source_port.is_input == True:
            raise ConnectionError(f"invalid connection: source port is an input, expected output: '{source_port.port_id}'")
        if target_port.is_input == False:
            raise ConnectionError(f"invalid connection: target port is an output, expected input: '{target_port.port_id}'")
        # are there any other connections in self.connections with target_port as target_port?
        for key, connection in self.connections.items():
            if connection.target_port == target_port:
                raise ConnectionError(f"invalid connection: target port already has an input connection: '{target_port.port_id}'")
        # will this result in a loop?
        loop_check(target_port.node_id, source_port.node_id, set([source_port.node_id]))

    def shape_check(self, source_port, target_port):
        # if all dimensions in target_port.metadata.image_shape_constraints == -1:
        #   - continue
        # if any dimension in target_port.metadata.image_shape_constraints != -1:
        #   - if that dimension in source_port.image_shape_constraints is not -1 and 
        #       does NOT match the target port shape constraints metadat for that dimension:
        #       - raise error
        # if target_port.metadata.image_map matches source_port.metadata.image_map:
        #   - return None
        # else:
        #   - return target_port.metadata.image_map
        # NOTE - SOME ASPECTS OF SHAPE CHECKING TAKE PLACE WHEN THE WORKFLOW IS RUN - WHERE SHAPE CONSTRAINTS ARE -1 (UNDEFINED)
        # ITS IMPOSSIBLE TO SAY IF THE SOURCE DATA MATCHES THE TARGET METADATA UNTIL THE GRAPH IS RUN
        if source_port.metadata.dtype.is_image is True:
            for dimension in Shape.dimensions:
                if target_port.metadata.image_shape_constraints[dimension] != -1:
                    if target_port.metadata.image_shape_constraints[dimension] != -1 and \
                        target_port.metadata.image_shape_constraints[dimension] != source_port.metadata.image_shape_constraints[dimension]:
                        raise ConnectionError(f"invalid image shapes: target port '{target_port.port_id}' requires {dimension}={target_port.metadata.image_shape_constraints[dimension]}, for source_port '{source_port.port_id}', {dimension}={source_port.metadata.image_shape_constraints[dimension]}")
            if str(source_port.metadata.image_map) == str(target_port.metadata.image_map):
                return None
            else:
                return target_port.metadata.image_map

    def type_check(self, source_port, target_port):
        # if target_port.metadata.dtype has same dtype as source_port metadata: 
        #   - return None
        # if target_port.metadata.dtype is in list source_port.dtyle.permitted_conversions:
        #   - return target_port.metadata.dtype
        # if target_port.metadata.dtype is in list source_port.dtype.warned_conversions:
        #   - warn about conversion
        #   - log conversion
        #   - return target_port.metadata.dtype
        # else:
        #   - raise ConnectionError
        if target_port.metadata.dtype == source_port.metadata.dtype:
            return None
        elif hasattr(source_port.metadata.dtype, "permitted_conversions") and \
            source_port.metadata.dtype.permitted_conversions is not None and \
            target_port.metadata.dtype in source_port.metadata.dtype.permitted_conversions:
                return target_port.metadata.dtype
        elif hasattr(source_port.metadata.dtype, "warned_conversions") and \
                source_port.metadata.dtype.warned_conversions is not None and \
                target_port.metadata.dtype in source_port.metadata.dtype.warned_conversions:
                    log(self.workflow_logger, None, f"warning: for connection between '{source_port.port_id}' and '{target_port.port_id}', data of type {source_port.metadata.dtype} converted to {target_port.metadata.dtype}", "WorkFlow", "type_check",".".join((source_port.port_id, target_port.port_id)))
                    warn(f"warning: for connection between '{source_port.port_id}' and '{target_port.port_id}', data of type {source_port.metadata.dtype} converted to {target_port.metadata.dtype}")
                    return target_port.metadata.dtype
        else:
            raise ConnectionError(f"invalid port data types (source {source_port.metadata.dtype} not compatible with target {target_port.metadata.dtype}); connection not possible between '{source_port.port_id}' and '{target_port.port_id}'")

    """
    Graph functions:
        - get_next_nodes gets the IDs of node(s) immediately following a Port, Node or Connection
        - get_previous_nodes gets the ID of node(s) immediately before a given Port, Node or Connection
        - get_downstream_nodes gets ALL the nodes downstream of a given node
        - get_graph_map generates a list of order nodes should be run"""


    # gets node(s) that receive output from given Node/Port/Connection
    # expects input as Node, Connection or Port class, or string as self.nodes/self.connections dictionary key  
    # gives an output as a list of self.nodes dictionary keys (strings, node_id of given Nodes)
    def get_next_nodes(self, input):

        # checks for string or Node input
        if not isinstance(input, (str, Node, Port, Connection)):
            raise TypeError(f"get_next_nodes requires input of Node, Port or Connection class, or nodes or connections dictionary key, not: {type(input)}")
        if isinstance(input, str):
            # if string is a key in self.nodes, get Node, else raise ValueError
            if input in self.nodes.keys():
                input = self.nodes[input]
            elif input in self.connections.keys():
                input = self.connections[input]
            else: 
                raise ValueError(f"for string inputs, get_next_nodes expects a nodes or connections dictionary key: {input}")
        # if input is not of Node class, raise TypeError           
        if isinstance (input, Node) and input not in self.nodes.values():
            raise ValueError(f"for Node inputs, get_next_nodes expects value from nodes dictionary")
        if isinstance (input, Connection) and input not in self.connections.values():
            raise ValueError(f"for Connection inputs, get_next_nodes expects value from nodes dictionary")
        if isinstance (input, Port) and input.node_id not in self.nodes.keys():
            raise ValueError(f"for Port inputs, get_next_nodes expects Port to me part of Node from nodes dictionary")
              
        # gets list of IDs of downstream node(s) immediately after given Port, Node or Connection 
        next_node = []
        # if input is a Port
        if isinstance(input, Port):
            # check its an output Port
            if input.is_input is True:
                raise ValueError(f"get_next_nodes requires output port, not input port: '{input.port_id}'")
            # go through all connections, find connections with input as source_port and append target_port node ids
            for connection in self.connections.values():
                if connection.source_port == input:
                    next_node.append(connection.target_port.node_id)

        # if input is a Node
        elif isinstance(input, Node):
            # goes through each output Port in the Node and calls get_next_nodes with that Port as input
            for port in input.output_ports.values():
                next_node += self.get_next_nodes(port)

        # if input is a Connection, just gets node_id from target_port
        elif isinstance(input, Connection):
            next_node.append(input.target_port.node_id)

        # otherwise, raises error.
        else:
            raise TypeError(f"get_next_nodes requires input of Port, Node or Connection class, or nodes/connections dictionary key, not: {type(input)}")

        # returns list of Node ids
        return next_node

    # gets node(s) that act as inputs to given Node/Port/Connection
    # expects input as Node, Connection or Port class, or string as self.nodes/self.connections dictionary key  
    # gives an output as a list of self.nodes dictionary keys (strings, node_id of given Nodes)
    def get_previous_nodes(self, input): 
        # checks for string or Node input
        if not isinstance(input, (str, Node, Port, Connection)):
            raise TypeError(f"get_previous_nodes requires input of Node, Port or Connection class, or nodes or connections dictionary key, not: {type(input)}")
        if isinstance(input, str):
            # if string is a key in self.nodes, get Node, else raise ValueError
            if input in self.nodes.keys():
                input = self.nodes[input]
            elif input in self.connections.keys():
                input = self.connections[input]
            else: 
                raise ValueError(f"for string inputs, get_previous_nodes expects a nodes or connections dictionary key: {input}")
        # if input is not of Node class, raise TypeError           
        if isinstance (input, Node) and input not in self.nodes.values():
            raise ValueError(f"for Node inputs, get_previous_nodes expects value from nodes dictionary")
        if isinstance (input, Connection) and input not in self.connections.values():
            raise ValueError(f"for Connection inputs, get_previous_nodes expects value from nodes dictionary")
        if isinstance (input, Port) and input.node_id not in self.nodes.keys():
            raise ValueError(f"for Port inputs, get_previous_nodes expects Port to me part of Node from nodes dictionary")
        # gets list of previous nodes from either a Port or a Node 
        previous_node = []
        # if input is a Port
        if isinstance(input, Port):
            # check its an input Port
            if input.is_input is False:
                raise ValueError(f"get_previous_nodes requires input port, not output port: {input.port_id}")
            # go through all connections, find connections with input as target_port and append source_port node ids
            for connection in self.connections.values():
                if connection.target_port == input:
                    previous_node.append(connection.source_port.node_id)
        # if input is a Node
        elif isinstance(input, Node):
            # goes through each output Port in the Node and calls get_previous_nodes with that Port as input
            for port in input.input_ports.values():
                previous_node += self.get_previous_nodes(port)
        # if input is a Connection, just gets node_id from source_port
        elif isinstance(input, Connection):
            previous_node.append(input.source_port.node_id)
        # otherwise, raises error.
        else:
            raise TypeError(f"get_previous_nodes requires input of Port, Node or Connection class, or nodes/connections dictionary key, not: {type(input)}")
        # returns list of Node ids
        return previous_node

    def get_downstream_nodes(self, input):
        # checks for string or Node input
        if not isinstance(input, (str,Node)):
            raise TypeError(f"get_downstream_nodes requires input of Node class, or nodes dictionary key, not: {type(input)}")
        if isinstance(input, str):
            # if string is a key in self.nodes, get Node, else raise ValueError
            if input in self.nodes.keys():
                input = self.nodes[input]
            else: 
                raise ValueError(f"for string inputs, get_downstream_nodes expects a node dictionary key: {input}")
        # if input is not in nodes dictionary, raise ValueError         
        if input not in self.nodes.values():
            raise ValueError(f"for node inputs, get_downstream_nodes expects value from nodes dictionary")
        # gets list of IDs of all nodes downstream from given node
        downstream_nodes = set()
        next_nodes = self.get_next_nodes(input)
        downstream_nodes.update(next_nodes)
        for node in next_nodes:
            downstream_nodes.update(self.get_downstream_nodes(self.nodes[node]))
        return downstream_nodes

    def get_graph_map(self, start_node):
        # for a start_node as either a node_id in nodes dictionary or Node class, gets graph_map as orderd list of node_ids to run
        def check_nodes(node, node_list):
            previous_nodes = self.get_previous_nodes(self.nodes[node])
            for previous_node in previous_nodes:
                if previous_node not in node_list:
                    check_nodes(previous_node, node_list)
            if node not in node_list: node_list.append(node)
            next_nodes = self.get_next_nodes(self.nodes[node])
            for next_node in next_nodes:
                if next_node not in node_list:
                    check_nodes(next_node, node_list)
        # will accept nodes dictionary key (string) or value (Node)
        if not isinstance(start_node, (str,Node)):
            raise TypeError(f"get_graph_map requires input of Node class, or nodes dictionary key, not: {type(start_node)}")
        if isinstance(start_node, Node):
            if start_node in self.nodes.values():
                start_node = start_node.node_id
            else:
                raise ValueError(f"for node inputs, get_graph_map expects value from nodes dictionary")
        if start_node not in self.nodes.keys():
            raise ValueError(f"for string inputs, get_graph_map expects a node dictionary key")

        running_list = [start_node]
        next_nodes = self.get_next_nodes(start_node)
        for node in next_nodes:
            check_nodes(node, running_list)
        return running_list

    def update_graph(self, test = False):

        #TODO#######################################################
        # Did I ever add checks of image/array shape data when passing data through the graph?


        """1. Generate ordered node list"""
        # get list of start nodes by comparing nodes dictionary value to start_nodes list from io_image_operations.py
        start_node_id_list = [node.node_id for node in self.nodes.values() if node.image_operation.id in core.io_image_operations.start_nodes]
        if test: log(self.workflow_logger, None, f"nodes added to start node list","WorkFlow","update_graph",start_node_id_list)
        print("\nstart node list:",start_node_id_list)
        # if no start nodes, log error
        if len(start_node_id_list) == 0:
            log(self.workflow_logger, GraphError, f"cannot update graph without defined start nodes","WorkFlow","update_graph") 

        # get node_list from graph map from each start_node
        node_list = []
        for start_node_id in start_node_id_list:
            try:
                for item in self.get_graph_map(start_node_id):
                    if item not in node_list: node_list.append(item)
            except Exception as e:
                log(self.workflow_logger, GraphError, f"error generating graph map for start node {start_node_id}: {e}","WorkFlow","update_graph") 
        """2. Iterate through node list, update is_ready flags, transfer input data, run nodes"""
        """input data to Node is transferred in but output data is not transferred out: for upstream nodes to exist, connection must exist. No guarantee dowsntream connection exists"""

        for node_id in node_list:
            active_node = self.nodes[node_id]
            port_connections_dict = {}
            print("\n checking node:",node_id)

            # 2.1: check that all input Ports are either UI Ports or have connections. If not, not ready
            # generate port_connections_dict of all input_ports of active_node
            # if it requires user data, in format {Port class: "user_input"}
            # it it requires a connection and one is present, in format {Port class: Connection class}
            # if it requires a connection but none is present, in format {Port class: None}
            for port in active_node.input_ports.values():
                if hasattr(port.metadata, "user_input") and port.metadata.user_input is True:
                    port_connections_dict[port] = "user_input"
                else:
                    port_connections_dict[port] = next(
                        (connection for connection in self.connections.values() if connection.target_port == port), None)

            # if any ports are missing a connection, continue to next Node
            if None in port_connections_dict.values():
                if test is True: log(self.workflow_logger, None, f"node '{node_id}' not activated, missing connections","WorkFlow","update_graph",node_id)
                print("\nports missing connections")
                continue
            
            # 2.2: check that all previous nodes are ready
            try:
                previous_node_ids = self.get_previous_nodes(node_id)
            except Exception as e:
                log(self.workflow_logger, GraphError, f"error generating list of previous nodes for node {node_id}: {e}","WorkFlow","update_graph")

            ready_state = all([self.nodes[node_id].is_ready for node_id in previous_node_ids])
            for node_id in previous_node_ids:
                print(f"\n{node_id} is_ready: {self.nodes[node_id].is_ready}")

            if ready_state is not True:
                if test is True: log(self.workflow_logger, None, f"node '{node_id}' not activated, previous nodes not ready","WorkFlow","update_graph",node_id)
                continue

            # 2.3: set node is_ready to True
            # TODO: CONSIDER TESTING INPUT VALUES PRIOR TO SETTING IS_READY
            active_node.is_ready = True

            # 2.4: check node needs_update is True
            if active_node.needs_update is True:
                # 2.5: copy data from previous nodes
                try:
                    for input_port, connection in port_connections_dict.items():
                        # if user input, skip data transfer through graph
                        if connection == "user_input": 
                            continue

                        incoming_data = connection.source_port.data
                        # tranpose data if transposition required
                        if connection.transpose is not None:
                            try:
                                incoming_data = transpose(value = incoming_data,
                                                current_shape=connection.source_port.metadata.image_map,
                                                new_shape = connection.transpose)
                            except Exception as e:
                                raise GraphError(f"error transposing data for port '{input_port.port_id}': {e}")

                        
                        # convert data if conversion required
                        if connection.convert is not None:
                            try:
                                incoming_data = connection.source_port.metadata.dtype.to(value=incoming_data,
                                                                            dtype=connection.convert)
                            except Exception as e:
                                raise GraphError(f"error converting data for port '{input_port.port_id}': {e}")
                            
                        # copy data to input_port
                        try:
                            input_port.data = incoming_data
                        except Exception as e:
                            raise GraphError(f"error copying data for port '{input_port.port_id}': {e}")
                           
                except Exception as e:
                    log(self.workflow_logger, GraphError, f"error transferring data data for node '{node_id}': {e}","WorkFlow","update_graph")
                    continue

                # 2.6: activate node
                try:
                    active_node.activate_node()
                except Exception as e:
                    log(self.workflow_logger, GraphError, f"error activating node '{node_id}': {e}","WorkFlow","update_graph")
                    continue
                
                active_node.needs_update = False
                if test is True: log(self.workflow_logger, None, f"node activated sucessfully","WorkFlow","update_graph",node_id)
        
                
def transpose( value, current_shape, new_shape):    
    # check value is a np.ndarray
    if not isinstance(value, np.ndarray):
        raise TypeError(f"expected value as np.array, got {type(value)}")
    
    # check new_shape is Shape class with dimension values between 0 and max_image_dimensions
    if not isinstance(new_shape, Shape):
        raise TypeError (f"expected new_shape as Shape class, got {type(new_shape)}")
    for item in new_shape:
        if item < 0 or item > Shape.max_image_dimensions:
            raise ValueError (f"new_shape shape dimensions out of range, must be 0-{Shape.max_image_dimensions}")
        
    # check current_shape is Shape class with dimension values between 0 and max_image_dimensions
    if not isinstance(current_shape, Shape):
        raise TypeError (f"expected current_shape as Shape class, got {type(current_shape)}")
    for item in current_shape:
        if item < 0 or item > Shape.max_image_dimensions:
            raise ValueError (f"current_shape shape dimensions out of range, must be 0-{Shape.max_image_dimensions}")
        
    # new_shape is Shape class with new dimensions indices of each array (c,z,y,x)
    # needs to create transpose list with values new_c, new_z, new_y, new_x in order of old_c, old_z, old_y, old_x
    transpose = [current_shape[item] for item in new_shape]       
    transposed_array = np.transpose(value, transpose)

    return transposed_array
    

