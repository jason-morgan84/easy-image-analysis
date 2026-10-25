from core.image_operation_directory import ImageOperationDirectory
from core.data_checks import check_data_dictionary_value, check_metadata_dictionary, check_data_dictionary
from core.metadata import ImageMetadata, ParameterMetadata
from core.io_image_operations import LoadImage, SaveImage
from core.constants import DataPolicy
from core.shape import Shape
from core.workflow import transpose
from core.error_handling import ExportError
import os
import traceback

class TestItem():
    def __init__(self, text, error = None, results = "N\\A"):
        self.text = text
        self.error = error
        self.results = results

def test_image_operation(image_operation_folder, image_operation_name, sample_image=None):

    import_function_errors = [TestItem("Compatible function found","compatible module not found", "N\\A"),
            TestItem("Permitted import checks","module imports", "N\\A"),
            TestItem("Version number checks","version number", "N\\A"),
            TestItem("Function imported","error importing module", "N\\A"),
            TestItem("Metadata for input image present","require input_image_metadata", "N\\A"),
            TestItem("Metadata for output image or parameter present", "require output_image_metadata", "N\\A"),
            TestItem("Metadata for input image is a dictionary", "expected metadata 'input_image' to be dictionary", "N\\A"),
            TestItem("Metadata for input image is a dictionary of ImageMetadata", "for metadata dictionary 'input_image', expected values of type", "N\\A"),
            TestItem("Metadata for input parameters (where present) is a dictionary", "expected metadata 'input_parameter' to be dictionary", "N\\A"),
            TestItem("Metadata for input parameters (where present) is a dictionary of ParameterMetadata", "for metadata dictionary 'input_parameter', expected values of type", "N\\A"),
            TestItem("Function executes", "error executing operation","N\\A"),
            TestItem("Metadata for output images (where present) is a dictionary", "expected metadata 'output_image' to be dictionary","N\\A"),
            TestItem("Metadata for output images (where present) is a dictionary of ImageMetadata", "for metadata dictionary 'output_image', expected values of type","N\\A"),
            TestItem("Output image (where present) is a dictionary","expected data 'output_image' to be dictionary","N\\A"),
            TestItem("Function has metadata to describe output images (where present)", "data present with no metadata: 'output_image'","N\\A"),
            TestItem("Function outputs images as expected given metadata", "metadata present with no data: 'output_image'","N\\A"),
            TestItem("All output images (where present) have matching metadata description","key present in data dictionary 'output_image'","N\\A"),
            TestItem("Output images (where present) have expected data type", "data dictionary value for 'output_image' does not pass dtype validation","N\\A"),
            TestItem("Output images (where present) have expected shape", "image shape does not match metadata; for 'output_image'","N\\A"),
            TestItem("Metadata for output parameters (where present) is a dictionary", "expected metadata 'output_parameter' to be dictionary","N\\A"),
            TestItem("Metadata for output parameters (where present) is a dictionary of ParameterMetadata", "for metadata dictionary 'output_parameter', expected values of type","N\\A"),
            TestItem("Output parameter (where present) is a dictionary","expected data 'output_parameter' to be dictionary","N\\A"),
            TestItem("Function has metadata to describe output parameters (where present)", "data present with no metadata: 'output_parameter'","N\\A"),
            TestItem("Function outputs parameters as expected given metadata", "metadata present with no data: 'output_parameter'","N\\A"),
            TestItem("All output parameters (where present) have matching metadata description","key present in data dictionary 'output_parameter'","N\\A"),
            TestItem("Output parameters (where present) have expected data type", "data dictionary value for 'output_parameter' does not pass dtype validation","N\\A"),
            TestItem("Function does not alter input values", "operation altered input values", "N\\A"),
            TestItem("Function failed testing with randomised data","failed module testing", "N\\A"),
            TestItem("Module can be imported to directory", "module failed to import", "N\\A")]

    # carry out pre-import tests:

    # import function
    error_text = None
    imported_function = None
    test_results = None

    try:
        imported_function = ImageOperationDirectory().import_file(folder = image_operation_folder, name = image_operation_name, logger =[])
    except Exception as import_exception:
        error_text = traceback.format_exc()

    for error in import_function_errors:
        if not error_text:
            error.results = "Pass"
        elif error_text and error.error not in error_text:
            error.results = "Pass"
        else:
            error.results = error_text
            break

    if imported_function:
        # test imported function on sample data
        test_results = TestItem("Module tested with sample data")
        try:
            test_sample_data(imported_function)
            test_results.results = "Pass"
        except Exception as sample_data_exception:
            error_text = traceback.format_exc()
            test_results.results = error_text

        # output to file
        import_function_errors.append(test_results)

    # get results into readable format
    lines = []
    first_line = f"ImageOperation Test Results for '{image_operation_name}'"
    lines.append(first_line)
    lines.append(f"\n{len(first_line)*"-"}\n\n")

    max_length = max(len(item.text) for item in import_function_errors)
    for item in import_function_errors:

        padded_text = item.text.ljust(max_length)
        if item.results == "Pass" or item.results == "N\\A":
            lines.append(f"{padded_text} : {item.results}\n")
        else:
            # if failed test, then item.results will be the error message
            # this is chained up through classes, separated by colons
            # show error message in readable format separated by line
            lines.append(f"{padded_text} : Fail\n")
            error_message = item.results.split(": ")
            for n, section in enumerate(error_message):
                lines.append(f"{"\t"*n}└─> {section}\n")
                lines.append("\n") 

    # give path to saved output image/give output parameter data for test image
    if test_results:
        if test_results.results == "Pass":
            if imported_function.output_image:
                for key in imported_function.output_image.keys():
                    lines.append(f"\nOutput image '{key}' saved to {os.path.join(".\\backend\\tests\\image_operation_test_output",imported_function.id +"_"+ key + "_output.tif")}")
            if imported_function.output_parameter:
                for key, value in imported_function.output_parameter.items():
                    if imported_function.output_parameter_metadata[key].dtype.is_array is False:
                        lines.append(f"\nOutput parameter '{key}': {value}")
                    else:
                        lines.append(f"\nOutput parameter '{key}':")
                        for item in value:
                            lines.append(f"\n{item}")


    with open(".\\backend\\tests\\image_operation_test_output\\test_"+image_operation_name+".txt", "w") as file:
        file.writelines(lines)

    return import_function_errors



        


       
def test_sample_data(imported_function):
    if imported_function:
        input_image = {}
        for key, value in imported_function.input_image_metadata.items():
            # load input image(s) that matches image_type (binarised or non-binarised) and adjust to image dtype
            if value.dtype == DataPolicy.ImageBinary:
                image = LoadImage().load_image(".\\backend\\tests\\test_images\\test_image_binary.tif", shape = "ZCYX")
            else:
                image = LoadImage().load_image(path = ".\\backend\\tests\\test_images\\test_image_8bit.tif", shape = "ZCYX")
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
        try:
            check_data_dictionary_value(data = input_image,
                                        metadata=imported_function.input_image_metadata,
                                        dtype=ImageMetadata,
                                        identifier = "input_image")
        except Exception as e:
            raise RuntimeError(f"error creating test image data for function: {e}")

        # check if test input parameters have been passed
        input_parameter = imported_function.test_input_parameters if hasattr(imported_function, "test_input_parameters") else None
        if imported_function.input_image_metadata is not None and input_parameter is not None:
            function_has_test_input_parameters = True

        # check if test input parameters are valid
        if imported_function.input_parameter_metadata is not None:
            try:
                check_data_dictionary_value(data = input_parameter, 
                                            metadata=imported_function.input_parameter_metadata,
                                            dtype=ParameterMetadata,
                                            identifier = "input_parameter")
            except Exception as e:
                raise RuntimeError(f"error in test parameter data for function: {e}")
        
        # run imported function with given image dictionary
        try:
            output_image, output_parameter = ImageOperationDirectory().test_function(function=imported_function, 
                                                                                        input_image_dictionary = input_image, 
                                                                                        input_parameter_dictionary = input_parameter)
           
        except Exception as execution_exception:
            raise RuntimeError(f"function fails to run with sample data: {e}")
                                                
        # save output image
        try:
            for key, value in output_image.items():
                SaveImage().save_image(image = value, path = os.path.join(".\\backend\\tests\\image_operation_test_output",imported_function.id +"_"+ key + "_output.tif"))
        except Exception as e:
            raise(ExportError(f"error saving image '{key}': {e}"))
