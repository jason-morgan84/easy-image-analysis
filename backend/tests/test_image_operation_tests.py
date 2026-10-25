from core.image_operation_tests import test_image_operation as check_image_operation
import pytest
from core.error_handling import VersionError

# test invalid imported operation
def test_image_operation_invalid_operation():
    

    errors = check_image_operation("testing","doesnt_exist")

    for error in errors:
        if error.text == "Compatible function found":
            assert error.results != "Pass"


# test with 8bit input
def test_test_image_operation():
    
    errors = check_image_operation("testing","same_image")

    for error in errors:
        if error.text == "Module can be imported to directory":
            assert error.results == "Pass"
        if error.text == "Module tested with sample data":
            assert error.results == "Pass"

# test with binary input
    
