import pytest
from core.image_operation_directory import ImageOperationDirectory


# test correct number of files inputted
def test_number_inputs():
    directory = ImageOperationDirectory()
    directory.import_list()

    assert len(directory.image_operation_list) == 1


# import ImageOperation with correct category
def test_category_inputs():
    directory = ImageOperationDirectory()
    directory.import_list()

    assert directory.image_operation_list["same_image"].category == "Testing"
    assert directory["same_image"].category == "Testing"