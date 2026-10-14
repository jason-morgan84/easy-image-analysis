import pytest
from core.workflow import WorkFlow
from core.image_operation_directory import ImageOperationDirectory
from core.image_operation import ImageOperation
from core.constants import DataType
from core.interface_classes import Connection, Port

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

# all delete_node
def test_delete_node_removes_node():
    log = []
    directory = ImageOperationDirectory(logger = log, testing = True)
    directory.import_operations_dict()
    workflow = WorkFlow(logger = log, image_operation_directiory = directory)
    workflow.add_node(directory["same_image"])
    workflow.delete_node("node.same_image.0")
    assert "node.same_image.0" not in workflow.nodes.keys()

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

# test get_next_nodes
def test_get_next_nodes():
    log = []
    directory = ImageOperationDirectory(logger = log, testing = True)
    directory.import_operations_dict()
    workflow = WorkFlow(logger = log, image_operation_directiory = directory)

    workflow.add_node(directory["same_image"])
    workflow.add_node(directory["same_image"])
    workflow.add_node(directory["same_image"])
    workflow.add_node(directory["same_image"])
    # four nodes, node.same_image.0, node.same_image.1, node.same_image.2, node.same_image.3
    # node.same_image.0 connects to node.same_image.1 (connection.4)
    # node.same_image.1 connects to node.same_image.2 (connection.5) and node.same_image.3 (connection.6) through output port image.output

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

    # test get_next_nodes from string "node.same_image.0" expect typeerror
    with pytest.raises(TypeError, match = "get_next_nodes requires input of Port, Node or Connection class"):
        nodes = workflow.get_next_nodes("node.same_image.0")

    # test get_next_nodes from input port "workflow.nodes["node.same_image.1"].input_ports["image.input"]"
    with pytest.raises(ValueError, match = "get_next_nodes requires output port, not input port"):
        nodes = workflow.get_next_nodes(workflow.nodes["node.same_image.1"].input_ports["image.input"])


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

# call create_connection where a connection would fail type checks(invalid type (eg 8 bit image to binarised input))
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

# call create_connection where a connection fails type checks but can be converted with warning (eg binarised to 8 bit int)
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

# call create_connection where a connection fails type checks but can be converted (eg 8 bit int to float input)
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

# call create_connection where a connection would fail shape checks(invalid shape (eg needs flattened image but has z != 1))
def test_connection_wrong_shape():
    log = []
    directory = ImageOperationDirectory(logger = log, testing = True)
    directory.import_operations_dict()

    workflow = WorkFlow(logger = log, image_operation_directiory = directory)
    workflow.add_node(directory["same_image"])
    workflow.add_node(directory["single_channel_input"])
    workflow.add_connection(source_port = workflow.nodes["node.same_image.0"].output_ports["image.output"],
                            target_port = workflow.nodes["node.single_channel_input.1"].input_ports["image.input"])

    for item in log:
        print(item.message)
        if item.class_name == "WorkFlow" and item.function_name == "add_connection":
            assert item.identifier == "image.output.image.input"
            assert "connection not created (failed at shape checks):invalid image shapes: target port 'image.input' requires c=1, for source_port 'image.output', c=-1" in item.message 

# call create_connection where a connection would pass shape checks but require transposition
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

# call create_connection where a connection would fail structure checks (connecting port to itself)
# call create_connection where a connection would fail structure checks (connecting input to input/output to output)
# call create_connection where a connection would fail structure checks(connecting to input which already has connections - NB - inputs allow 1 connection, outputs allow many connections)
# call create_connection where a connection would fail structure checks(would result in loop)

# call create_connection where a connection would fail structure checks (connecting port to itself)
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

# call create_connection where a connection would fail structure checks (connecting input to input/output to output)
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

# call create_connection where a connection would fail structure checks(connecting to input which already has connections - NB - inputs allow 1 connection, outputs allow many connections)
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

# call create_connection where a connection would fail structure checks(would result in loop)
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
