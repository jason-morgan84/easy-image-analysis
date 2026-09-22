import pytest
from core.image_operation_directory import ImageOperationDirectory


# test correct number of files inputted
def test_number_inputs():
    directory = ImageOperationDirectory(testing = True)
    directory.import_list()

    assert len(directory.image_operation_list) == 3, print(len(directory.image_operation_list))


# import ImageOperation with correct category
def test_category_inputs():
    directory = ImageOperationDirectory(testing = True)
    directory.import_list()

    assert directory.image_operation_list["same_image"].category == "Testing"
    assert directory["same_image"].category == "Testing"

# Import an ImageOperation that should not be accepted (ie, missing arguements)
# test ImageOperations imported:
# missing_arguements.py: missing_arguements
# invalid_arguement.py: invalid_arguement
def test_broken_inputs():
    directory = ImageOperationDirectory(testing = True)
    directory.import_list()

    assert "missing_arguements" not in directory.image_operation_list.keys()
    assert "invalid_arguement" not in directory.image_operation_list.keys()

#Test ImageOperation with no/incorrect version number
def test_no_version_number():
    pass

