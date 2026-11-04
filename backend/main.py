from core.image_operation_directory import ImageOperationDirectory
from core.workflow import WorkFlow
from fastapi import FastAPI

def main():
    # set up logger
    logger = []

    # set up image operation directory
    image_operation_directory = ImageOperationDirectory(logger=logger)

    # import ImageOperations
    image_operation_directory.import_operations_dict()

    # set up workflow
    workflow = WorkFlow(image_operation_directory=image_operation_directory, 
                        logger=logger)

    

main()

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}