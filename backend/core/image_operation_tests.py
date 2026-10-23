from core.image_operation_directory import ImageOperationDirectory
from core.data_checks import check_data_dictionary_value
from core.metadata import ImageMetadata, ParameterMetadata
from core.io_image_operations import LoadImage
from core.constants import DataPolicy
from core.shape import Shape
from core.workflow import transpose

def test_image_operation(image_operation_folder, image_operation_name, sample_image=None):
    __test__ = False
    # define log
    logger = []

    # import function
    imported_function = ImageOperationDirectory().import_file(folder = image_operation_folder, name = image_operation_name, logger = logger)

    if imported_function:
        #test_function = imported_function()

        input_image = {}
        for key, value in imported_function.input_image_metadata.items():
            # load input image(s) that matches image_type (binarised or non-binarised) and adjust to image dtype
            if value.dtype == DataPolicy.ImageBinary:
                image = LoadImage().load_image(".\\backend\\tests\\test_image_binary.tif")
            else:
                image = LoadImage().load_image(path = ".\\backend\\tests\\test_image_8bit.tif", shape = [0,1,2,3])
                if value.dtype == DataPolicy.ImageFloat:
                    image = DataPolicy.ImageInt.to(DataPolicy.ImageFloat, image)

            # adjust to shape
            shape = {}
            shape["c"], shape["z"], shape["y"], shape["x"] = image.shape
            for dimension in Shape.dimensions:
                if value.image_shape_constraints[dimension] != -1:
                    shape[dimension] = value.image_shape_constraints[dimension]
            image = image[0:shape["c"], 0:shape["z"], 0:shape["y"], 0:shape["x"]]
            image = transpose(value=image,
                              current_shape=Shape(c=0,z=1,y=2,x=3),
                              new_shape=value.image_map)


            # add to image dictionary
            input_image[key] = image.copy()
       
        # check input image and parameters
        check_data_dictionary_value(data = input_image,
                                    metadata=imported_function.input_image_metadata,
                                    dtype=ImageMetadata,
                                    identifier = "input_image")
        
        input_parameter = imported_function.test_input_parameters if hasattr(imported_function, "test_input_parameters") else None

        if imported_function.input_parameter_metadata is not None:
            check_data_dictionary_value(data = input_parameter, 
                                        metadata=imported_function.input_parameter_metadata,
                                        dtype=ParameterMetadata,
                                        identifier = "input_parameter")
        
        # run imported function with given image dictionary
        ImageOperationDirectory().test_function(function=imported_function, 
                                                input_image_dictionary = input_image, 
                                                input_parameter_dictionary = input_parameter)
                                                
        # save output image

    # go through log and report pass or fails
    return logger