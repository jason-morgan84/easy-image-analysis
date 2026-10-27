from core.image_operation_tests import test_image_operation as check_image_operation
import pytest
from core.error_handling import VersionError




# test invalid imported operation
def test_image_operation_invalid_operation():
    

    errors = check_image_operation("testing", "doesnt_exist")

    for error in errors:
        if error.text == "Compatible function found":
            assert error.results != "Pass"


# test with 8bit input
def test_test_image_operation_8bit():
    
    errors = check_image_operation("testing", "same_image")

    for error in errors:
        if error.text == "Module can be imported to directory":
            assert error.results == "Pass"
        if error.text == "Module tested with sample data":
            assert error.results == "Pass"

# test with binary input
def test_test_image_operation_binary():
    
    errors = check_image_operation("testing", "binarised_input")

    for error in errors:
        if error.text == "Module can be imported to directory":
            assert error.results == "Pass"
        if error.text == "Module tested with sample data":
            assert error.results == "Pass"

"""Test failures updated properly for all of the following"""
class ErrorFiles():
    def __init__ (self, error_to_check, file):
        self.error_to_check = error_to_check
        self.file = file
tests = [
ErrorFiles("Compatible function found", ""),
ErrorFiles("Permitted import checks",  "code_import_invalid"),
ErrorFiles("Version number checks",  "incorrect_version"),
ErrorFiles("Function imported",  "unexpected_version"),
ErrorFiles("Metadata for input image present",  "missing_input_image"),
ErrorFiles("Metadata for output image or parameter present",  "code_output_metadata_missing"),
ErrorFiles("Metadata for input image is a dictionary",  "code_input_image_metadata_not_dictionary"),
ErrorFiles("Metadata for input image is a dictionary of ImageMetadata",  "code_input_image_metadata_not_dictionary_of_ImageMetadata"),
ErrorFiles("Metadata for input parameters* is a dictionary",  "code_input_parameter_metadata_not_dictionary"),
ErrorFiles("Metadata for input parameters* is a dictionary of ParameterMetadata",  "code_input_parameter_metadata_not_dictionary_parameter_metadata"),
ErrorFiles("Metadata for output images* is a dictionary",  "code_output_image_metadata_not_dictionary"),
ErrorFiles("Metadata for output images* is a dictionary of ImageMetadata",  "code_output_image_metadata_not_dictionary_imagemetadata"),
ErrorFiles("Output image* is a dictionary",  "code_output_image_not_dictionary"),
ErrorFiles("Output image dictionary* has output image metadata dictionary",  "code_output_image_no_metadata"),
ErrorFiles("Output image metadata dictionary* has output image dictionary",  "code_output_image_metadata_with_no_data"),
ErrorFiles("Each output image* has a key-matched metadata description",  "code_output_image_data_with_no_metadata_key"),
ErrorFiles("Output images* have expected data type",  "code_output_image_data_wrong_type"),
ErrorFiles("Output images* have expected shape",  "code_output_image_data_wrong_shape"),
ErrorFiles("Metadata for output parameters* is a dictionary",  "code_output_parameter_metadata_not_dictionary"),
ErrorFiles("Metadata for output parameters* is a dictionary of ParameterMetadata",  "code_output_parameter_metadata_not_dictionary_parametermetadata"),
ErrorFiles("Output parameter* is a dictionary",  "code_output_parameter_not_dictionary"),
ErrorFiles("Output parameter dictionary* has output parameter metadata dictionary",  "code_output_parameter_no_metadata"),
ErrorFiles("Output parameter metadata dictionary* has output parameter dictionary",  "code_output_parameter_metadata_with_no_data"),
ErrorFiles("Each output parameter* has a key-matched metadata description",  "code_output_parameter_data_with_no_metadata_key"),
ErrorFiles("Output parameters* have expected data type",  "code_output_parameter_data_wrong_type"),
ErrorFiles("Function executes",  "code_invalid"),
ErrorFiles("Function does not alter input values",  "code_alters_input"),
# Both following tests removed because can't provide code to break this without also causing a previous error
#ErrorFiles("Function failed testing with randomised data",  "code_fails_random_testing"),
#ErrorFiles("Module can be imported to directory",  "")
]

def test_test_image_operation_all():
    for n, test in enumerate(tests):
        if test.file != "" and n > 0:
            print(f"\n{n}: {test.error_to_check} using {test.file}")
            output_errors = check_image_operation("testing", test.file)
            for error in output_errors:
                if error.text == tests[n-1].error_to_check:
                    print(f"\t{tests[n-1].error_to_check}: {error.results}")
                    assert error.results == "Pass"
                if error.text == test.error_to_check:
                    print(f"\t{error.text}: {"Fail" if error.results!= "Pass" and error.results != "N\\A" else error.results}")
                    assert error.results != "Pass" and error.results != "N\\A"

                if n < len(tests) - 1:
                    if error.text == tests[n+1].error_to_check:
                        print(f"\t{error.text}: {error.results}")
                        assert error.results == "N\\A"


