import py
from core.frontend_operations import create_image, import_luts
import tifffile
from PIL import Image
import numpy as np

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