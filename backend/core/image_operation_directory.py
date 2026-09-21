from image_operation import ImageOperation
import importlib
import pkgutil
import os

class ImageOperationDirectory():
    def __init__(self, image_operation_list):
        self.image_operation_list = self.image_operation_list

    def import_list():
        # get list of files to import
        path = ".\\backend\\image_operations"
        folders = [name for name in os.listdir(path) if os.path.isdir(os.path.join(path,name)) and name[0]!="_"]

        package_path="image_operations"
        operations_dict = {}
        # iterates through the list of folders
        for folder in folders:
            # for each folder, imports package
            package = importlib.import_module(package_path + "." + folder)

            # iterates through each module (file) in package (folder)
            for _, name, ispkg in pkgutil.iter_modules(package.__path__):
                # checks its not another package
                if not ispkg:
                    # imports individual file
                    sub_module = importlib.import_module(".".join((package_path, folder, name)))
                    # iterates through each attribute in module
                    for attribute_name in dir(sub_module):
                        
                        """Here we need to check for allowed imports"""
                        attribute = getattr(sub_module, attribute_name)
                        # if its a class that is a subclass of ImageOperation, but not ImageOperation itself (which should never be in that folder anyway)
                        if isinstance(attribute, type) and issubclass(attribute,ImageOperation) and attribute is not ImageOperation:
                                """Here we need to test before importing"""
                                operations_dict[name] = attribute()
                    ##operations_dict.update({name: getattr(sub_module, name)})


        # import each file as an instance of ImageOperation 
        #   check for imports for security
        #   test imported files

        """global variables that need to go somewhere:
                - image_operations path
                - acceptable imports"""
