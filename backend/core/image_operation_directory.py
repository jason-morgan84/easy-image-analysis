from core.image_operation import ImageOperation
import core.io_image_operations
import importlib
import pkgutil
import os
from core.error_handling import log, VersionError
from core.data_checks import sample_data, check_metadata_dictionary
import ast
import inspect

class ImageOperationDirectory():
    """Key constants for importing ImageOperations"""
    package_folder = "image_operations" # name of base folder for ImageOperations packages
    backend_path = ".\\backend\\" # defines path of backend
    permitted_imports = {"core",
                         "math", 
                         "numpy",
                         "pillow"} # defines permitted imports in ImageOperations
 

    def __init__(self, logger = None, testing = False):
        self.image_operation_list = {}
        self.testing = testing
        self.version_image_map = {"0": lambda attr: self.import_0(attr),
                                  "1": lambda attr: self.import_1(attr)}
        self.logger = logger if logger else []
        self.disallowed_modules = set()

    def __getitem__(self, item):
        return self.image_operation_list[item]

    def import_operations_dict(self):
        """imports all ImageOperation files from defined folder to image_operation_list.
        For each import, checks that only permitted libraries are imported and provides test input to look for output errors from ImageOperation class"""
        # get list of files to import
        path = os.path.join(self.backend_path, self.package_folder)
        folders = [name for name in os.listdir(path) if os.path.isdir(os.path.join(path,name)) and name[0]!="_"]

        operations_dict = {}
        # iterates through the list of folders
        for folder in folders:
            # for each folder, imports package
            package = importlib.import_module(self.package_folder + "." + folder)

            # checks if folder should be ignored
            try:
                package_ignore = getattr(package, "ignore")
            except:
                package_ignore = False

            if package_ignore == True:
                continue

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
                        try:
                            imported_function = self.import_file(folder = folder, name = name, logger = self.logger)
                        except Exception as e:
                            log(self.logger,ImportError, f"module failed to import '{name}': {e}","ImageOperationDirectory","import_operations_dict", name)
                            continue
                            
                        if imported_function:
                            operations_dict[name] = imported_function
                            operations_dict[name].id = name
                            operations_dict[name].category = current_category
                                
                                
        self.image_operation_list = operations_dict
        self.image_operation_list.update(core.io_image_operations.io_imageoperations)

    def import_file(self, folder, name, logger):
        # imports individual file
        location = ".".join((self.package_folder, folder, name)) if folder else ".".join((self.package_folder, name))
        try:
            sub_module = importlib.import_module(location)
        except Exception as e:
            raise ImportError(f"compatible module not found: {e}")

        """Before running the code, check for only allowed imports"""
        try:
            imported_modules = self.check_imports(inspect.getsource(sub_module))
        except Exception as e:
            raise ImportError(f"error checking module imports: {e}")
            
        self.disallowed_modules = imported_modules - self.permitted_imports
        if self.disallowed_modules:
            raise ImportError(f"non-permitted module imports found: {self.disallowed_modules}")

        """Next, check version is acceptable"""
        try:
            version = getattr(sub_module, "version")
        except Exception as e:
            raise AttributeError(f"no version number found: {e}")

        try: 
            major, _, _ = version.split(".")
        except Exception as e:
            raise ValueError(f"incorrect version number format: {e}")

        """ Once imports and version are checked, get actual ImageOperation class"""
        # iterates through each attribute in module
        for attribute_name in dir(sub_module):
            item = getattr(sub_module, attribute_name)
            # if its a class that is a subclass of ImageOperation, but not ImageOperation itself (which should never be in that folder anyway)
            if isinstance(item, type) and issubclass(item, ImageOperation) and item is not ImageOperation:
                """ Use major version number and version_image_map dictionary to import new dictionary item 
                # with key "name" and value based on return from relevant import function"""
                try:
                    import_function = self.version_image_map[major]
                except Exception as e:
                    raise ImportError(f"no valid import function found: {e}")
                
                try:
                    imported_function = import_function(item)
                except Exception as e:
                    raise ImportError(f"failed to import module: {e}")

                """check code has required inputs and outputs"""
                try:
                    self.check_inputs_outputs(imported_function)
                except Exception as e:
                    raise AttributeError(f"failed input/output checks: {e}")


                """test code to ensure it runs and gives expected output given sample input"""
                try:
                    self.test_function(imported_function)
                except Exception as e:
                    raise ImportError(f"failed module testing: {e}")
                
                imported_function.version = version
                return imported_function
    
    def import_0(self, attribute):
        """imports functions where major version is 0"""
        raise VersionError(f"ImportOperationDirectory not back compatible to major version 0, cannot import '{attribute}'")


    def import_1(self, image_op):
        """imports functions where major version is 1"""
        imported_image_op = image_op()
        return imported_image_op
    
    def check_imports(self, function):
        """gets a list of all modules imported into 'function' and 
        checks them against permitted module names"""

        imported_modules = set() # set to hold names of any imported modules
        ast_code = ast.parse(function) # parses imported code into ast nodes

        # Iterates through each ast node in ast_code.
        # Looks for nodes of the Import class and nodes of the ImportFrom class.
        # Where it finds them, adds the relevant module name to modules set
        for node in ast.walk(ast_code): 
            if isinstance (node, ast.Import):
                for alias in node.names:
                    imported_modules.add(alias.name.split('.')[0])
            elif isinstance (node, ast.ImportFrom):
                if node.module:
                    imported_modules.add(node.module.split('.')[0])
        # non-permited imports are any modules left after subtracting 
        # permitted imports from imported modules
        return imported_modules

    def check_inputs_outputs(self, function):
        # to import an ImageOperation, it must define an input image (through input_image_metadata dictionary) and an output 
        # (through either output_image_metadata or output_parameter_metadata dictionaries)
        if not function.input_image_metadata:
            raise AttributeError(f"imported ImageOperations require input_image_metadata")
              
        if not function.output_image_metadata and not function.output_parameter_metadata:
            raise AttributeError(f"imported ImageOperations require output_image_metadata or output_parameter_metadata")

        # if dictionaries exist, their format will have been checked by ImageOperation clas      

    def test_function(self, function, input_image_dictionary = None, input_parameter_dictionary = None):
        """tests functions by providing sample inputs (given requested input dtype, shape etc). Actual outputs are checked in ImageOperation.run_code and any
        errors will be chained here, then to input_list function where they're logged."""
        # default values for each image dimension if function is indifferent to shape in that dimension
        default_c = 3
        default_z = 4
        default_y = 50
        default_x = 50
        image_shape = [0,0,0,0]

        input_images = {}
        input_parameters = {}
        #loops through input images
        if not input_image_dictionary:
            for key, value in function.input_image_metadata.items():
                # gets dtype of input image
                image_dtype = value.dtype


                # calculates dimensions of shape for pixel_array based on input_image shape and image_map arguements
                image_shape[value.image_map.c] = default_c if value.image_shape_constraints.c == -1 else value.image_shape_constraints.c
                image_shape[value.image_map.z] = default_z if value.image_shape_constraints.z == -1 else value.image_shape_constraints.z
                image_shape[value.image_map.y] = default_y if value.image_shape_constraints.y == -1 else value.image_shape_constraints.y
                image_shape[value.image_map.x] = default_x if value.image_shape_constraints.x == -1 else value.image_shape_constraintse.x

                # uses type.sample_data to set pixel_array as an array of the correct shape and dtype of 0s
                input_images[key] = sample_data(dtype=image_dtype,
                                                shape = image_shape,
                                                zero = True)
        else:
            input_images = input_image_dictionary

        setattr(function,"input_image", input_images)

        # similar process for each input_parameter
        
        if function.input_parameter_metadata is not None:
            if not input_parameter_dictionary:
                for key, value in function.input_parameter_metadata.items():
                    # gets dtype and shape from parameter
                    parameter_dtype = value.dtype
                    parameter_shape = value.shape

                    # sets value to 0/array of 0s of correct dtype and shape using type.sample_data
                    input_parameters[key] = sample_data(dtype = parameter_dtype,
                                                        shape = parameter_shape,
                                                        zero = True)
            else:
                input_parameters = input_parameter_dictionary
            setattr(function,"input_parameter",input_parameters)
        
        
        function.run_code()
        return function.output_image, function.output_parameter





        


