import numpy as np
import os
from PIL import Image
from core.error_handling import log

lut_folder_location = ".\\frontend\\luts"
image_frame_x = 512
image_frame_y = 512
zoom_min = 0.1
zoom_max = 10

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
        raise TypeError(f"expected y_centre as integer, not {type(y_centre)}")
    if y_centre < 0 or y_centre > dim_y:
        raise ValueError(f"y_centre out of range for image size")
    if not isinstance(x_centre, (int, np.integer)):
        raise TypeError(f"expected x_centre as integer, not {type(x_centre)}")
    if x_centre < 0 or x_centre > dim_x:
        raise ValueError(f"x_centre out of range for image size")
    
    # check zoom is a float within min, max zoom values and is not < 0
    if not isinstance(zoom, (float,np.floating)):
        raise TypeError(f"expected zoom as float, not {type(zoom)}")
    if zoom <= 0:
        raise ValueError(f"zoom cannot be 0 or less, got {zoom}")
    if zoom < zoom_min:
        raise ValueError(f"zoom less than minimum allowed value: {zoom} < {zoom_min}")
    if zoom > zoom_max:
        raise ValueError(f"zoom greater than maximum allowed value: {zoom} > {zoom_max}")

    # check z is an integer and within dimensions of image
    if not isinstance(z, (int, np.integer)):
        raise TypeError(f"expected z as integer, not {type(z)}")
    if z < 0 or z > (dim_z - 1):
        raise ValueError(f"z outside image dimensions: {z} must be greater than 0 and less than {dim_z - 1}")

    # reduce to required z slices
    input_image = input_image[:,z:z,:,:]

    # reduce to required cs
    desired_channels = luts.keys()
    input_image = input_image[desired_channels,:,:,:]

    # adjust viewport dimension by zoom:
    viewport_y = int(image_frame_y / zoom)
    viewport_x = int(image_frame_x / zoom)

    # create viewport as np.array of 0s
    viewport = np.zeros ((3, viewport_y, viewport_x), np.uint8)

    # position viewport
    # (note, viewport centre is already constrained to within image dimensions)
    # if viewport is smaller than image dimension, position as close to desired point that doesn't cause buffering
    actual_y_centre = y_centre
    half_y_viewport = viewport_y // 2
    if viewport_y <= dim_y:
        if y_centre + half_y_viewport > dim_y:
            actual_y_centre = dim_y - half_y_viewport
        elif y_centre - half_y_viewport < 0:
            actual_y_centre = half_y_viewport
    # if viewport is larger than image dimension, position as close to centre point as possible so as not to cut off any image
    elif viewport_y > dim_y:
        actual_y_centre = dim_y // 2

    # likewise for x dimension
    actual_x_centre = x_centre
    half_x_viewport = viewport_x // 2
    if viewport_x <= dim_x:
        if x_centre + half_x_viewport > dim_x:
            actual_x_centre = dim_x - half_x_viewport
        elif x_centre - half_x_viewport < 0:
            actual_x_centre = half_x_viewport
    elif viewport_x > dim_x:
        actual_x_centre = dim_x // 2
    
    # overwrite any portion of viewport that covers image
    processed_image = input_image[:,:,actual_y_centre - half_y_viewport : actual_y_centre + half_y_viewport, actual_x_centre - half_x_viewport : actual_x_centre + half_x_viewport]

    # create 3 channel array of 0s as RGB image
    # create image by looping through channels and adding LUT values for each pixel to image
 

    
        

