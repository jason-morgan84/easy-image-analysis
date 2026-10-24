from core.io_image_operations import LoadImage, SaveImage
from core.error_handling import ExportError
import pytest
import numpy as np
"""test LoadImage"""
"""import image"""
# non-tif path - ImportError: loading of non .tif files not currently implemented
def test_load_image_non_tif_path():
    testload = LoadImage()
    testload.input_parameter = {"path":".\\backend\\tests\\test_images\\test.png",
                                "shape": "CZYX"}
    with pytest.raises(ImportError,match="loading of non .tif files not currently implemented"):
        testload.execute()

    with pytest.raises(RuntimeError,match="loading of non .tif files not currently implemented"):
        testload.run_code()

# invalid path - ImportError: failed to import image from tiff file
def test_load_image_incorrect_tif_path():
    testload = LoadImage()
    testload.input_parameter = {"path":".\\backend\\tests\\test_images\\no_file_here.tif",
                                "shape": "CZYX"}
    with pytest.raises(ImportError,match="failed to import image from tiff file"):
        testload.execute()

    with pytest.raises(RuntimeError,match="failed to import image from tiff file"):
        testload.run_code()

"""type conversion""" 
# try to import 16bit tif - ImportError: failed to convert imported image into defined dtype
def test_load_image_16bit_tif_path():
    testload = LoadImage()
    testload.input_parameter = {"path":".\\backend\\tests\\test_images\\test_image_16bit.tif",
                                "shape": "CZYX"}
    with pytest.raises(ImportError,match="failed to convert imported image into defined dtype"):
        testload.execute()

    with pytest.raises(RuntimeError,match="failed to convert imported image into defined dtype"):
        testload.run_code()


"""shape checking"""
#import with shape parameter which doesn't match number of dimensions in image - ValueError:number of dimensions in image pixel array does not match expected shape
def test_load_image_shape_wrong_length():
    testload = LoadImage()
    testload.input_parameter = {"path":".\\backend\\tests\\test_images\\test_image_8bit.tif",
                                "shape": "CYX"}
    with pytest.raises(ValueError,match="number of dimensions in image pixel array does not match expected shape"):
        testload.execute()

    with pytest.raises(RuntimeError,match="number of dimensions in image pixel array does not match expected shape"):
        testload.run_code()


#import with shape with unexpected dimension identifiers - ValueError: when loading image, shape includes unexpected dimension identifier
def test_load_image_shape_wrong_dimension_identifiers():
    testload = LoadImage()
    testload.input_parameter = {"path":".\\backend\\tests\\test_images\\test_image_8bit.tif",
                                "shape": "CFYX"}
    with pytest.raises(ValueError,match="when loading image, shape includes unexpected dimension identifier"):
        testload.execute()

    with pytest.raises(RuntimeError,match="when loading image, shape includes unexpected dimension identifier"):
        testload.run_code()

#import with shape with duplicate dimension identifiers - ValueError: when loading image, shape includes unexpected dimension identifier
def test_load_image_shape_duplicate_dimension_identifiers():
    testload = LoadImage()
    testload.input_parameter = {"path":".\\backend\\tests\\test_images\\test_image_8bit.tif",
                                "shape": "CYYX"}
    with pytest.raises(ValueError,match="when loading image, shape includes duplicated dimension identifier"):
        testload.execute()

    with pytest.raises(RuntimeError,match="when loading image, shape includes duplicated dimension identifier"):
        testload.run_code()

#import image with less than 4 dimensions - output image has 4 dimensions with missing dimensions as size 1
def test_load_image_less_than_4_dimensions():
    testload = LoadImage()
    testload.input_parameter = {"path":".\\backend\\tests\\test_images\\test_image_single.tif",
                                "shape": "YX"}
    testload.execute()

    image = testload.output_image["output"]
    assert len(image.shape) == 4

    testload.output_image = None
    testload.run_code()
    image = testload.output_image["output"]
    assert len(image.shape) == 4


#import image with dimensions not in order CZYX - output image has dimensions in order CZYX
def test_load_image_wrong_order_dimensions():
    testload = LoadImage()
    testload.input_parameter = {"path":".\\backend\\tests\\test_images\\test_image_8bit.tif",
                                "shape": "ZYCX"}

      
    testload.execute()

    """imported image dimensions are 5,3,444,331, which are declared as ZYCX
    therefore when output as CZYX, this will be 444,5,3,331"""
    image = testload.output_image["output"]
    assert len(image.shape) == 4
    assert image.shape == (444, 5, 3, 331)

    testload.output_image = None
    testload.run_code()
    image = testload.output_image["output"]
    assert len(image.shape) == 4
    assert image.shape == (444, 5, 3, 331)

"""save image"""
# import image that should work - output image matches image expectations
def test_load_image():
    testload = LoadImage()
    testload.input_parameter = {"path":".\\backend\\tests\\test_images\\test_image_8bit.tif",
                                "shape": "ZCYX"}

    testload.execute()

    """check imported image values against actual image values"""
    image = testload.output_image["output"]
    assert image[0][0][0][0] == 14
    assert image[0][1][0][0] == 16
    assert image[1][2][0][0] == 6
    assert image[1][4][25][30] == 16

    testload.output_image = None
    testload.run_code()
    image = testload.output_image["output"]
    assert image[0][0][0][0] == 14
    assert image[0][1][0][0] == 16
    assert image[1][2][0][0] == 6
    assert image[1][4][25][30] == 16

"""test SaveImage"""
"""check path """
#Non-tif save path - ExportError: saving of non .tif files not currently implemented
# non-tif path - ImportError: loading of non .tif files not currently implemented
def test_save_image_non_tif_path():
    testload = LoadImage()
    testload.input_parameter = {"path":".\\backend\\tests\\test_images\\test_image_8bit.tif",
                                "shape": "ZCYX"}

    testload.execute()

    testsave = SaveImage()
    testsave.input_parameter = {"path":".\\backend\\tests\\test_images\\test_image_8bit.png"}
    testsave.input_image = {"input": testload.output_image["output"].copy()}
    with pytest.raises(ImportError,match="saving non .tif files not currently implemented"):
        testsave.execute()

    with pytest.raises(RuntimeError,match="saving non .tif files not currently implemented"):
        testsave.run_code()

#invalid save path - ExportError: failed saving image
def test_save_image_invalid_path():
    testload = LoadImage()
    testload.input_parameter = {"path":".\\backend\\tests\\test_images\\test_image_8bit.tif",
                                "shape": "ZCYX"}

    testload.execute()

    testsave = SaveImage()
    testsave.input_parameter = {"path":"FS:\\backend\\tests\\test_images\\test_image_8bit.tif"}
    testsave.input_image = {"input": testload.output_image["output"].copy()}
    with pytest.raises(ExportError,match="failed saving image"):
        testsave.execute()
    with pytest.raises(RuntimeError,match="failed saving image"):
        testsave.run_code()

"""saving image"""
# save image with unexpected type
def test_save_image_wrong_type():
    testload = LoadImage()
    testload.input_parameter = {"path":".\\backend\\tests\\test_images\\test_image_8bit.tif",
                                "shape": "ZCYX"}

    testload.execute()

    testsave = SaveImage()
    testsave.input_parameter = {"path":".\\backend\\tests\\test_images\\test_image_8bit.tif"}
    testsave.input_image = {"input": np.float64(testload.output_image["output"].copy())}

    with pytest.raises(TypeError,match="does not pass dtype validation"):
        testsave.run_code()

# try to save valid image to valid path
def test_save_image():
    testload = LoadImage()
    testload.input_parameter = {"path":".\\backend\\tests\\test_images\\test_image_8bit.tif",
                                "shape": "ZCYX"}

    testload.execute()

    testsave = SaveImage()
    testsave.input_parameter = {"path":".\\backend\\tests\\test_images\\test_image_8bit_saved.tif"}
    testsave.input_image = {"input": testload.output_image["output"]}

    testsave.run_code()