from core.image_operation_directory import ImageOperationDirectory

def test_image_operation(image_operation_path, image_operation_name, sample_image=None):
    # needs to get kwargs for input parameter values

    # define log
    logger = []

    # import function
    imported_function = ImageOperationDirectory.import_file(folder = image_operation_path, name = image_operation_name, logger = logger)

    if imported_function:
        # load input image(s) that matches image_type (binarised or non-binarised)

        # adjust to metadata

        # create image dictionary

        # create parameter dictionary

        # run imported function with given image dictionary
        ImageOperationDirectory.test_function(function=imported_function, 
                                                input_image_dictionary = image_dictionary, 
                                                input_parameter_dictionary = parameter_dictionary)
                                                
        # save output image

    # go through log and report pass or fails