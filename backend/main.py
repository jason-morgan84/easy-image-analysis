from core.image_operation_directory import ImageOperationDirectory
from core.workflow import WorkFlow
from core.frontend_operations import ImageOperationData
from fastapi import FastAPI
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
all_image_operations = []
for ImageOperation in image_operation_directory.image_operation_list.values():
    all_image_operations.append(ImageOperationData(
        id=ImageOperation.id,
        name=ImageOperation.name,
        category=ImageOperation.category,
        docs=ImageOperation.docs,
        alerts=ImageOperation.alerts
    ))


app = FastAPI()


@app.get("/")
async def root():
    return {"message": f"WorkFlow running"}

@app.get("/operations")
async def get_operations():
    operations_dict = {}
    for image_operation in all_image_operations:
        operations_dict[image_operation.name] = image_operation.__dict__
    return operations_dict