import numpy as np
import os
from PIL import Image
from core.error_handling import log

lut_folder_location = ".\\frontend\\luts"
image_frame_x = 512
image_frame_y = 512

def import_luts(logger = []):
    lut_list = {}
    # get all files in lut folder
    path = lut_folder_location
    files = os.listdir(path)

    # loop through files
    for file in files:
        name, extension = os.path.splitext(file)
        # check file is a png
        if extension != ".png":
            log(logger,ImportError,f"lut file not imported as not .png: '{file}'",None,"import_luts",str(file))
            continue

        # open file
        try:
            import_lut = Image.open(os.path.join(path, file))
        except Exception as e:
            log(logger,ImportError,f"lut file could not be opened '{file}': {e}",None,"import_luts",str(file))
            continue

        print(f"\n{file}: {import_lut.mode}")
        if import_lut.mode != 'RGB':
            log(logger,ImportError,f"lut file not 8-bit RGB image: '{file}'",None,"import_luts",str(file))
            continue

        # convert to np.array
        new_lut = np.array(import_lut)
        # input will be shape (1,256,3), so remove fist dimension
        new_lut = np.squeeze(new_lut, axis = 0)




        # check shape is correct
        if new_lut.shape != (256, 3):
            log(logger,ImportError,f"\nlut '{file}' discarded as not correct shape: {new_lut.shape}",None,"import_luts",str(file))
            continue

        # convert file name to user-visible name by replacing _ with space and converting to sentence case
        name = name.replace("_", " ").capitalize()

        # add to lut_list dictionary
        lut_list[name] = new_lut

    return lut_list

def create_image(input_image, luts, z=0, y_centre=0, x_centre=0, zoom=1.0 ):
    # inputs:
    #   input_image: np.ndarray of np.uint in format CZYX
    #   luts: dictionary of form {channel: lut_name} where channel is an integer representing an input_image channel number and lut_name is a key from lut_lists
    #   top: for panning, y value of top of image to be generated as an int
    #   left: for panning, x value of left of image to be generated as an int
    #   zoom: how zoomed in the image is as a float


    """check input types"""
    # check input image is an np.array of np.uint8
    if not isinstance(input_image, np.ndarray):
        raise TypeError(f"expected input_image as np.ndarray, not {type(input_image)}")
    if input_image.dtype != np.uint8:
        raise TypeError(f"expected input_image as np.ndarray of np.uint8, not {input_image.dtype}")

    # get dimension sizes of input_image
    dim_c, dim_z, dim_y, dim_x = input_image.shape

    # check luts is a dictionary with integer keys, referencing channels, and np.arrays of shape (3,256) as values
    if not isinstance(luts, dict):
        raise TypeError(f"expected luts as dictionary, not {type(input_image)}")
    if len(set(luts.keys())) != len(luts.keys()):
        raise ValueError(f"luts dictionary contains duplicate keys")
    for key, value in luts.items():
        if not isinstance(key, int):
            raise TypeError(f"expected luts keys as integers, not {type(key)}")
        if key < 0 or key > dim_c:
            raise ValueError(f"luts dictionary contains out of range key: {key}") 
        if not isinstance(value, np.ndarray):
            raise TypeError(f"expected luts values as np.ndarray, not {type(value)}")
        if value.shape != (3,256):
            raise ValueError(f"expected luts values as np.ndarray of shape (3,256), not {value.shape}")

    # check top and left integers within expected range
    if not isinstance(y_centre, (int, np.integer)):
        raise TypeError(f"expected top as integer, not {type(y_centre)}")
    if y_centre < 0 or y_centre > dim_y:
        raise ValueError(f"y_centre out of range for image size")
    if not isinstance(x_centre, (int, np.integer)):
        raise TypeError(f"expected left as integer, not {type(x_centre)}")
    if x_centre < 0 or x_centre > dim_x:
        raise ValueError(f"left out of range for image size")
    
    # check zoom is a float
    if not isinstance(zoom, (float,np.floating)):
        raise TypeError(f"expected zoom as float, not {type(zoom)}")

    # reduce to required z slices
    # reduce to required cs

    # adjust viewport dimension by zoom:
    viewport_y = image_frame_y / zoom
    viewport_x = image_frame_x / zoom

    viewport = np.zeros ((len(luts), viewport_y, viewport_x), np.uint8)

    # create viewport as np.array of 0s
    # position viewport
    # if viewport is smaller than image dimension, position as close to centre point that doesn't cause buffering
    # if viewport is larger than image dimension, position as close to centre point as possible so as not to cut off any image
    # overwrite any portion of viewport that covers image

 

    
        

