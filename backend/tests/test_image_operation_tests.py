from core.image_operation_tests import test_image_operation as check_image_operation
from core.image_operation_tests import import_function_errors
import pytest
import copy
from core.error_handling import VersionError




# test invalid imported operation
def test_image_operation_invalid_operation():
    

    errors = check_image_operation("testing", "doesnt_exist")

    for error in errors:
        if error.feedback_text == "Compatible function found":
            assert error.results != "Pass"


# test with 8bit input
def test_test_image_operation_8bit():
    
    errors = check_image_operation("testing", "same_image")

    for error in errors:
        if error.feedback_text == "Module can be imported to directory":
            assert error.results == "Pass"
        if error.feedback_text == "Module tested with sample data":
            assert error.results == "Pass"

# test with binary input
def test_test_image_operation_binary():
    
    errors = check_image_operation("testing", "binarised_input")

    for error in errors:
        if error.feedback_text == "Module can be imported to directory":
            assert error.results == "Pass"
        if error.feedback_text == "Module tested with sample data":
            assert error.results == "Pass"

def test_test_image_operation_all():
    # imports list of all possible error messages and test files from image_operation_tests
    tests = copy.copy(import_function_errors)
    for n, test in enumerate(tests):
        # where a test_file is present
        if test.test_file != "" and n > 0:
            print(f"\n{n}: {test.feedback_text} using {test.test_file}")
            output_errors = check_image_operation("testing", test.test_file)
            # loops through all error messages
            for error in output_errors:
            # checks to make sure previous test was passed
                if error.feedback_text == tests[n-1].feedback_text:
                    print(f"\t{tests[n-1].feedback_text}: {error.results}")
                    assert error.results == "Pass"
            # checks to make sure currently tested item was failed
                if error.feedback_text == test.feedback_text:
                    print(f"\t{error.feedback_text}: {"Fail" if error.results!= "Pass" and error.results != "N\\A" else error.results}")
                    assert error.results != "Pass" and error.results != "N\\A"
            # checks to make sure next item is N\A (can't be tested because current item failed)
                if n < len(tests) - 1:
                    if error.feedback_text == tests[n+1].feedback_text:
                        print(f"\t{error.feedback_text}: {error.results}")
                        assert error.results == "N\\A"


