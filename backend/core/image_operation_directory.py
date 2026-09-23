from core.image_operation import ImageOperation
import importlib
import pkgutil
import os
from core.error_handling import log
from core.type import sample_data

class ImageOperationDirectory():
    """Key constants for importing ImageOperations"""
    package_folder = "image_operations" # name of base folder for ImageOperations packages
    backend_path = ".\\backend\\" # defines path of backend
    #permitted_imports = set("numpy", "pillow") # defines permitted imports in ImageOperations
 

    def __init__(self, logger = None, testing = False):
        self.image_operation_list = {}
        self.testing = testing
        self.version_mapping = {"0": lambda attr: self.import_0(attr)}
        self.succesful_imports = 0
        self.failed_imports = 0
        self.logger = logger if logger else []

    def __getitem__(self, item):
        return self.image_operation_list[item]

    def import_list(self):
        # get list of files to import
        path = os.path.join(self.backend_path, self.package_folder)
        folders = [name for name in os.listdir(path) if os.path.isdir(os.path.join(path,name)) and name[0]!="_"]

        operations_dict = {}
        # iterates through the list of folders
        for folder in folders:
            # for each folder, imports package
            package = importlib.import_module(self.package_folder + "." + folder)
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
                        sub_module = importlib.import_module(".".join((self.package_folder, folder, name)))
                        try:
                            version = getattr(sub_module, "version")
                        except Exception as e:
                            self.logger.append(log(ImportError,f"version number expected for module {name}: {e}","ImageOperationDirectory","import_list",name))
                            continue
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
                                    self.logger.append(log(ImportError,f"incorrect version format in {name}: {e}","ImageOperationDirectory","import_list",name))
                                    self.failed_imports += 1
                                    continue

                                # use major version number and version_mapping dictionary to import new dictionary item 
                                # with key "name" and value based on return from relevant import function
                                try:
                                    imported_function = self.version_mapping[major](attribute)
                                except Exception as e:
                                    self.logger.append(log(ImportError,f"cannot import module {attribute.__name__}: {e}","ImageOperationDirectory","import_list",name))
                                    self.failed_imports += 1
                                    continue

                                """Here we need to check for allowed imports"""
                                """Here we need to test before importing"""
                                # test_function with appropriate sample data for correct code function and outputs
                                try:
                                    self.test_function(imported_function)
                                except Exception as e:
                                    self.logger.append(log(ImportError,f"module {attribute.__name__} failed inport tests: {e}","ImageOperationDirectory","import_list", name))
                                    self.failed_imports += 1
                                    continue

                                operations_dict[name] = imported_function
                                operations_dict[name].category = current_category
                                operations_dict[name].version = version
                                self.succesful_imports += 1


                                #if import_function:




        # import each file as an instance of ImageOperation 
        #   check for imports for security
        #   test imported files

        """global variables that need to go somewhere:
                - image_operations path
                - acceptable imports"""
        self.image_operation_list = operations_dict
    
    def import_0(self, attribute):

        imported_function = attribute()
        
        return imported_function

    def test_function(self, function):

        # default values for each image dimension if function is indifferent to shape in that dimension
        default_c = 3
        default_z = 4
        default_y = 50
        default_x = 50
        item_shape = [0,0,0,0]

        #loops through input images
        for item in function.input_image.keys():
            # gets dtype of input image
            item_dtype = function.input_image[item].dtype

            # calculates dimensions of shape for pixel_array based on input_image shape and mapping arguements
            item_shape[function.input_image[item].mapping.c] = default_c if function.input_image[item].shape.c == -1 else function.input_image[item].shape.c
            item_shape[function.input_image[item].mapping.z] = default_z if function.input_image[item].shape.z == -1 else function.input_image[item].shape.z
            item_shape[function.input_image[item].mapping.y] = default_y if function.input_image[item].shape.y == -1 else function.input_image[item].shape.y
            item_shape[function.input_image[item].mapping.x] = default_x if function.input_image[item].shape.x == -1 else function.input_image[item].shape.x

            # uses type.sample_data to set pixel_array as an array of the correct shape and dtype of 0s
            function.input_image[item].pixel_array = sample_data(dtype = item_dtype,
                                                                 shape = item_shape,
                                                                 zero = True)

        # similar process for each input_parameter
        for item in function.input_parameter.keys():
            # gets dtype and shape from parameter
            item_dtype = function.input_parameter[item].dtype
            item_shape = function.input_parameter[item].shape

            # sets value to 0/array of 0s of correct dtype and shape using type.sample_data
            function.input_image[item].value = sample_data(dtype = item_dtype,
                                                           shape = item_shape,
                                                           zero = True)

        function.run_code()





        


