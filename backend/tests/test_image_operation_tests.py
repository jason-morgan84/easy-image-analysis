from core.image_operation_tests import test_image_operation as check_image_operation

def test_image_operation_tests():
    logger = check_image_operation("testing","same_image")

    for log in logger:
        print(f"\n{log.message}")