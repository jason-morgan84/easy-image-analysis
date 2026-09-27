"""
Things to test before activation:
* is the node is_ready flag true?
* is the port_id in the correct format ("type.name")
* does the input key referenced by port_name exist in ImageOperation inputs?
* does the input port contain data (pixel_array and mapping for images, value for parameters)?

Things to test after activation:
* is the port_id in the correct format ("type.name")
* does the output key referenced by port_name exist in ImageOperation outputs?
* does ImageOperation output contain data (pixel_array and mapping for images, value for parameters)?

"""