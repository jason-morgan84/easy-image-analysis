from core.image_operation_directory import ImageOperationDirectory
from core.image_operation import ImageOperation
from core.interface_classes import Node, Connection
from core.error_handling import ConnectionError

class WorkFlow:
    def __init__(self, image_operation_directiory):
        self.image_operation_directiory = image_operation_directiory

        self.nodes = {}
        self.connections = {}

        update_on_change = True # if True, updates whole graph every time theres a change. If False, waits for update call
        
        self.max_id = 0 # highest used ID value for new nodes/connections
        self.starting_node = self.initialise_start_node() # creates a load_image node as graph start point and returns node id

    
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
            raise TypeError(f"new node requires ImageOperation class, not {type(image_operation)}")
        new_key = ".".join(("node",image_operation.id,str(self.max_id)))
        self.max_id += 1

        if new_key in self.nodes.keys():
            raise TypeError(f"new node key already in nodes dictionary: {new_key}")

        self.nodes[new_key] = Node(image_operation = image_operation,
                                   node_id = new_key)
        

    """
    delete_node(id) function adds a key/value pair to nodes dictionary where dictionary key is node.ImageOperation.UniqueID
    """
    def delete_node(self, id):

        # checks if passed id is a value nodes key
        if id not in self.nodes.keys():
            raise ValueError(f"id not in node list: {id}")

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
        # checks if source and target Nodes are in nodes dictionary
        if source_port.node_id not in self.nodes.keys():
            raise ConnectionError(f"source_node not in nodes dictionary: {source_port.node_id}")
        if target_port.node_id not in self.nodes.keys():
            raise ConnectionError(f"target_node not in nodes dictionary: {target_port.node_id}")

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
            raise ValueError(f"id not in node list: {id}")

        # removes node from dictionary
        self.connections.pop(id)

    def structure_check(self, source_port, target_port):
        pass

    def shape_check(self, source_port, target_port):
        pass

    def type_check(self, source_port, target_port):
        pass