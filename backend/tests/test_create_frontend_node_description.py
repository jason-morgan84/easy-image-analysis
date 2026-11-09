import pytest
from core.frontend_operations import create_frontend_node_description
from core.image_operation_directory import ImageOperationDirectory

# test type checks - send in input not as image_operation - TypeError: expected image_operation type
def test_type_checks():
    with pytest.raises(TypeError, match="expected image_operation type"):
        create_frontend_node_description("image_operation")

def test_correct_output():

    # set up logger
    logger = []

    # set up image operation directory
    image_operation_directory = ImageOperationDirectory(logger=logger)

    # import ImageOperations
    image_operation_directory.import_operations_dict()

    output = create_frontend_node_description(image_operation_directory.image_operation_list["gaussian_filter"])

    assert output.id == "gaussian_filter"
    assert output.name == "Gaussian filter"
    assert output.category == "Filters"
    assert output.docs=="Applies a gaussian filter to the image, smoothing it and reducing noise. Sigma controls the area over which the filter is applied. The larger the sigma, the heavier the blurring. A good starting value is sigma = 3."
    assert output.alerts == None


    assert len(output.ports) == 2
    assert "output" in [port.name for port in output.ports]
    assert "input" in [port.name for port in output.ports]

    for port in output.ports:
        if port.name == "output":
            assert port.dtype == "ImageInt"
            assert port.id == "image.output"
            assert port.is_input == False
        if port.name == "intput":
            assert port.dtype == "ImageInt"
            assert port.id == "image.intput"
            assert port.is_input == True

    assert len(output.parameters) == 1
    assert "sigma" in [parameter.name for parameter in output.parameters]
    for parameter in output.parameters:
        if port.name == "sigma":
            assert port.dtype == "ValueInt"
            assert port.id == "parameter.sigma"
            assert port.is_input == True
            assert port.user_input_method == "integer"
            assert port.user_input_options == {"type": "slider", "min": 0, "max": 10, "step": 1, "slider": True}


