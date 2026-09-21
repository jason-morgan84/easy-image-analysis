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
def test_broken_inputs():
    directory = ImageOperationDirectory(testing = True)
    directory.import_list()

    assert directory.failed_imports == 1
#Test ImageOperation with no/incorrect version number
def test_no_version_number():
    pass

