from core.image_operation_directory import ImageOperationDirectory
from core.workflow import WorkFlow
from core.frontend_operations import FrontendTypeDescription, create_frontend_node_description
from core.constants import DataPolicy
from fastapi import FastAPI, Request, BackgroundTasks
from core.error_handling import log, GraphError
import json

# set up logger
logger = []

# set up image operation directory
image_operation_directory = ImageOperationDirectory(logger=logger)

# import ImageOperations
image_operation_directory.import_operations_dict()

# set up workflow
workflow = WorkFlow(image_operation_directory=image_operation_directory, 
                    logger=logger)




# get data from all ImageOperations in format to present to frontend
all_data_types = []
for policy in DataPolicy.policies():
    permitted_conversions = [conversion.target_class.__name__ for conversion in policy.permitted_conversions]
    warned_conversions = [conversion.target_class.__name__ for conversion in policy.warned_conversions]
    all_data_types.append(FrontendTypeDescription(
        name=policy.target_class.__name__,
        color=policy.colour,
        compatibleWith=permitted_conversions + warned_conversions
    ))

app = FastAPI()
types_dict = {}
for item in all_data_types:
    types_dict[item.name] = item.__dict__

@app.get("/")
async def root():
    return {"message": f"WorkFlow running"}


# get data from all ImageOperations in format to present to frontend
all_image_operations = []
for id, ImageOperation in image_operation_directory.image_operation_list.items():
    try:
        all_image_operations.append(create_frontend_node_description(ImageOperation))
    except Exception as e:
        log(logger, f"failed to generate ImageOperation description for frontend for '{id}: {e}")

@app.get("/operations")
async def get_operations():
    operations_dict = {}
    for image_operation in all_image_operations:
        operations_dict[image_operation.name] = image_operation.__dict__
    return operations_dict

@app.get("/types")
async def get_types():
    types_dict = {}
    for item in all_data_types:
        types_dict[item.name] = item.__dict__
    return types_dict

@app.post("/new_node")
async def get_new_node(request: Request, background_tasks: BackgroundTasks):
    data = await request.json()
    image_operation = data.get('image_operation')
    id = data.get('id')
    try:
        workflow.add_node(image_operation_directory.image_operation_list[image_operation], id)
    except Exception as e:
        print(f"error creating node: {e}")
        log(logger,GraphError,"error creating node: {e}","main.py","get_new_node",id)

    print(f"NODES: {workflow.nodes.keys()}")
    if id in workflow.nodes.keys() and workflow.nodes[id].image_operation.id == image_operation:
        try:
            background_tasks.add_task(workflow.update_graph)
        except Exception as e:
            print(f"failed to create background task: {e}")
        return{"status": "created", "node": id}
    else:
        return{"status": "failed", "node": id}

@app.post("/remove")
async def get_remove(request: Request):
    data = await request.json()
    nodes = data.get('nodes')
    edges = data.get('edges')
    try:
        output = workflow.remove(node_ids=nodes, connection_ids=[".".join(["connection",connection]) for connection in edges])
    except Exception as e:
        print(f"error removing elements: {e}")
        log(logger,GraphError,"error removing elements: {e}","main.py","get_remove",id)
    #print(workflow.nodes.keys())
    #print(f"id: {id}, {type(id)}, {id in workflow.nodes.keys()}")

    print(f"NODES: {workflow.nodes.keys()}")
    print(f"CONNECTIONS: {workflow.connections.keys()}")

    if output:
        return{"status": "completed"}
    else:
        return{"status": "failed"}

# get data for adding a connection
@app.post("/add_connection")
async def get_add_connection(request: Request, background_tasks: BackgroundTasks):
    data = await request.json()
    id = data.get('id')
    source_node = data.get('source_node')
    source_port = data.get('source_port')
    target_node = data.get('target_node')
    target_port = data.get('target_port')

    workflow.add_connection(source_port=workflow.nodes[source_node].output_ports[source_port],
                            target_port=workflow.nodes[target_node].input_ports[target_port],
                            id=id)

    for item in logger:
        print(f"{item.identifier}: {item.message}")

    print(f"CONNECTIONS: {workflow.connections.keys()}")

    if ".".join(["connection", id]) in workflow.connections.keys():
        try:
            background_tasks.add_task(workflow.update_graph)
        except Exception as e:
            print(f"failed to create background task: {e}")
        return{"status": "completed"}
    else:
        return{"status": "failed"}

@app.post("/set_params")
async def get_set_params(request: Request, background_tasks: BackgroundTasks):
    data = await request.json()
    node_id = data.get('node_id')
    values = data.get('values')

    for key, value in values.items():
        print(f"EDITED NODE BEFORE\n{key}: {workflow.nodes[node_id].input_ports[key].data}")

    workflow.edit_node(node_id, values)

    for item in logger:
        print(f"{item.identifier}: {item.message}")

    validated = True
    for key, value in values.items():
        print(f"EDITED NODE AFTER\n{key}: {workflow.nodes[node_id].input_ports[key].data}")
        if workflow.nodes[node_id].input_ports[key].data != value: validated = False

    if validated:
        try:
            background_tasks.add_task(workflow.update_graph)
        except Exception as e:
            print(f"failed to create background task: {e}")
        return{"status": "completed", "node": node_id}
    else:
        return{"status": "failed", "node": node_id}
        
