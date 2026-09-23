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

    assert directory.image_operation_list["same_image"].category == "Testing"
    assert directory["same_image"].category == "Testing"

# Import an ImageOperation that should not be accepted (ie, missing arguements)
# test ImageOperations imported:
# missing_arguements.py: missing_arguements
# invalid_arguement.py: invalid_arguement
def test_imports_missing_arguements():
    directory = ImageOperationDirectory(testing = True)
    directory.import_list()

    not_imported = [item.import_name for item in directory.logger]
    assert "missing_arguements" not in directory.image_operation_list.keys()
    assert "missing_arguements" in not_imported, f"{directory.logger},{directory.failed_imports},{directory.logger[0]}"

    for item in directory.logger:
        if item.import_name == "missing_arguements":
            assert "cannot import module" in item.message, f"{item.message}"

    assert "missing_arguements" not in directory.image_operation_list.keys()

def test_imports_invalid_arguements():
    directory = ImageOperationDirectory(testing = True)
    directory.import_list()

    not_imported = [item.import_name for item in directory.logger]
    assert "invalid_arguement" not in directory.image_operation_list.keys()
    assert "invalid_arguement" in not_imported, f"{directory.logger},{directory.failed_imports},{directory.logger[0]}"

    for item in directory.logger:
        if item.import_name == "invalid_arguement":
            assert "cannot import module" in item.message, f"{item.message}"

    assert "invalid_arguement" not in directory.image_operation_list.keys()

#Test ImageOperation with no version number
def test_import_version_number_missing():
    directory = ImageOperationDirectory(testing = True)
    directory.import_list()

    not_imported = [item.import_name for item in directory.logger]
    assert "missing_version" not in directory.image_operation_list.keys()
    assert "missing_version" in not_imported, f"{directory.logger},{directory.failed_imports},{directory.logger[0]}"

    for item in directory.logger:
        if item.import_name == "missing_version":
            assert "version number expected for module" in item.message, f"{item.message}"

    assert "missing_version" not in directory.image_operation_list.keys()

#Test ImageOperation with incorrect version number
def test_import_version_number_incorrect():
    directory = ImageOperationDirectory(testing = True)
    directory.import_list()

    not_imported = [item.import_name for item in directory.logger]
    assert "incorrect_version" not in directory.image_operation_list.keys(), f"{directory.image_operation_list.keys()}"
    assert "incorrect_version" in not_imported, f"{directory.logger},{directory.failed_imports},{directory.logger[0]}"
    for item in directory.logger:
        if item.import_name == "incorrect_version":
            assert "incorrect version format in" in item.message, f"{item.message}"

    assert "incorrect_version" not in directory.image_operation_list.keys()


#Test loading an ImageOperation with no input_image
def test_no_input_image():
    directory = ImageOperationDirectory(testing = True)
    directory.import_list()

    not_imported = [item.import_name for item in directory.logger]
    assert "missing_input_image" not in directory.image_operation_list.keys()
    assert "missing_input_image" in not_imported, f"{directory.logger},{directory.failed_imports},{directory.logger[0]}"


    assert "missing_input_image" not in directory.image_operation_list.keys()



