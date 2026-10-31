import numpy as np
import os
from PIL import Image

lut_folder_location = ".\\frontend\\luts"
image_output_dimensions = 512

def import_luts():
    lut_list = {}
    # get all files in lut folder
    path = lut_folder_location
    files = os.listdir(path)

    # loop through files
    for file in files:
        name, extension = os.path.splitext(file)
        # check file is a png
        if extension != ".png":
            print(f"\nfile discarded as not .png: '{file}'")
            continue

        # open file
        try:
            import_lut = Image.open(os.path.join(path, file))
        except Exception as e:
            print(f"\nfailed to open file '{file}': {e}")
            continue

        # convert to np.array
        new_lut = np.array(import_lut)

        # check shape is correct
        if new_lut.shape != (3,256):
            print(f"\nfile discarded as not correct shape: {new_lut.shape}")
            continue

        # convert file name to user-visible name by replacing _ with space and converting to sentence case
        name = name.replace("_", " ").capitalize()

        # add to lut_list dictionary
        lut_list["name"] = new_lut

    return lut_list

def create_image(input_image, luts, top=0, left=0, zoom=1.0 ):
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
    if not isinstance(top, (int, np.integer)):
        raise TypeError(f"expected top as integer, not {type(top)}")
    if top < 0 or top > dim_y:
        raise ValueError(f"top out of range for image size")
    if not isinstance(left, (int, np.integer)):
        raise TypeError(f"expected left as integer, not {type(top)}")
    if left < 0 or left > dim_x:
        raise ValueError(f"left out of range for image size")
    
    # check zoom is a float
    if not isinstance(zoom, (float,np.floating)):
        raise TypeError(f"expected zoom as float, not {type(top)}")

    # calculate zoom
    # considerations - 
    # 
    # Algorithm:
    # 1) Pad images smaller than 512 x 512 to 512 x 512 using black pixels
    # 2) Pad small dimension of rectangular images to square using black pixels
    # 3) If zoom = 1, image is presented at same scale it was made: crop any padded images larger than 512 x 512 to 512 x 512, starting from (top, left)
    # 4) if zoom > 1, image will be resized using inter_nearest: take a region starting at (top, left) measuring 512/zoom x 512/zoom and resize to 512 x 512
    # 5) if zoom < 1, image will be resized using inter_area: take a region starting at (top, left) measuring 512/zoom x 512/zoom and resize to 512 x 512
    # 6) if resulting image is smaller than 512 x 512, pad using black pixels
    # nb) panning may interact weirdly with zoom. Depending on UI implementation and feel for the user, the actual top, left values may need to be adjusted according to zoom to keep a consistent user experience.


    # when zoom = 1, image is presented at same scale it was made (so cropped or padded only)
    #                   If image is 256 x 256, it will need padding, 
    #                   If image is 1024 x 1024, only a quarter of the image will be visible
    #                  when zoom > 1, image will be resized using inter_nearest
    #                   
    #                   
    #                  when zoom < 1, image will be resized using inter_area
    #                       if resulting image < 512 x 512, pad it with black
    # if image is 512 x 512:
    #   if zoom is 1, take 512 x 512 image and convert
    #   if zoom is 0.5, use inter_area to reduce to 256 x 256 - buffer surrounding pixels with black space
    #   if zoom is 2, use inter_nearest to expand 256 x 256 pixels starting with (top, left) (defined using array splicing) to 512 x 512
    #   if zoom is n: if n > 1 use inter_nearest to expand original_width/n x original_height/n (rounding where required) starting with (top, left) to 512 x 512
    #                 if n < 1, use inter_area to reduce to original_width/n x original_height/n (rounding where required) starting with (top, left) to 512 x 512

    # if image is 1024 x 1024:
    #   if zoom is 1: use inter_area to reduce to 512 x 512
    #   if zoom is 0.5: use inter_area to reduce to 256 x 256 - buffer surrounding pixels with black space

    # if image is y x x:
    #   if zoom is 1:
    #           1) if y or x < 512: add black pixels to make 512
    #           2) if y or x > 512: use inter_area to reduce to 512 x 512 starting with (top, left)
    #   if zoom is n:
    #           1) 
                      

    
        

