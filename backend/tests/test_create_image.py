import py
from core.frontend_operations import create_image, import_luts
import tifffile
from PIL import Image
import numpy as np

"""check input image """
# send in non np.ndarray - TypeError: expected input_image as np.ndarray 
# send in np.ndarray not of np.uint8 - TypeError: expected input_image as np.ndarray of np.uint8 
"""check luts"""
# send in luts not as dictionary - TypeError: expected luts as dictionary 
# send in luts with duplicate keys - ValueError: luts dictionary contains duplicate keys 
# send in luts with non-integer key - TypeError: expected luts keys as integers 
# send in luts with key that doesn't match channel - ValueError: luts dictionary contains out of range key 
# send in luts with non-dictionary value - TypeError: expected luts values as np.ndarray 
# send in luts with value that isn't of correct shape - ValueError: expected luts values as np.ndarray of shape (256,3)
"""check centres"""
# send in centre_y not as integer  - TypeError: expected centre_y as integer
# send in centre_y less than 0 or higher than image size  - ValueError: centre_y out of range for image sizer
# csend in centre_x not as integer  - TypeError: expected centre_x as integer
# send in centre_x less than 0 or higher than image size  - ValueError: centre_x out of range for image sizer
"""check zoom"""
# send in zoom not as float  - TypeError: expected zoom as float
# end in zoom less than zoom_min  - ValueError: zoom less than minimum allowed value
# send in zoom greater than zoom_max  - ValueError: zoom greater than maximum allowed value

"""check z"""
# send in z not as integer - TypeError: expected z as integer
# send in z outside image z dimension size - ValueError: z outside image dimensions
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
    outputimage = outputimage
    print("SHAPE:", outputimage.shape)
    img = Image.fromarray(outputimage, mode='RGB')
    img.save("output.png")

    assert outputimage.shape == (512,512,3)