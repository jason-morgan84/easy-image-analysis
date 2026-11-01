import numpy as np
import os
from PIL import Image
from core.error_handling import log
import cv2

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

def create_image(input_image, luts, z=0, centre_y=0, centre_x=0, zoom=1.0 ):
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
    image_size_c, image_size_z, image_size_y, image_size_x = input_image.shape

    # check luts is a dictionary with integer keys, referencing channels, and np.arrays of shape (3,256) as values
    if not isinstance(luts, dict):
        raise TypeError(f"expected luts as dictionary, not {type(input_image)}")
    if len(set(luts.keys())) != len(luts.keys()):
        raise ValueError(f"luts dictionary contains duplicate keys")
    for key, value in luts.items():
        if not isinstance(key, int):
            raise TypeError(f"expected luts keys as integers, not {type(key)}")
        if key < 0 or key > image_size_c:
            raise ValueError(f"luts dictionary contains out of range key: {key}") 
        if not isinstance(value, np.ndarray):
            raise TypeError(f"expected luts values as np.ndarray, not {type(value)}")
        if value.shape != (256,3):
            raise ValueError(f"expected luts values as np.ndarray of shape (256,3), not {value.shape}")

    # check top and left integers within expected range
    if not isinstance(centre_y, (int, np.integer)):
        raise TypeError(f"expected y_centre as integer, not {type(centre_y)}")
    if centre_y < 0 or centre_y > image_size_y:
        raise ValueError(f"y_centre out of range for image size")
    if not isinstance(centre_x, (int, np.integer)):
        raise TypeError(f"expected x_centre as integer, not {type(centre_x)}")
    if centre_x < 0 or centre_x > image_size_x:
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
    if z < 0 or z > (image_size_z - 1):
        raise ValueError(f"z outside image dimensions: {z} must be greater than 0 and less than {image_size_z - 1}")

    """shape image"""
    # reduce to required z slices
    input_image = input_image[:,z,:,:]

    # adjust viewport dimension by zoom (and adjust to avoid odd values):
    viewport_size_y = int(image_frame_y / zoom)                     
    viewport_size_y = viewport_size_y if viewport_size_y % 2 == 0 else viewport_size_y - 1
    viewport_size_x = int(image_frame_x / zoom)
    viewport_size_x = viewport_size_x if viewport_size_x % 2 == 0 else viewport_size_x - 1

    # position viewport if viewport is smaller than image dimension 
    # want to make sure viewport doesn't go past edge of the image 
    # if viewport is larger or equal to image, the image will just be centred
    viewport_actual_centre_y = centre_y
    half_viewport_size_y = viewport_size_y // 2                                        
    if viewport_size_y < image_size_y:                                                  
        if centre_y + half_viewport_size_y > image_size_y:                              
            viewport_actual_centre_y = image_size_y - half_viewport_size_y              
        elif centre_y - half_viewport_size_y < 0:
            viewport_actual_centre_y = half_viewport_size_y

    # likewise for x dimension
    viewport_actual_centre_x = centre_x
    half_viewport_size_x = viewport_size_x // 2
    if viewport_size_x < image_size_x:
        if centre_x + half_viewport_size_x > image_size_x:
            viewport_actual_centre_x = image_size_x - half_viewport_size_x
        elif centre_x - half_viewport_size_x < 0:
            viewport_actual_centre_x = half_viewport_size_x
   
    # calculate region of image to be extracted
    # if y dimension for viewport is bigger than image, get whole image then pad
    # extracted rgb image size limited to size of input image
    if viewport_size_y >= image_size_y:                                         
        start_y = 0
        end_y = image_size_y
        rgb_size_y = image_size_y
        y_pad = (viewport_size_y - image_size_y)//2
    # if y dimension for viewport is smaller than image, get image on either side of viewport centre and don't pad
    # extracted rgb image size matches size of viewport
    elif viewport_size_y < image_size_y:
        start_y = viewport_actual_centre_y - half_viewport_size_y               
        end_y = start_y + viewport_size_y                                       
        rgb_size_y = end_y - start_y                                            
        y_pad = 0

    # likewise for x dimension
    if viewport_size_x >= image_size_x:
        start_x = 0
        end_x = image_size_x
        rgb_size_x = image_size_x
        x_pad = (viewport_size_x - image_size_x) // 2
    elif viewport_size_x < image_size_x:
        start_x = viewport_actual_centre_x - half_viewport_size_x
        end_x = start_x + viewport_size_x
        rgb_size_x = end_x - start_x
        x_pad = 0

    # create np.array for extraction
    # created as uint16 to avoid issues with values over 255
    rgb_image = np.zeros((rgb_size_y, rgb_size_x, 3), np.uint16)

    # loop through each channel and lut
    for channel, lut in luts.items():
        # get lut values for region of input image to be grabbed (as uint16 to avoid issues with values over 255)
        lut_mapped = lut[input_image[channel, start_y:end_y, start_x:end_x]].astype(np.uint16)
        # add each channel lut_map to rgb image and clip to 255
        rgb_image = np.clip(rgb_image + lut_mapped, 0, 255)
    # pad as required
    rgb_image = np.pad(rgb_image, pad_width=((y_pad, y_pad), (x_pad, x_pad), (0,0)))
    # return to uint8
    rgb_image = rgb_image.astype(np.uint8)

    # resize rgb_image given zoom value
    if zoom > 1:
        rgb_image = cv2.resize(rgb_image, (512, 512), interpolation=cv2.INTER_NEAREST)
    elif zoom < 1:
        rgb_image = cv2.resize(rgb_image, (512, 512), interpolation=cv2.INTER_AREA)
    else:
        rgb_image = cv2.resize(rgb_image, (512, 512))


    return rgb_image

    
        

