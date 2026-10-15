import pytest
from core.workflow import WorkFlow
from core.image_operation_directory import ImageOperationDirectory
from core.image_operation import ImageOperation
from core.constants import DataType
from core.interface_classes import Connection, Port
import copy
# provide image_operation_directory arguement which is not ImageOperationDirectory class
def test_initialise_not_image_operation_directory():
    a = "test"
    with pytest.raises(TypeError, match = "expected ImageOperationDirectory class on WorkFlow instantiation"):
        workflow = WorkFlow(logger = [], image_operation_directiory = a)

# call add_node(image_operation) function where image_operation is not ImageOperation class
def test_add_node_not_image_operation():
    log = []
    directory = ImageOperationDirectory(logger = log, testing = True)
    workflow = WorkFlow(logger = log, image_operation_directiory = directory)

    workflow.add_node("test")

    for item in log:
        if item.class_name == "WorkFlow" and item.function_name == "add_node":
            assert "new node requires ImageOperation class" in item.message 


# call add_node(image_operation) function where dictionary key already exists
def test_add_node_existing_key():
    log = []
    directory = ImageOperationDirectory(logger = log, testing = True)
    directory.import_operations_dict()
    workflow = WorkFlow(logger = log, image_operation_directiory = directory)
    workflow.add_node(directory["same_image"])
    workflow.max_id -= 1
    workflow.add_node(directory["same_image"])

    for item in log:
        if item.class_name == "WorkFlow" and item.function_name == "add_node":
            assert "new node key already in nodes dictionary" in item.message 

# check add_node adds a node
def test_add_node_adds_node():
    log = []
    directory = ImageOperationDirectory(logger = log, testing = True)
    directory.import_operations_dict()
    workflow = WorkFlow(logger = log, image_operation_directiory = directory)
    workflow.add_node(directory["same_image"])
    assert len(workflow.nodes) == 1
    assert workflow.nodes["node.same_image.0"]

# check adding two nodes gives unique dictionary keys
def test_add_node_has_unique_key():
    log = []
    directory = ImageOperationDirectory(logger = log, testing = True)
    directory.import_operations_dict()
    workflow = WorkFlow(logger = log, image_operation_directiory = directory)
    workflow.add_node(directory["same_image"])
    workflow.add_node(directory["same_image"])
    assert len(workflow.nodes) == 2
    assert workflow.nodes["node.same_image.0"]
    assert workflow.nodes["node.same_image.1"]

# call delete_node with an invalid key
def test_delete_node_invalid_key():
    log = []
    directory = ImageOperationDirectory(logger = log, testing = True)
    directory.import_operations_dict()
    workflow = WorkFlow(logger = log, image_operation_directiory = directory)
    workflow.add_node(directory["same_image"])
    workflow.delete_node("test")

    for item in log:
        if item.class_name == "WorkFlow" and item.function_name == "delete_node":
            assert item.identifier == "test"
            assert "id not in node list" in item.message 

# call delete_node
def test_delete_node_removes_node():
    log = []
    directory = ImageOperationDirectory(logger = log, testing = True)
    directory.import_operations_dict()
    workflow = WorkFlow(logger = log, image_operation_directiory = directory)
    workflow.add_node(directory["same_image"])
    workflow.delete_node("node.same_image.0")
    assert "node.same_image.0" not in workflow.nodes.keys()


# check delete_node removes associated connections
def test_node_delete_removes_connections():
    log = []
    directory = ImageOperationDirectory(logger = log, testing = True)
    directory.import_operations_dict()
    workflow = WorkFlow(logger = log, image_operation_directiory = directory)

    workflow.add_node(directory["same_image"])
    workflow.add_node(directory["same_image"])
    workflow.add_connection(source_port = workflow.nodes["node.same_image.0"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image.1"].input_ports["image.input"])
    workflow.delete_node("node.same_image.1")
    assert "connection.2" not in workflow.connections.keys()

# call add_connection where source is not a port
def test_connection_source_not_port():
    log = []
    directory = ImageOperationDirectory(logger = log, testing = True)
    directory.import_operations_dict()
    workflow = WorkFlow(logger = log, image_operation_directiory = directory)
    workflow.add_node(directory["same_image"])
    workflow.add_node(directory["same_image"])
    
    workflow.add_connection(source_port = workflow.nodes["node.same_image.0"],
                            target_port = workflow.nodes["node.same_image.1"].input_ports["image.input"])

    for item in log:
        if item.class_name == "WorkFlow" and item.function_name == "add_connection":
            assert "expected source_port as Port" in item.message 
# call add_connection where target is not a port
def test_connection_target_not_port():
    log = []
    directory = ImageOperationDirectory(logger = log, testing = True)
    directory.import_operations_dict()
    workflow = WorkFlow(logger = log, image_operation_directiory = directory)
    workflow.add_node(directory["same_image"])
    workflow.add_node(directory["same_image"])
    
    workflow.add_connection(source_port = workflow.nodes["node.same_image.0"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image.1"])

    for item in log:
        print ("\n",item.message,"\n")
        if item.class_name == "WorkFlow" and item.function_name == "add_connection":
            assert "expected target_port as Port" in item.message 


# call add_connection where a connection would fail type checks(invalid type (eg 8 bit image to binarised input))
def test_connection_add_invalid_types():
    log = []
    directory = ImageOperationDirectory(logger = log, testing = True)
    directory.import_operations_dict()
    workflow = WorkFlow(logger = log, image_operation_directiory = directory)

    workflow.add_node(directory["same_image"])
    workflow.add_node(directory["binarised_input"])
    workflow.add_connection(source_port = workflow.nodes["node.same_image.0"].output_ports["image.output"],
                            target_port = workflow.nodes["node.binarised_input.1"].input_ports["image.input"])
    for item in log:
        if item.class_name == "WorkFlow" and item.function_name == "add_connection":
            assert item.identifier == "image.output.image.input"
            assert "connection not created (failed at type checks):invalid port data types" in item.message 

# call add_connection where a connection fails type checks but can be converted with warning (eg binarised to 8 bit int)
def test_connection_add_conversion_with_warning():
    log = []
    directory = ImageOperationDirectory(logger = log, testing = True)
    directory.import_operations_dict()
    workflow = WorkFlow(logger = log, image_operation_directiory = directory)
    workflow.add_node(directory["binarised_output"])
    workflow.add_node(directory["same_image"])
    workflow.add_connection(source_port = workflow.nodes["node.binarised_output.0"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image.1"].input_ports["image.input"])
    
    assert "connection.2" in workflow.connections.keys()
    assert workflow.connections["connection.2"].convert == DataType.ImageInt
    for item in log:
        if item.class_name == "WorkFlow" and item.function_name == "add_connection":
            assert item.identifier == "image.output.image.input"
            assert "warning: for connection between 'image.output' and 'image.input'" in item.message 

# call add_connection where a connection fails type checks but can be converted (eg 8 bit int to float input)
def test_connection_add_with_conversion():
    log = []
    directory = ImageOperationDirectory(logger = log, testing = True)
    directory.import_operations_dict()

    log += directory.logger

    workflow = WorkFlow(logger = log, image_operation_directiory = directory)
    workflow.add_node(directory["same_image"])
    workflow.add_node(directory["float_input"])
    workflow.add_connection(source_port = workflow.nodes["node.same_image.0"].output_ports["image.output"],
                            target_port = workflow.nodes["node.float_input.1"].input_ports["image.input"])
    
    assert "connection.2" in workflow.connections.keys()
    assert workflow.connections["connection.2"].convert == DataType.ImageFloat

# call add_connection where a connection would fail shape checks(invalid shape (eg needs flattened image but has z != 1))
def test_connection_wrong_shape():
    log = []
    directory = ImageOperationDirectory(logger = log, testing = True)
    directory.import_operations_dict()
    workflow = WorkFlow(logger = log, image_operation_directiory = directory)
    workflow.add_node(directory["multi_channel_output"])
    workflow.add_node(directory["single_channel_input"])
    workflow.add_connection(source_port = workflow.nodes["node.multi_channel_output.0"].output_ports["image.output"],
                            target_port = workflow.nodes["node.single_channel_input.1"].input_ports["image.input"])

    for item in log:
        if item.class_name == "WorkFlow" and item.function_name == "add_connection":
            assert item.identifier == "image.output.image.input"
            assert "connection not created (failed at shape checks):invalid image shapes: target port 'image.input' requires c=1, for source_port 'image.output', c=4" in item.message 

# call add_connection where a connection would pass shape checks but require transposition
def test_connection_add_with_transposition():
    log = []
    directory = ImageOperationDirectory(logger = log, testing = True)
    directory.import_operations_dict()

    log += directory.logger
    workflow = WorkFlow(logger = log, image_operation_directiory = directory)
    workflow.add_node(directory["same_image"])
    workflow.add_node(directory["same_image_reversed_input_image_map"])
    workflow.add_connection(source_port = workflow.nodes["node.same_image.0"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image_reversed_input_image_map.1"].input_ports["image.input"])
    
    assert "connection.2" in workflow.connections.keys()
    assert str(workflow.connections["connection.2"].transpose) == "(3, 2, 1, 0)"

# call add_connection where a connection would fail structure checks (connecting port to itself)
def test_structure_check_add_connection_same_node():
    log = []
    directory = ImageOperationDirectory(logger = log, testing = True)
    directory.import_operations_dict()
    workflow = WorkFlow(logger = log, image_operation_directiory = directory)



    workflow.add_node(directory["same_image"])
    workflow.add_node(directory["same_image"])
    workflow.add_connection(source_port = workflow.nodes["node.same_image.0"].input_ports["image.input"],
                                target_port = workflow.nodes["node.same_image.0"].input_ports["image.input"])
    for item in log:
        print(item.message)
        if item.class_name == "WorkFlow" and item.function_name == "add_connection":
            assert "connection not created (failed at structure checks):invalid connection: source port is target port" in item.message

# call add_connection where a connection would fail structure checks (connecting input to input/output to output)
def test_structure_check_add_connection_source_input():
    log = []
    directory = ImageOperationDirectory(logger = log, testing = True)
    directory.import_operations_dict()
    workflow = WorkFlow(logger = log, image_operation_directiory = directory)

    workflow.add_node(directory["same_image"])
    workflow.add_node(directory["same_image"])
    workflow.add_connection(source_port = workflow.nodes["node.same_image.0"].input_ports["image.input"],
                            target_port = workflow.nodes["node.same_image.0"].output_ports["image.output"])
    for item in log:
        print(item.message)
        if item.class_name == "WorkFlow" and item.function_name == "add_connection":
            assert "connection not created (failed at structure checks):invalid connection: source port is an input" in item.message

# call add_connection where a connection would fail structure checks(connecting to input which already has connections - NB - inputs allow 1 connection, outputs allow many connections)
def test_structure_check_add_connection_already_present():
    log = []
    directory = ImageOperationDirectory(logger = log, testing = True)
    directory.import_operations_dict()
    workflow = WorkFlow(logger = log, image_operation_directiory = directory)

    workflow.add_node(directory["same_image"])
    workflow.add_node(directory["same_image"])
    workflow.add_node(directory["same_image"])
    workflow.add_connection(source_port = workflow.nodes["node.same_image.0"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image.1"].input_ports["image.input"])
    
    workflow.add_connection(source_port = workflow.nodes["node.same_image.0"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image.1"].input_ports["image.input"])
    for item in log:
        print(item.message)
        if item.class_name == "WorkFlow" and item.function_name == "add_connection":
            assert "invalid connection: target port already has an input connection" in item.message

    workflow.add_connection(source_port = workflow.nodes["node.same_image.0"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image.2"].input_ports["image.input"])

    assert "connection.3" in workflow.connections.keys()

# call add_connection where a connection would fail structure checks(would result in loop)
def test_structure_check_add_connection_loop():
    log = []
    directory = ImageOperationDirectory(logger = log, testing = True)
    directory.import_operations_dict()
    workflow = WorkFlow(logger = log, image_operation_directiory = directory)

    # create the following structure:
    # node0
    #   |
    #   v
    # node1 --> node2
    #   |
    #   V
    # node 3
    # then try to connect node2 output to node1 input

    workflow.add_node(directory["same_image"]) # node0: node.same_image.0
    workflow.add_node(directory["same_image"]) # node1: node.same_image.1
    workflow.add_node(directory["same_image"]) # node2: node.same_image.2
    workflow.add_node(directory["same_image"]) # node3: node.same_image.3

    # connect node0 to node1 and check connection exists
    workflow.add_connection(source_port = workflow.nodes["node.same_image.0"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image.1"].input_ports["image.input"])

    assert len(workflow.connections) == 1
    assert "connection.4" in workflow.connections.keys()

    # connect node1 to node2 and check connection exists
    workflow.add_connection(source_port = workflow.nodes["node.same_image.1"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image.2"].input_ports["image.input"])

    assert len(workflow.connections) == 2
    assert "connection.5" in workflow.connections.keys()

    # connect node1 to node3 and check connection exists
    workflow.add_connection(source_port = workflow.nodes["node.same_image.1"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image.3"].input_ports["image.input"])

    assert len(workflow.connections) == 3
    assert "connection.6" in workflow.connections.keys()

    # attempt to connect node2 to node0 - check connection doesn't exist and correct error in log
    workflow.add_connection(source_port = workflow.nodes["node.same_image.2"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image.0"].input_ports["image.input"])

    assert len(workflow.connections) == 3
    assert "connection.7" not in workflow.connections.keys()

    for item in log:
        print(item.message)
        if item.class_name == "WorkFlow" and item.function_name == "add_connection":
            assert "invalid connection: connection results in a loop" in item.message

# check add_connection creates a connection
def test_connection_add():
    log = []
    directory = ImageOperationDirectory(logger = log, testing = True)
    directory.import_operations_dict()
    workflow = WorkFlow(logger = log, image_operation_directiory = directory)

    workflow.add_node(directory["same_image"])
    workflow.add_node(directory["same_image"])
    workflow.add_connection(source_port = workflow.nodes["node.same_image.0"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image.1"].input_ports["image.input"])
    assert "connection.2" in workflow.connections.keys()

# call delete_connection with an invalid key
def test_connection_delete_invalid_key():
    log = []
    directory = ImageOperationDirectory(logger = log, testing = True)
    directory.import_operations_dict()
    workflow = WorkFlow(logger = log, image_operation_directiory = directory)

    workflow.add_node(directory["same_image"])
    workflow.add_node(directory["same_image"])
    workflow.add_connection(source_port = workflow.nodes["node.same_image.0"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image.1"].input_ports["image.input"])

    for item in log:
        if item.class_name == "WorkFlow" and item.function_name == "delete_connection":
            assert item.identifier == "test"
            assert "id not in node list" in item.message 

# check delete_connection removes a connection
def test_connection_delete():
    log = []
    directory = ImageOperationDirectory(logger = log, testing = True)
    directory.import_operations_dict()
    workflow = WorkFlow(logger = log, image_operation_directiory = directory)

    workflow.add_node(directory["same_image"])
    workflow.add_node(directory["same_image"])
    workflow.add_connection(source_port = workflow.nodes["node.same_image.0"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image.1"].input_ports["image.input"])
    workflow.delete_connection("connection.2")
    
    assert "connection.2" not in workflow.connections.keys()


# test get_next_nodes
def test_get_next_nodes():
    log = []
    directory = ImageOperationDirectory(logger = log, testing = True)
    directory.import_operations_dict()
    workflow = WorkFlow(logger = log, image_operation_directiory = directory)

    # four nodes, node.same_image.0, node.same_image.1, node.same_image.2, node.same_image.3
    workflow.add_node(directory["same_image"])
    workflow.add_node(directory["same_image"])
    workflow.add_node(directory["same_image"])
    workflow.add_node(directory["same_image"])

    # create the following structure:
    # node0
    #   |
    #   v
    # node1 --> node2
    #   |
    #   V
    # node3

    workflow.add_connection(source_port = workflow.nodes["node.same_image.0"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image.1"].input_ports["image.input"])
    workflow.add_connection(source_port = workflow.nodes["node.same_image.1"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image.2"].input_ports["image.input"])
    workflow.add_connection(source_port = workflow.nodes["node.same_image.1"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image.3"].input_ports["image.input"])
    
    # test get_next_nodes from node "node.same_image.0", expect single node returned
    nodes = workflow.get_next_nodes(workflow.nodes["node.same_image.0"])
    assert len(nodes) == 1
    assert "node.same_image.1" in nodes


    # test get_next_nodes from node "node.same_image.1", expect two nodes returned
    nodes = workflow.get_next_nodes(workflow.nodes["node.same_image.1"])
    assert len(nodes) == 2
    assert "node.same_image.2" in nodes
    assert "node.same_image.3" in nodes
    # same test but with node key passed
    nodes = workflow.get_next_nodes("node.same_image.1")
    assert len(nodes) == 2
    assert "node.same_image.2" in nodes
    assert "node.same_image.3" in nodes

    # test get_next_nodes from port "node.same_image.0.output_ports["image.output"]", expect single node returned
    nodes = workflow.get_next_nodes(workflow.nodes["node.same_image.0"].output_ports["image.output"])
    assert len(nodes) == 1
    assert "node.same_image.1" in nodes


    # test get_next_nodes from port "workflow.nodes["node.same_image.1"].output_ports["image.output"]", expect two nodes returned
    nodes = workflow.get_next_nodes(workflow.nodes["node.same_image.1"].output_ports["image.output"])
    assert len(nodes) == 2
    assert "node.same_image.2" in nodes
    assert "node.same_image.3" in nodes

    # test get_next_nodes from connection "workflow.connections["connection.5"]", expect one nodes returned
    nodes = workflow.get_next_nodes(workflow.connections["connection.5"])
    assert len(nodes) == 1
    assert "node.same_image.2" in nodes
    # same test but with connections key passed
    nodes = workflow.get_next_nodes("connection.5")
    assert len(nodes) == 1
    assert "node.same_image.2" in nodes

    # test get_next_nodes from non-string/Node/Connection/Port object expect TypeError
    with pytest.raises(TypeError, match = "get_next_nodes requires input of Node, Port or Connection class, or nodes or connections dictionary key, not"):
        nodes = workflow.get_next_nodes(workflow)

    # test get_next_nodes from string that is not nodes or connections key, expect ValueError
    with pytest.raises(ValueError, match = "for string inputs, get_next_nodes expects a nodes or connections dictionary key"):
        nodes = workflow.get_next_nodes("image.output")

    # test get_next_nodes from Node that is not nodes value, expect ValueError
    test_node = copy.copy(workflow.nodes["node.same_image.0"])
    with pytest.raises(ValueError, match = "for Node inputs, get_next_nodes expects value from nodes dictionary"):
        nodes = workflow.get_next_nodes(test_node)

    # test get_next_nodes from Connection that is not connections value, expect ValueError
    test_node = copy.copy(workflow.connections["connection.4"])
    with pytest.raises(ValueError, match = "for Connection inputs, get_next_nodes expects value from nodes dictionary"):
        nodes = workflow.get_next_nodes(test_node)

    # test get_next_nodes from Port that is not in a nodes Node, expect ValueError
    test_port = copy.copy(workflow.nodes["node.same_image.0"].output_ports["image.output"])
    test_port.node_id = "none"
    with pytest.raises(ValueError, match = "for Port inputs, get_next_nodes expects Port to me part of Node from nodes dictionary"):
        nodes = workflow.get_next_nodes(test_port)

    # test get_next_nodes from input port "workflow.nodes["node.same_image.1"].input_ports["image.input"]"
    with pytest.raises(ValueError, match = "get_next_nodes requires output port, not input port"):
        nodes = workflow.get_next_nodes(workflow.nodes["node.same_image.1"].input_ports["image.input"])


# test get_previous_nodes
def test_get_previous_nodes():
    log = []
    directory = ImageOperationDirectory(logger = log, testing = True)
    directory.import_operations_dict()
    workflow = WorkFlow(logger = log, image_operation_directiory = directory)

    # four nodes, node.same_image.1, node.same_image.2, node.same_image.3
    workflow.add_node(directory["same_image"])              # node0: node.same_image.0
    workflow.add_node(directory["same_image"])              # node1: node.same_image.1
    workflow.add_node(directory["same_image_two_inputs"])   # node2: node.same_image_two_inputs.2
    workflow.add_node(directory["same_image"])              # node3: node.same_image.3

    # create the following structure:
    # node0 ------
    #   |        |
    #   v        V
    # node1 --> node2
    #   |
    #   V
    # node3

    workflow.add_connection(source_port = workflow.nodes["node.same_image.0"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image.1"].input_ports["image.input"])
    workflow.add_connection(source_port = workflow.nodes["node.same_image.0"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image_two_inputs.2"].input_ports["image.input1"])
    workflow.add_connection(source_port = workflow.nodes["node.same_image.1"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image_two_inputs.2"].input_ports["image.input2"])
    workflow.add_connection(source_port = workflow.nodes["node.same_image.1"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image.3"].input_ports["image.input"])
    
    # test get_previous_nodes from node "node3", expect single node returned, node1
    nodes = workflow.get_previous_nodes(workflow.nodes["node.same_image.3"])
    assert len(nodes) == 1
    assert "node.same_image.1" in nodes

    # test get_previous_nodes from node "node2", expect single node returned, node1 and node0
    # test using dictionary key
    nodes = workflow.get_previous_nodes("node.same_image_two_inputs.2")
    assert len(nodes) == 2
    assert "node.same_image.0" in nodes
    assert "node.same_image.1" in nodes
    

    # test get_previous_nodes from port "node.same_image.1.input_ports["image.input"]", expect single node returned
    nodes = workflow.get_previous_nodes(workflow.nodes["node.same_image.1"].input_ports["image.input"])
    assert len(nodes) == 1
    assert "node.same_image.0" in nodes

    # test get_previous_nodes from port "node.same_image.1.input_ports["image.input"]" provided as string, expect ValueError
    with pytest.raises(ValueError, match = "for string inputs, get_previous_nodes expects a nodes or connections dictionary key"):
        nodes = workflow.get_previous_nodes("image.input")

    # test get_previous_nodes from connection "workflow.connections["connection.5"]", expect one node returned
    nodes = workflow.get_previous_nodes(workflow.connections["connection.5"])
    assert len(nodes) == 1
    assert "node.same_image.0" in nodes
    # same test but with connections key passed
    nodes = workflow.get_previous_nodes("connection.5")
    assert len(nodes) == 1
    assert "node.same_image.0" in nodes

    
    # test get_previous_nodes from non-string/Node/Connection/Port object expect TypeError
    with pytest.raises(TypeError, match = "get_previous_nodes requires input of Node, Port or Connection class, or nodes or connections dictionary key, not"):
        nodes = workflow.get_previous_nodes(workflow)

    # test get_previous_nodes from string that is not nodes or connections key, expect ValueError
    with pytest.raises(ValueError, match = "for string inputs, get_previous_nodes expects a nodes or connections dictionary key"):
        nodes = workflow.get_previous_nodes("image.output")

    # test get_previous_nodes from Node that is not nodes value, expect ValueError
    test_node = copy.copy(workflow.nodes["node.same_image.0"])
    with pytest.raises(ValueError, match = "for Node inputs, get_previous_nodes expects value from nodes dictionary"):
        nodes = workflow.get_previous_nodes(test_node)

    # test get_previous_nodes from Connection that is not connections value, expect ValueError
    test_node = copy.copy(workflow.connections["connection.4"])
    with pytest.raises(ValueError, match = "for Connection inputs, get_previous_nodes expects value from nodes dictionary"):
        nodes = workflow.get_previous_nodes(test_node)

    # test get_previous_nodes from Port that is not in a nodes Node, expect ValueError
    test_port = copy.copy(workflow.nodes["node.same_image.0"].output_ports["image.output"])
    test_port.node_id = "none"
    with pytest.raises(ValueError, match = "for Port inputs, get_previous_nodes expects Port to me part of Node from nodes dictionary"):
        nodes = workflow.get_previous_nodes(test_port)

    # test get_previous_nodes from output port "workflow.nodes["node.same_image.1"].output_ports["image.output"]"
    with pytest.raises(ValueError, match = "get_previous_nodes requires input port, not output port"):
        nodes = workflow.get_previous_nodes(workflow.nodes["node.same_image.1"].output_ports["image.output"])

# test get_downstream_nodes
def test_get_downstream_nodes():
    log = []
    directory = ImageOperationDirectory(logger = log, testing = True)
    directory.import_operations_dict()
    workflow = WorkFlow(logger = log, image_operation_directiory = directory)

    # create the following structure:
    # node0
    #   |
    #   v
    # node1 ------> node2
    #   |             |
    #   V             V
    # node3         node4 ------> node5
    #   |             |
    #   V             V
    # node6         node7

    workflow.add_node(directory["same_image"]) # node0: node.same_image.0
    workflow.add_node(directory["same_image"]) # node1: node.same_image.1
    workflow.add_node(directory["same_image"]) # node2: node.same_image.2
    workflow.add_node(directory["same_image"]) # node3: node.same_image.3
    workflow.add_node(directory["same_image"]) # node4: node.same_image.4
    workflow.add_node(directory["same_image"]) # node5: node.same_image.5
    workflow.add_node(directory["same_image"]) # node6: node.same_image.6
    workflow.add_node(directory["same_image"]) # node7: node.same_image.7

    workflow.add_connection(source_port = workflow.nodes["node.same_image.0"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image.1"].input_ports["image.input"])
    
    workflow.add_connection(source_port = workflow.nodes["node.same_image.1"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image.2"].input_ports["image.input"])
    
    workflow.add_connection(source_port = workflow.nodes["node.same_image.1"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image.3"].input_ports["image.input"])
    
    workflow.add_connection(source_port = workflow.nodes["node.same_image.2"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image.4"].input_ports["image.input"])
    
    workflow.add_connection(source_port = workflow.nodes["node.same_image.3"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image.6"].input_ports["image.input"])
    
    workflow.add_connection(source_port = workflow.nodes["node.same_image.4"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image.5"].input_ports["image.input"])

    workflow.add_connection(source_port = workflow.nodes["node.same_image.4"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image.7"].input_ports["image.input"])
    
    # test with invalid input (not string or Node)
    with pytest.raises(TypeError, match = "get_downstream_nodes requires input of Node class, or nodes dictionary key"):
        nodes = workflow.get_downstream_nodes(workflow)

    # test with invalid input (string but not nodes dictionary key)
    with pytest.raises(ValueError, match = "for string inputs, get_downstream_nodes expects a node dictionary key"):
        nodes = workflow.get_downstream_nodes("not_a_node_id")

    # test with invalid input (Node class but not nodes dictionary value) 
    test_node = copy.copy(workflow.nodes["node.same_image.0"])
    with pytest.raises(ValueError, match = "for node inputs, get_downstream_nodes expects value from nodes dictionary"):
        nodes = workflow.get_downstream_nodes(test_node)
    # get downstream nodes from node4. Should be node5 and node7
    nodes = workflow.get_downstream_nodes(workflow.nodes["node.same_image.4"])
    assert len(nodes) == 2
    assert "node.same_image.5" in nodes
    assert "node.same_image.7" in nodes

    # get downstream nodes from node3. Should be node6.
    # use string input
    nodes = workflow.get_downstream_nodes("node.same_image.3")
    assert len(nodes) == 1
    assert "node.same_image.6" in nodes

    # get downstream nodes from node2. Should be node4, node5 and node7
    nodes = workflow.get_downstream_nodes(workflow.nodes["node.same_image.2"])
    assert len(nodes) == 3
    assert "node.same_image.4" in nodes
    assert "node.same_image.5" in nodes
    assert "node.same_image.7" in nodes

    # get downstream nodes from node1. Should be node2, node3, node4, node5, node6 and node7
    nodes = workflow.get_downstream_nodes("node.same_image.1")
    assert len(nodes) == 6
    assert "node.same_image.2" in nodes
    assert "node.same_image.3" in nodes
    assert "node.same_image.4" in nodes
    assert "node.same_image.5" in nodes
    assert "node.same_image.6" in nodes
    assert "node.same_image.7" in nodes


# test test_get_graph_map
def test_get_graph_map_structure_1():
    log = []
    directory = ImageOperationDirectory(logger = log, testing = True)
    directory.import_operations_dict()
    workflow = WorkFlow(logger = log, image_operation_directiory = directory)

    # create the following structure:
    # node0 -------                     node9 ---------
    #   |         |                       |           |
    #   v         V                       V           V
    # node1     node2 ----> node4       node8       node10
    #   |         |           |           |           |
    #   V         V           V           V           V
    # node3     node5       node6 ----> node7       node11

    workflow.add_node(directory["same_image"])              # node0: node.same_image.0
    workflow.add_node(directory["same_image"])              # node1: node.same_image.1
    workflow.add_node(directory["same_image"])              # node2: node.same_image.2
    workflow.add_node(directory["same_image"])              # node3: node.same_image.3
    workflow.add_node(directory["same_image"])              # node4: node.same_image.4
    workflow.add_node(directory["same_image"])              # node5: node.same_image.5
    workflow.add_node(directory["same_image"])              # node6: node.same_image.6
    workflow.add_node(directory["same_image_two_inputs"])   # node7: node.same_image_two_inputs.7
    workflow.add_node(directory["same_image"])              # node8: node.same_image.8
    workflow.add_node(directory["same_image"])              # node9: node.same_image.9
    workflow.add_node(directory["same_image"])              # node10: node.same_image.10
    workflow.add_node(directory["same_image"])              # node11: node.same_image.11

    workflow.add_connection(source_port = workflow.nodes["node.same_image.0"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image.1"].input_ports["image.input"])
    workflow.add_connection(source_port = workflow.nodes["node.same_image.1"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image.3"].input_ports["image.input"])
    workflow.add_connection(source_port = workflow.nodes["node.same_image.0"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image.2"].input_ports["image.input"])
    workflow.add_connection(source_port = workflow.nodes["node.same_image.2"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image.4"].input_ports["image.input"])
    workflow.add_connection(source_port = workflow.nodes["node.same_image.2"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image.5"].input_ports["image.input"])
    workflow.add_connection(source_port = workflow.nodes["node.same_image.4"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image.6"].input_ports["image.input"])
    workflow.add_connection(source_port = workflow.nodes["node.same_image.6"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image_two_inputs.7"].input_ports["image.input1"])
    workflow.add_connection(source_port = workflow.nodes["node.same_image.8"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image_two_inputs.7"].input_ports["image.input2"])
    workflow.add_connection(source_port = workflow.nodes["node.same_image.9"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image.8"].input_ports["image.input"])
    workflow.add_connection(source_port = workflow.nodes["node.same_image.9"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image.10"].input_ports["image.input"])
    workflow.add_connection(source_port = workflow.nodes["node.same_image.10"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image.11"].input_ports["image.input"])

    assert len(workflow.nodes) == 12
    assert len(workflow.connections) == 11

    # test with invalid input (not string or Node)
    with pytest.raises(TypeError, match = "get_graph_map requires input of Node class, or nodes dictionary key"):
        map = workflow.get_graph_map(workflow)

    # test with invalid input (string but not nodes dictionary key)
    with pytest.raises(ValueError, match = "for string inputs, get_graph_map expects a node dictionary key"):
        map = workflow.get_graph_map("not_a_node_id")

    # test with invalid input (Node class but not nodes dictionary value) 
    test_node = copy.copy(workflow.nodes["node.same_image.0"])
    with pytest.raises(ValueError, match = "for node inputs, get_graph_map expects value from nodes dictionary"):
        map = workflow.get_graph_map(test_node)

    workflow.starting_node = "node.same_image.0"
    map = workflow.get_graph_map(workflow.starting_node)

    assert len(map) == 12
    assert map[0] == "node.same_image.0"
    assert map[1] == "node.same_image.1"
    assert map[2] == "node.same_image.3"
    assert map[3] == "node.same_image.2"
    assert map[4] == "node.same_image.4"
    assert map[5] == "node.same_image.6"
    assert map[6] == "node.same_image.9"
    assert map[7] == "node.same_image.8"
    assert map[8] == "node.same_image_two_inputs.7"
    assert map[9] == "node.same_image.10"
    assert map[10] == "node.same_image.11"
    assert map[11] == "node.same_image.5"
    
def test_get_graph_map_structure_2():
    log = []
    directory = ImageOperationDirectory(logger = log, testing = True)
    directory.import_operations_dict()
    workflow = WorkFlow(logger = log, image_operation_directiory = directory)

#            node0 -------
#              |         |
#              v         v
#            node1     node2
#              |         |
#              v         v
#            node3     node4
#              |         |
#              v         |
#            node5 <------
#              |
#              v
#            node6


    workflow.add_node(directory["same_image"])              # node0: node.same_image.0
    workflow.add_node(directory["same_image"])              # node1: node.same_image.1
    workflow.add_node(directory["same_image"])              # node2: node.same_image.2
    workflow.add_node(directory["same_image"])              # node3: node.same_image.3
    workflow.add_node(directory["same_image"])              # node4: node.same_image.4
    workflow.add_node(directory["same_image_two_inputs"])   # node7: node.same_image_two_inputs.5
    workflow.add_node(directory["same_image"])              # node6: node.same_image.6

    # left branch
    workflow.add_connection(source_port = workflow.nodes["node.same_image.0"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image.1"].input_ports["image.input"])
    workflow.add_connection(source_port = workflow.nodes["node.same_image.1"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image.3"].input_ports["image.input"])
    workflow.add_connection(source_port = workflow.nodes["node.same_image.3"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image_two_inputs.5"].input_ports["image.input1"])

    # right branch
    workflow.add_connection(source_port = workflow.nodes["node.same_image.0"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image.2"].input_ports["image.input"])
    workflow.add_connection(source_port = workflow.nodes["node.same_image.2"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image.4"].input_ports["image.input"])
    workflow.add_connection(source_port = workflow.nodes["node.same_image.4"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image_two_inputs.5"].input_ports["image.input2"])

    workflow.add_connection(source_port = workflow.nodes["node.same_image_two_inputs.5"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image.6"].input_ports["image.input"])

    assert len(workflow.nodes) == 7
    assert len(workflow.connections) == 7

    workflow.starting_node = "node.same_image.0"
    map = workflow.get_graph_map(workflow.starting_node)

    assert len(map) == 7
    assert map[0] == "node.same_image.0"
    assert map[1] == "node.same_image.1"
    assert map[2] == "node.same_image.3"
    assert map[3] == "node.same_image.2"
    assert map[4] == "node.same_image.4"
    assert map[5] == "node.same_image_two_inputs.5"
    assert map[6] == "node.same_image.6"

def test_get_graph_map_structure_3():
    log = []
    directory = ImageOperationDirectory(logger = log, testing = True)
    directory.import_operations_dict()
    workflow = WorkFlow(logger = log, image_operation_directiory = directory)



#            node0           node1
#              |               |
#              v               |
#            node2             |
#              |               |
#              v               |
#            node3  <----------   
#              |         
#              v         
#            node4           node5
#              |               |
#              v               |
#            node6  <----------
#              |
#              v
#            node7


    workflow.add_node(directory["same_image"])              # node0: node.same_image.0
    workflow.add_node(directory["same_image"])              # node1: node.same_image.1
    workflow.add_node(directory["same_image"])              # node2: node.same_image.2
    workflow.add_node(directory["same_image_two_inputs"])   # node3: node.same_image_two_inputs.3
    workflow.add_node(directory["same_image"])              # node4: node.same_image.4
    workflow.add_node(directory["same_image"])              # node5: node.same_image.5
    workflow.add_node(directory["same_image_two_inputs"])   # node6: node.same_image_two_inputs.6
    workflow.add_node(directory["same_image"])              # node7: node.same_image.7

    # left branch
    workflow.add_connection(source_port = workflow.nodes["node.same_image.0"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image.2"].input_ports["image.input"])
    workflow.add_connection(source_port = workflow.nodes["node.same_image.2"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image_two_inputs.3"].input_ports["image.input1"])
    workflow.add_connection(source_port = workflow.nodes["node.same_image_two_inputs.3"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image.4"].input_ports["image.input"])
    workflow.add_connection(source_port = workflow.nodes["node.same_image.4"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image_two_inputs.6"].input_ports["image.input1"])
    workflow.add_connection(source_port = workflow.nodes["node.same_image_two_inputs.6"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image.7"].input_ports["image.input"])

    # right branch
    workflow.add_connection(source_port = workflow.nodes["node.same_image.1"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image_two_inputs.3"].input_ports["image.input2"])
    workflow.add_connection(source_port = workflow.nodes["node.same_image.5"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image_two_inputs.6"].input_ports["image.input2"])


    assert len(workflow.nodes) == 8
    assert len(workflow.connections) == 7

    workflow.starting_node = "node.same_image.0"
    map = workflow.get_graph_map(workflow.starting_node)

    assert len(map) == 8
    assert map[0] == "node.same_image.0"
    assert map[1] == "node.same_image.2"
    assert map[2] == "node.same_image.1"
    assert map[3] == "node.same_image_two_inputs.3"
    assert map[4] == "node.same_image.4"
    assert map[5] == "node.same_image.5"
    assert map[6] == "node.same_image_two_inputs.6"
    assert map[7] == "node.same_image.7"


def test_get_graph_map_structure_4():
    log = []
    directory = ImageOperationDirectory(logger = log, testing = True)
    directory.import_operations_dict()
    workflow = WorkFlow(logger = log, image_operation_directiory = directory)

    #         ----- node0 -----
    #         |       |       |
    #         v       v       v
    #       node1   node3   node5
    #         |       |       |
    #         v       v       v
    #       node2   node4   node6

    workflow.add_node(directory["same_image"])              # node0: node.same_image.0
    workflow.add_node(directory["same_image"])              # node1: node.same_image.1
    workflow.add_node(directory["same_image"])              # node2: node.same_image.2
    workflow.add_node(directory["same_image"])              # node3: node.same_image.3
    workflow.add_node(directory["same_image"])              # node4: node.same_image.4
    workflow.add_node(directory["same_image"])              # node5: node.same_image.5
    workflow.add_node(directory["same_image"])              # node6: node.same_image.6

    # left branch
    workflow.add_connection(source_port = workflow.nodes["node.same_image.0"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image.1"].input_ports["image.input"])
    workflow.add_connection(source_port = workflow.nodes["node.same_image.1"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image.2"].input_ports["image.input"])

    # middle branch
    workflow.add_connection(source_port = workflow.nodes["node.same_image.0"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image.3"].input_ports["image.input"])
    workflow.add_connection(source_port = workflow.nodes["node.same_image.3"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image.4"].input_ports["image.input"])

    # right branch
    workflow.add_connection(source_port = workflow.nodes["node.same_image.0"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image.5"].input_ports["image.input"])
    workflow.add_connection(source_port = workflow.nodes["node.same_image.5"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image.6"].input_ports["image.input"])

    assert len(workflow.nodes) == 7
    assert len(workflow.connections) == 6

    workflow.starting_node = "node.same_image.0"
    map = workflow.get_graph_map(workflow.starting_node)

    assert len(map) == 7
    assert map[0] == "node.same_image.0"
    assert map[1] == "node.same_image.1"
    assert map[2] == "node.same_image.2"
    assert map[3] == "node.same_image.3"
    assert map[4] == "node.same_image.4"
    assert map[5] == "node.same_image.5"
    assert map[6] == "node.same_image.6"

"""test edit_node()"""
# pass in wrong data type, expect TypeError
def test_edit_node_wrong_type():
    log = []
    directory = ImageOperationDirectory(logger = log, testing = True)
    directory.import_operations_dict()
    workflow = WorkFlow(logger = log, image_operation_directiory = directory)

    workflow.add_node(directory["same_image"])

    with pytest.raises(TypeError, match = "edit_node requires input of Node class, or nodes dictionary key"):
        workflow.edit_node(25)

# pass in wrong data type, expect TypeError
def test_edit_node_string_not_key():
    log = []
    directory = ImageOperationDirectory(logger = log, testing = True)
    directory.import_operations_dict()
    workflow = WorkFlow(logger = log, image_operation_directiory = directory)

    workflow.add_node(directory["same_image"])

    with pytest.raises(ValueError, match = "for string inputs, edit_node expects a node dictionary key"):
        workflow.edit_node("same_image")

def test_edit_node_node_not_value():
    log = []
    directory = ImageOperationDirectory(logger = log, testing = True)
    directory.import_operations_dict()
    workflow = WorkFlow(logger = log, image_operation_directiory = directory)

    workflow.add_node(directory["same_image"])
    # test with invalid input (Node class but not nodes dictionary value) 
    test_node = copy.copy(workflow.nodes["node.same_image.0"])
    with pytest.raises(ValueError, match = "for node inputs, edit_node expects value from nodes dictionary"):
        nodes = workflow.edit_node(test_node)

# pass in string for non-existent key, expect ValueError
def test_edit_node_sets_needs_update_to_true():
    log = []
    directory = ImageOperationDirectory(logger = log, testing = True)
    directory.import_operations_dict()
    workflow = WorkFlow(logger = log, image_operation_directiory = directory)

    workflow.add_node(directory["same_image"])
    workflow.nodes["node.same_image.0"].needs_update = False

    assert workflow.nodes["node.same_image.0"].needs_update == False

    workflow.edit_node("node.same_image.0")
    assert workflow.nodes["node.same_image.0"].needs_update == True

# test edit node sets needs_update flag of downstream nodes to True
def test_edit_node_sets_downstream_needs_update_to_true():
    log = []
    directory = ImageOperationDirectory(logger = log, testing = True)
    directory.import_operations_dict()
    workflow = WorkFlow(logger = log, image_operation_directiory = directory)

    # create the following structure:
    # node0
    #   |
    #   v
    # node1 ------> node2
    #   |             |
    #   V             V
    # node3         node4 ------> node5
    #   |             |
    #   V             V
    # node6         node7

    workflow.add_node(directory["same_image"]) # node0: node.same_image.0
    workflow.add_node(directory["same_image"]) # node1: node.same_image.1
    workflow.add_node(directory["same_image"]) # node2: node.same_image.2
    workflow.add_node(directory["same_image"]) # node3: node.same_image.3
    workflow.add_node(directory["same_image"]) # node4: node.same_image.4
    workflow.add_node(directory["same_image"]) # node5: node.same_image.5
    workflow.add_node(directory["same_image"]) # node6: node.same_image.6
    workflow.add_node(directory["same_image"]) # node7: node.same_image.7

    workflow.add_connection(source_port = workflow.nodes["node.same_image.0"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image.1"].input_ports["image.input"])
    
    workflow.add_connection(source_port = workflow.nodes["node.same_image.1"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image.2"].input_ports["image.input"])
    
    workflow.add_connection(source_port = workflow.nodes["node.same_image.1"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image.3"].input_ports["image.input"])
    
    workflow.add_connection(source_port = workflow.nodes["node.same_image.2"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image.4"].input_ports["image.input"])
    
    workflow.add_connection(source_port = workflow.nodes["node.same_image.3"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image.6"].input_ports["image.input"])
    
    workflow.add_connection(source_port = workflow.nodes["node.same_image.4"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image.5"].input_ports["image.input"])

    workflow.add_connection(source_port = workflow.nodes["node.same_image.4"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image.7"].input_ports["image.input"])

    workflow.nodes["node.same_image.0"].needs_update = False
    workflow.nodes["node.same_image.1"].needs_update = False
    workflow.nodes["node.same_image.2"].needs_update = False
    workflow.nodes["node.same_image.3"].needs_update = False
    workflow.nodes["node.same_image.4"].needs_update = False
    workflow.nodes["node.same_image.5"].needs_update = False
    workflow.nodes["node.same_image.6"].needs_update = False
    workflow.nodes["node.same_image.7"].needs_update = False

    workflow.edit_node("node.same_image.1")

    assert workflow.nodes["node.same_image.0"].needs_update == False
    assert workflow.nodes["node.same_image.1"].needs_update == True
    assert workflow.nodes["node.same_image.2"].needs_update == True
    assert workflow.nodes["node.same_image.3"].needs_update == True
    assert workflow.nodes["node.same_image.4"].needs_update == True
    assert workflow.nodes["node.same_image.5"].needs_update == True
    assert workflow.nodes["node.same_image.6"].needs_update == True
    assert workflow.nodes["node.same_image.7"].needs_update == True


