from core.image_operation_directory import ImageOperationDirectory
from core.workflow import WorkFlow
from core.frontend_operations import FrontendTypeDescription, create_frontend_node_description
from core.constants import DataPolicy
from fastapi import FastAPI

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
for type in all_data_types:
    types_dict[type.name] = type.__dict__

@app.get("/")
async def root():
    return {"message": f"WorkFlow running"}


# get data from all ImageOperations in format to present to frontend
all_image_operations = []
for ImageOperation in image_operation_directory.image_operation_list.values():
    all_image_operations.append(create_frontend_node_description(ImageOperation))

@app.get("/operations")
async def get_operations():
    operations_dict = {}
    for image_operation in all_image_operations:
        operations_dict[image_operation.name] = image_operation.__dict__
    return operations_dict

@app.get("/types")
async def get_types():
    types_dict = {}
    for type in all_data_types:
        types_dict[type.name] = type.__dict__
    return types_dict