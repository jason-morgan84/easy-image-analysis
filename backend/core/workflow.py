from core.image_operation_directory import ImageOperationDirectory
from core.image_operation import ImageOperation
from core.interface_classes import Node

class WorkFlow:
    def __init__(self, image_operation_directiory):
        self.image_operation_directiory = image_operation_directiory

        self.nodes = {}
        self.connections = {}

        update_on_change = True # if True, updates whole graph every time theres a change. If False, waits for update call
        max_id = 0 # highest used ID value for new nodes/connections

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
    """* Create add_node(ImageOperation, key) function
    - this adds a key/value pair to nodes dictionary
    - dictionary key is node.ImageOperation.UniqueID
    - gets uniqueID and checks the key isn't already in dictionary
    - value is Node(ImageOperation)"""

    def add_node(self, image_operation):

        if not isinstance(image_operation,ImageOperation):
            raise TypeError(f"new node requires ImageOperation class, not {type(image_operation)}")

        new_key = ".".join("node",image_operation.name,str(self.max_id))
        max_id += 1

        if new_key in self.nodes.keys():
            raise TypeError(f"new node key already in nodes dictionary: {new_key}")

        self.nodes[new_key] = Node(image_operation = image_operation,
                                   node_id = new_key)
        

    