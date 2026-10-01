import pytest
from core.workflow import WorkFlow
from core.image_operation_directory import ImageOperationDirectory
from core.image_operation import ImageOperation

# provide image_operation_directory arguement which is not ImageOperationDirectory class
def test_initialise_not_image_operation_directory():
    a = "test"
    with pytest.raises(TypeError, match = "expected ImageOperationDirectory class on WorkFlow instantiation"):
        workflow = WorkFlow(a)

# call add_node(image_operation) function where image_operation is not ImageOperation class
def test_add_node_not_image_operation():
    directory = ImageOperationDirectory(testing = True)
    workflow = WorkFlow(directory)
    with pytest.raises(TypeError, match = "new node requires ImageOperation class"):
        workflow.add_node("test")

# call add_node(image_operation) function where dictionary key already exists
def test_add_node_existing_key():
    directory = ImageOperationDirectory(testing = True)
    directory.import_operations_dict()
    workflow = WorkFlow(directory)
    workflow.add_node(directory["same_image"])
    workflow.max_id -= 1
    with pytest.raises(TypeError, match = "new node key already in nodes dictionary:"):
        workflow.add_node(directory["same_image"])

# check add_node adds a node
def test_add_node_adds_node():
    directory = ImageOperationDirectory(testing = True)
    directory.import_operations_dict()
    workflow = WorkFlow(directory)
    workflow.add_node(directory["same_image"])
    assert len(workflow.nodes) == 1
    assert workflow.nodes["node.same_image.0"]

#  call delete_node with an invalid key
def test_delete_node_invalid_key():
    directory = ImageOperationDirectory(testing = True)
    directory.import_operations_dict()
    workflow = WorkFlow(directory)
    workflow.add_node(directory["same_image"])
    with pytest.raises(ValueError,match = "id not in node list"):
        workflow.delete_node("test")

#  call delete_node
def test_delete_node_removes_node():
    directory = ImageOperationDirectory(testing = True)
    directory.import_operations_dict()
    workflow = WorkFlow(directory)
    workflow.add_node(directory["same_image"])
    workflow.delete_node("node.same_image.0")
    assert "node.same_image.0" not in workflow.nodes.keys()

# call create connection
def test_connection_add():
    directory = ImageOperationDirectory(testing = True)
    directory.import_operations_dict()
    workflow = WorkFlow(directory)
    workflow.add_node(directory["same_image"])
    workflow.add_node(directory["same_image"])
    workflow.add_connection(source_port = workflow.nodes["node.same_image.0"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image.1"].input_ports["image.input"])
    assert "connection.2" in workflow.connections.keys()

# call delete_connection with an invalid key
def test_connection_delete_invalid_key():
    directory = ImageOperationDirectory(testing = True)
    directory.import_operations_dict()
    workflow = WorkFlow(directory)
    workflow.add_node(directory["same_image"])
    workflow.add_node(directory["same_image"])
    workflow.add_connection(source_port = workflow.nodes["node.same_image.0"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image.1"].input_ports["image.input"])
    with pytest.raises(ValueError,match = "id not in node list"):
        workflow.delete_connection("test")

# check delete_connection removes a connection
def test_connection_delete():
    directory = ImageOperationDirectory(testing = True)
    directory.import_operations_dict()
    workflow = WorkFlow(directory)
    workflow.add_node(directory["same_image"])
    workflow.add_node(directory["same_image"])
    workflow.add_connection(source_port = workflow.nodes["node.same_image.0"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image.1"].input_ports["image.input"])
    workflow.delete_connection("connection.2")
    assert "connection.2" not in workflow.connections.keys()

# check delete_node removes associated connections
def test_node_delete_removes_connections():
    directory = ImageOperationDirectory(testing = True)
    directory.import_operations_dict()
    workflow = WorkFlow(directory)
    workflow.add_node(directory["same_image"])
    workflow.add_node(directory["same_image"])
    workflow.add_connection(source_port = workflow.nodes["node.same_image.0"].output_ports["image.output"],
                            target_port = workflow.nodes["node.same_image.1"].input_ports["image.input"])
    workflow.delete_node("node.same_image.1")
    assert "connection.2" not in workflow.connections.keys()


"""
* call create_connection with invalid connections (invalid port_id, id of soemthign thats not a port, input to conenction also input to node etc) - check errors chained up and logged
* call create_connection where a connection would fail structure checks (connecting input to input/output to output)
* call create_connection where a connection would fail structure checks(connecting to input which already has connections - NB - inputs allow 1 connection, outputs allow many connections)
* call create_connection where a connection would fail structure checks(would result in loop)
* call create_connection where a connection would fail shape checks(invalid shape input image)
* call create_connection where a connection would fail shape checks(invalid type (eg 8 bit image to binarised input))
* call create_connection where a connection would fail shape checks(invalid shape (eg needs flattened image but has z != 1))
* call create_connection where a connection would fail type checks(invalid type (eg 8 bit image to binarised input))
* call create_connection where a connection fails type checks but can be converted (eg 8 bit int to float input)
  - check conversion properly made
"""