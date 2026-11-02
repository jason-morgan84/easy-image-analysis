from core.frontend_operations import create_image, import_luts
import tifffile
from PIL import Image
import numpy as np
import pytest

"""check input image """
# send in non np.ndarray - TypeError: expected input_image as np.ndarray 
def test_non_np_image():
    image = [[1,2,3],[1,2,3]]
    loaded_luts = import_luts()

    lut_list = {0:loaded_luts["Magenta hot"],
                1:loaded_luts["Cyan hot"],
                2:loaded_luts["Yellow"]}
    with pytest.raises(TypeError, match = "expected input_image as np.ndarray"):
        outputimage = create_image(image, lut_list, 3, 0, 0, 1.0)

# send in np.ndarray not of np.uint8 - TypeError: expected input_image as np.ndarray of np.uint8 .
def test_non_npuintt8_image():
    image = np.array([[1,2,3],[1,2,3]],np.uint16)
    loaded_luts = import_luts()

    lut_list = {0:loaded_luts["Magenta hot"],
                1:loaded_luts["Cyan hot"],
                2:loaded_luts["Yellow"]}
    with pytest.raises(TypeError, match = "expected input_image as np.ndarray of np.uint8"):
        outputimage = create_image(image, lut_list, 3, 0, 0, 1.0)
"""check luts"""
# send in luts not as dictionary - TypeError: expected luts as dictionary 
def test_non_dictionary_luts():
    image = tifffile.imread(".\\backend\\tests\\test_images\\test_image_8bit.tif").transpose((1,0,2,3))
    loaded_luts = import_luts()

    lut_list = [0,loaded_luts["Magenta hot"],
                1,loaded_luts["Cyan hot"],
                2,loaded_luts["Yellow"]]
    with pytest.raises(TypeError, match = "expected luts as dictionary"):
        outputimage = create_image(image, lut_list, 3, 0, 0, 1.0)

# send in luts with non-integer key - TypeError: expected luts keys as integers 
def test_non_int_lut_keys():
    image = tifffile.imread(".\\backend\\tests\\test_images\\test_image_8bit.tif").transpose((1,0,2,3))
    loaded_luts = import_luts()

    lut_list = {0:loaded_luts["Magenta hot"],
                "green":loaded_luts["Cyan hot"],
                2:loaded_luts["Yellow"]}
    with pytest.raises(TypeError, match = "expected luts keys as integers"):
        outputimage = create_image(image, lut_list, 3, 0, 0, 1.0)

# send in luts with key that doesn't match channel - ValueError: luts dictionary contains out of range key 
def test_incorrect_lut_keys():
    image = tifffile.imread(".\\backend\\tests\\test_images\\test_image_8bit.tif").transpose((1,0,2,3))
    loaded_luts = import_luts()

    lut_list = {0:loaded_luts["Magenta hot"],
                5:loaded_luts["Cyan hot"],
                2:loaded_luts["Yellow"]}
    with pytest.raises(ValueError, match = "luts dictionary contains out of range key"):
        outputimage = create_image(image, lut_list, 3, 0, 0, 1.0)

# send in luts with non-dictionary value - TypeError: expected luts values as np.ndarray 
def test_incorrect_lut_value():
    image = tifffile.imread(".\\backend\\tests\\test_images\\test_image_8bit.tif").transpose((1,0,2,3))
    loaded_luts = import_luts()

    lut_list = {0:"Non-existent LUT",
                1:loaded_luts["Cyan hot"],
                2:loaded_luts["Yellow"]}
    with pytest.raises(TypeError, match = "expected luts values as np.ndarray"):
        outputimage = create_image(image, lut_list, 3, 0, 0, 1.0)
# send in luts with value that isn't of correct shape - ValueError: expected luts values as np.ndarray of shape (256,3)
def test_incorrect_lut_shape():
    image = tifffile.imread(".\\backend\\tests\\test_images\\test_image_8bit.tif").transpose((1,0,2,3))
    loaded_luts = import_luts()

    lut_list = {0:np.array([1,2,3]),
                1:loaded_luts["Cyan hot"],
                2:loaded_luts["Yellow"]}
    with pytest.raises(ValueError, match = "expected luts values as np.ndarray of shape"):
        outputimage = create_image(image, lut_list, 3, 0, 0, 1.0)
"""check centres"""
# send in centre_y not as integer  - TypeError: expected centre_y as integer
def test_centre_y_not_integer():
    image = tifffile.imread(".\\backend\\tests\\test_images\\test_image_8bit.tif").transpose((1,0,2,3))
    loaded_luts = import_luts()

    lut_list = {0:loaded_luts["Magenta hot"],
                1:loaded_luts["Cyan hot"],
                2:loaded_luts["Yellow"]}
    with pytest.raises(TypeError, match = "expected centre_y as integer"):
        outputimage = create_image(image, lut_list, 3, "0", 0, 1.0)
# send in centre_y less than 0 or higher than image size  - ValueError: centre_y out of range for image sizer
def test_centre_y_not_valid():
    image = tifffile.imread(".\\backend\\tests\\test_images\\test_image_8bit.tif").transpose((1,0,2,3))
    loaded_luts = import_luts()

    lut_list = {0:loaded_luts["Magenta hot"],
                1:loaded_luts["Cyan hot"],
                2:loaded_luts["Yellow"]}
    with pytest.raises(ValueError, match = "centre_y out of range for image size"):
        outputimage = create_image(image, lut_list, 3, -5, 0, 1.0)
# send in centre_y not as integer  - TypeError: expected centre_y as integer
def test_centre_x_not_integer():
    image = tifffile.imread(".\\backend\\tests\\test_images\\test_image_8bit.tif").transpose((1,0,2,3))
    loaded_luts = import_luts()

    lut_list = {0:loaded_luts["Magenta hot"],
                1:loaded_luts["Cyan hot"],
                2:loaded_luts["Yellow"]}
    with pytest.raises(TypeError, match = "expected centre_x as integer"):
        outputimage = create_image(image, lut_list, 3, 0, "0", 1.0)
# send in centre_x less than 0 or higher than image size  - ValueError: centre_y out of range for image sizer
def test_centre_x_not_valid():
    image = tifffile.imread(".\\backend\\tests\\test_images\\test_image_8bit.tif").transpose((1,0,2,3))
    loaded_luts = import_luts()

    lut_list = {0:loaded_luts["Magenta hot"],
                1:loaded_luts["Cyan hot"],
                2:loaded_luts["Yellow"]}
    with pytest.raises(ValueError, match = "centre_x out of range for image size"):
        outputimage = create_image(image, lut_list, 3, 0, 5000, 1.0)

"""check zoom"""
# send in zoom not as float  - TypeError: expected zoom as float
def test_zoom_not_float():
    image = tifffile.imread(".\\backend\\tests\\test_images\\test_image_8bit.tif").transpose((1,0,2,3))
    loaded_luts = import_luts()

    lut_list = {0:loaded_luts["Magenta hot"],
                1:loaded_luts["Cyan hot"],
                2:loaded_luts["Yellow"]}
    with pytest.raises(TypeError, match = "expected zoom as float"):
        outputimage = create_image(image, lut_list, 3, 0, 50, 1)
# end in zoom less than zoom_min  - ValueError: zoom less than minimum allowed value
def test_zoom_too_low():
    image = tifffile.imread(".\\backend\\tests\\test_images\\test_image_8bit.tif").transpose((1,0,2,3))
    loaded_luts = import_luts()

    lut_list = {0:loaded_luts["Magenta hot"],
                1:loaded_luts["Cyan hot"],
                2:loaded_luts["Yellow"]}
    with pytest.raises(ValueError, match = "zoom less than minimum allowed value"):
        outputimage = create_image(image, lut_list, 3, 0, 50, 0.001)
# send in zoom greater than zoom_max  - ValueError: zoom greater than maximum allowed value
def test_zoom_too_high():
    image = tifffile.imread(".\\backend\\tests\\test_images\\test_image_8bit.tif").transpose((1,0,2,3))
    loaded_luts = import_luts()

    lut_list = {0:loaded_luts["Magenta hot"],
                1:loaded_luts["Cyan hot"],
                2:loaded_luts["Yellow"]}
    with pytest.raises(ValueError, match = "zoom greater than maximum allowed value"):
        outputimage = create_image(image, lut_list, 3, 0, 50, 1000.0)

"""check z"""
# send in z not as integer - TypeError: expected z as integer
def test_z_not_integer():
    image = tifffile.imread(".\\backend\\tests\\test_images\\test_image_8bit.tif").transpose((1,0,2,3))
    loaded_luts = import_luts()

    lut_list = {0:loaded_luts["Magenta hot"],
                1:loaded_luts["Cyan hot"],
                2:loaded_luts["Yellow"]}
    with pytest.raises(TypeError, match = "expected z as integer"):
        outputimage = create_image(image, lut_list, "3", 0, 50, 1.0)
# send in z outside image z dimension size - ValueError: z outside image dimensions
def test_z_outside_image():
    image = tifffile.imread(".\\backend\\tests\\test_images\\test_image_8bit.tif").transpose((1,0,2,3))
    loaded_luts = import_luts()

    lut_list = {0:loaded_luts["Magenta hot"],
                1:loaded_luts["Cyan hot"],
                2:loaded_luts["Yellow"]}
    with pytest.raises(ValueError, match = "z outside image dimensions"):
        outputimage = create_image(image, lut_list, -5, 0, 50, 1.0)
"""create_image"""
# send in correct parameters  - output image as expected

def test_create_image():
    imported_image = tifffile.imread(".\\backend\\tests\\test_images\\test_image_8bit.tif").transpose((1,0,2,3))
    loaded_luts = import_luts()
    print(loaded_luts.keys())
    print(imported_image.shape)
    lut_list = {0:loaded_luts["Magenta hot"],
                1:loaded_luts["Cyan hot"],
                2:loaded_luts["Yellow"]}

    outputimage = create_image(imported_image, lut_list, 3, 0, 0, 1.0)

    img = Image.fromarray(outputimage, mode='RGB')
    img.save("output.png")

    assert outputimage.shape == (512,512,3)