import pytest
import numpy as np
from core.type import ImageInt

def test_data_type_ImageInt():
    mock_image_0_0 = np.array([[0, 0], 
                            [0, 0]], dtype=np.uint8)

    mock_image_0_1 = np.array([[1, 1], 
                            [1, 1]], dtype=np.uint8)

    mock_image_0_2 = np.array([[2, 2], 
                            [2, 2]], dtype=np.uint8)


    mock_image_0 = np.array ([mock_image_0_0, mock_image_0_1, mock_image_0_2])
    mock_image = np.array([mock_image_0, mock_image_0 + 10, mock_image_0 + 20, mock_image_0 + 30])

    test_value1 = 2
    test_value2 = -5
    test_value3 = 2267
    test_value4 = 0.5
    test_value5 = 5.0

    with pytest.raises(ValueError):
        ImageInt(test_value2)

    with pytest.raises(ValueError):
        ImageInt(test_value3)

    with pytest.raises(TypeError):
        ImageInt(test_value4)

    with pytest.raises(TypeError):
        ImageInt(test_value5)

    ImageInt(mock_image)

    assert mock_image.shape == (4,3,2,2)





