from core.image_operation import ImageOperation
import importlib
import pkgutil
import os
from core.error_handling import log

class ImageOperationDirectory():


    

    def __init__(self, image_operation_list = {}, testing = False):
        self.image_operation_list = image_operation_list
        self.testing = testing
        self.version_mapping = {"0": lambda attr: self.import_0(attr)}
        self.succesful_imports = 0
        self.failed_imports = 0

    def __getitem__(self, item):
        return self.image_operation_list[item]

    def import_list(self):
        # get list of files to import
        path = ".\\backend\\image_operations"
        folders = [name for name in os.listdir(path) if os.path.isdir(os.path.join(path,name)) and name[0]!="_"]

        package_path="image_operations"
        operations_dict = {}
        # iterates through the list of folders
        for folder in folders:
            # for each folder, imports package
            package = importlib.import_module(package_path + "." + folder)
            current_category = getattr(package,"category")
            # compares whether package has test flag set to True, with ImageOperationDirectory test flag
            try:
                package_test = getattr(package, "test")
            except:
                package_test = False
            if package_test == self.testing:
                # iterates through each module (file) in package (folder)
                for _, name, ispkg in pkgutil.iter_modules(package.__path__):
                    # checks its not another package
                    if not ispkg:
                        # imports individual file
                        sub_module = importlib.import_module(".".join((package_path, folder, name)))
                        try:
                            version = getattr(sub_module, "version")
                        except Exception as e:
                            raise ValueError(f"version number expected for module {name}: {e}")
                        # iterates through each attribute in module
                        for attribute_name in dir(sub_module):
                            attribute = getattr(sub_module, attribute_name)
                            # if its a class that is a subclass of ImageOperation, but not ImageOperation itself (which should never be in that folder anyway)
                            if isinstance(attribute, type) and issubclass(attribute,ImageOperation) and attribute is not ImageOperation:
                                """First, check version is acceptable"""
                                # use version_mapping dictionary to pass attribute to correct import function
                                try: 
                                    major, _, _ = version.split(".")
                                except Exception as e:
                                    log(ValueError,f"incorrect version format in {name}: {e}","ImageOperationDirectory","import_list")
                                    self.failed_imports += 1
                                    major = None
                                    #raise ValueError(f"incorrect version format in {name}: {e}")
                                import_function = self.version_mapping[major](attribute) if major else None
                                if import_function:
                                    operations_dict[name] = import_function
                                    operations_dict[name].category = current_category



        # import each file as an instance of ImageOperation 
        #   check for imports for security
        #   test imported files

        """global variables that need to go somewhere:
                - image_operations path
                - acceptable imports"""
        self.image_operation_list = operations_dict
    
    def import_0(self, attribute):
        """Here we need to check for allowed imports"""
        """Here we need to test before importing"""
        try:
            imported_function = attribute()
            self.succesful_imports += 1
            return imported_function
        except Exception as e:
            log(ValueError,f"cannot import module {attribute.__name__}: {e}","ImageOperationDirectory","import_0")
            self.failed_imports += 1
            return None
            # raise ValueError(f"cannot import module {attribute.__name__}: {e}")
        


