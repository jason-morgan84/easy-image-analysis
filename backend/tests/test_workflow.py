import pytest
from core.workflow import WorkFlow
from core.image_operation_directory import ImageOperationDirectory
from core.image_operation import ImageOperation

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

#  call delete_node with an invalid key
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

#  call delete_node
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
# call  add_connection where target is not a port
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
        if item.class_name == "WorkFlow" and item.function_name == "add_connection":
            assert "expected target_port as Port" in item.message 

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


"""copied from get_output testing for connection"""

"""test get_output"""
#Use get_output when no data at source_port

def test_get_output_no_data_at_source_port():
    test_connection = Connection(connection_id = "test",
                                 source_port = Port(True,"a","b"),
                                 target_port = Port(True,"a","b"))

    test_connection.source_port.output_data = None
    """top test commented out: attempted to get data from a port where none is present raises a ConnectionError in the port
    commented out test matches error message from connection if port is changed to break this"""
    #with pytest.raises(ConnectionError, match = "attempt to get output where source_port.output_data has no data present"):
       # test_connection.output_data
    with pytest.raises(ConnectionError, match = "attempt to get port output where no input present"):
        test_connection.output_data

#Use get_output when source_port contains parameter with no value

def test_get_output_no_value_at_source_port():
    test_connection = Connection(connection_id = "test",
                                 source_port = Port(False,"port","node"),
                                 target_port = Port(True,"port","node"))

    test_connection.source_port.input_data = ParameterParcel(dtype = DataType.ValueInt, value = None )
    """as with previous test, doing source_port.output_data where input_data has no pixel_array or value raises a ConnectionError in
    Port - relevant ConenctionError in Conenction (commented out) never reached"""
    #with pytest.raises(ConnectionError, match = "attempt to get output where source_port.output_data has no data present"):
       # test_connection.output_data
    with pytest.raises(ConnectionError, match = "attempt to get port output where no input present"):
        test_connection.output_data

#Use get_output when source_port contains image with no pixel_array
def test_get_output_no_pixel_array_at_source_port():
    test_connection = Connection(connection_id = "test",
                                 source_port = Port(False,"port","node"),
                                 target_port = Port(True,"port","node"))

    test_connection.source_port.input_data = ImageParcel(dtype = DataType.ImageInt, pixel_array = None, image_map=None )
    """as with previous test, doing source_port.output_data where input_data has no pixel_array or value raises a ConnectionError in
    Port - relevant ConenctionError in Conenction (commented out) never reached"""
    #with pytest.raises(ConnectionError, match = "attempt to get output where source_port.output_data has no data present"):
       # test_connection.output_data
    with pytest.raises(ConnectionError, match = "attempt to get port output where no input present"):
        test_connection.output_data

#Test correct output given with no transpose or convert 
def test_get_output_correct_no_transpose_no_convert():
    test_connection = Connection(connection_id = "test",
                                 source_port = Port(False,"port","node"),
                                 target_port = Port(True,"port","node"))

    test_connection.source_port.input_data = ImageParcel(dtype = DataType.ImageInt, pixel_array = sample_data(DataType.ImageInt,[4,3,2,1],numpy = True), image_map = Shape(0,1,2,3) )

    a = test_connection.output_data
    assert np.array_equal(a.pixel_array.value,test_connection.source_port.input_data.pixel_array)
    assert a.pixel_array.value is not None
#Test correct output given with transpose but no convert
def test_get_output_correct_with_transpose_no_convert():
    test_connection = Connection(connection_id = "test",
                                 source_port = Port(False,"port","node"),
                                 target_port = Port(True,"port","node"),
                                 transpose=Shape(3,2,1,0))

    test_connection.source_port.input_data = ImageParcel(dtype = DataType.ImageInt, pixel_array = sample_data(DataType.ImageInt,[4,3,2,1],numpy = True), image_map = Shape(0,1,2,3) )

    a = test_connection.output_data
    assert a is not None
    assert a.pixel_array.value is not None
    assert a.pixel_array.value.shape == (1,2,3,4)

#Test correct output given with convert but no transpose
def test_get_output_correct_with_convert_no_transpose():
    test_connection = Connection(connection_id = "test",
                                 source_port = Port(False,"port","node"),
                                 target_port = Port(True,"port","node"),
                                 convert = DataType.ImageFloat)

    test_connection.source_port.input_data = ImageParcel(dtype = DataType.ImageInt, pixel_array = sample_data(DataType.ImageInt,[4,3,2,1],numpy = True), image_map = Shape(0,1,2,3) )

    a = test_connection.output_data
    assert a is not None
    assert a.pixel_array.value is not None
    assert a.pixel_array.data_type == DataType.ImageFloat
    #assert a.pixel_array.value.shape == (1,2,3,4)
#Test correct output given with transpose and convert
def test_get_output_correct_with_convert_and_transpose():
    test_connection = Connection(connection_id = "test",
                                 source_port = Port(False,"port","node"),
                                 target_port = Port(True,"port","node"),
                                 convert = DataType.ImageFloat,
                                 transpose=Shape(3,2,1,0))

    test_connection.source_port.input_data = ImageParcel(dtype = DataType.ImageInt, pixel_array = sample_data(DataType.ImageInt,[4,3,2,1],numpy = True), image_map = Shape(0,1,2,3) )

    a = test_connection.output_data
    assert a is not None
    assert a.pixel_array.value is not None
    assert a.pixel_array.data_type == DataType.ImageFloat
    assert a.pixel_array.value.shape == (1,2,3,4)