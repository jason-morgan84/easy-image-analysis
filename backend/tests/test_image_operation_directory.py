import pytest
from core.image_operation_directory import ImageOperationDirectory


# test correct number of files inputted
def test_import_number():
    directory = ImageOperationDirectory(testing = True)
    directory.import_list()

    assert len(directory.image_operation_list) == 1, print(len(directory.image_operation_list))


# import ImageOperation with correct category
def test_import_category():
    directory = ImageOperationDirectory(testing = True)
    directory.import_list()

    log_output = [str(item) for item in directory.logger]

    assert "same_image" in directory.image_operation_list.keys(), f"{log_output}"
    assert directory.image_operation_list["same_image"].category == "Testing"
    assert directory["same_image"].category == "Testing"


# Test ImageOperation with incorrect version number:
# missing_version.py: no version number
# incorrect_version.py: version number in wrong format
@pytest.mark.parametrize("function_name, error_message", [
    ("missing_version","version number expected for module"),
    ("incorrect_version","incorrect version format in")])
def test_incorrect_version_number(function_name, error_message):
    directory = ImageOperationDirectory(testing = True)
    directory.import_list()
    not_imported = [item.import_name for item in directory.logger]

    assert function_name not in directory.image_operation_list.keys()
    assert function_name in not_imported, f"{directory.logger},{directory.failed_imports},{directory.logger[0]}"
    for item in directory.logger:
        if item.import_name == function_name:
            assert error_message in item.message, f"{item.message}"

# Import an ImageOperation that should not be accepted (ie, missing arguements)
# test ImageOperations imported:
# missing_arguements.py: missing_arguements
# invalid_arguement.py: invalid_arguement
# missing_input_image.py: input image as None
@pytest.mark.parametrize("function_name, error_message", [
    ("missing_arguements","cannot import module"),
    ("invalid_arguement","cannot import module"),
    ("missing_input_image","input_image expected")])
def test_inputs_incorrect_arguements(function_name, error_message):
    directory = ImageOperationDirectory(testing = True)
    directory.import_list()
    not_imported = [item.import_name for item in directory.logger]

    assert function_name not in directory.image_operation_list.keys()
    assert function_name in not_imported, f"{directory.logger},{directory.failed_imports},{directory.logger[0]}"
    for item in directory.logger:
        if item.import_name == function_name:
            assert error_message in item.message, f"{item.message}"


# ImageOperation with code failures
# code_invalid.py - error in code when run
# code_output_missing.py - code doesn't produce an output
# code_output_wrong_format_image.py - code produces an image output in the wrong format (not Package class)
# code_output_wrong_format_parameter.py - code produces a parameter output in the wrong format (not Package class)
# code_outout_missing_arguement_image_pixel_array.py - code produces an image output with an missing arguement (pixel_array)
# code_outout_missing_arguement_image_mapping.py - code produces an image output with an missing arguement (mapping)
# code_outout_missing_arguement_parameter_value.py - code produces a parameter output with a missing arguement (value)
# code_outout_incorrect_arguements_image_shape.py - code produces an image output with incorrectly defined shape
@pytest.mark.parametrize("function_name, error_message", [
    # Supply dtype as not member of DataTypes.image_types
    ("code_invalid","error executing operation"),
    ("code_output_missing","operation did not generate an output"),
    ("code_output_wrong_format_image","Expected output to be dictionary of ImageParcel"),
    ("code_output_wrong_format_parameter","Expected output to be dictionary of ParameterParcel"),
    ("code_outout_missing_arguement_image_pixel_array","No image pixel array given for"),
    ("code_output_missing_arguement_image_mapping","No image mapping data given for"),
    ("code_outout_missing_arguement_parameter_value","No value given for parameter output"),
    ("code_outout_incorrect_arguements_image_shape","For output image output, pixel_array dimension")])
def test_incorrect_code(function_name, error_message):
    directory = ImageOperationDirectory(testing = True)
    directory.import_list()
    not_imported = [item.import_name for item in directory.logger]

    assert function_name not in directory.image_operation_list.keys()
    assert function_name in not_imported
    for item in directory.logger:
        if item.import_name == function_name:
            assert error_message in item.message, f"{item.message}"


# Importing ImageOperations with correct code
# - outputs image only
# - outputs parameter only
# - outputs image and parameter
@pytest.mark.parametrize("function_name", [
    # Supply dtype as not member of DataTypes.image_types
    ("code_correct_image_only"),
    ("code_correct_parameter_only"),
    ("code_correct_image_parameter")])
def test_correct_code(function_name):
    directory = ImageOperationDirectory(testing = True)
    directory.import_list()

    for item in directory.logger:
        assert item.import_name != function_name, f"{item.message}"

    assert function_name in directory.image_operation_list.keys()



