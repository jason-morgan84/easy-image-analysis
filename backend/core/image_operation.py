import numpy as np
from core.constants import DataType
from core.shape import Shape
from core.parameter import Parameter
from core.image import Image

class ImageOperation:
    def __init__(self, name, category, excecute, version, docs, alerts, inputs = {}, outputs = {}, parameters = {}, ):
        self.name = name
        self.category = category
        self.excecute = excecute
        self.version = version
        self.docs = docs
        self.alerts = alerts 
        self.inputs = inputs
        self.outputs = outputs
        self.parameters = parameters

    @property
    def inputs(self):
        return self._inputs

    @inputs.setter
    def inputs(self,inp):
        # check input is a dictionary
        if not isinstance(inp,dict):
            raise TypeError(f"Inputs should be passed as a dictionary of Parameter class, not {type(item)}")
        # loop through each item in dictionary
        for key, item in inp.items():
            dtype = item["dtype"]
            value = item["value"]
            shape = item["shape"]
            
            # First check dictionary value is of Parameter class
            if not isinstance(item, Parameter):
                raise TypeError(f"For input {key}, inputs should be passed using the Parameter class, not {type(item)}")
             

            # Following tests depend on whether the parameter is an image or not
            # if its an image, need to check image shape matches shape arguement
            # if its an image, need to check image type matches type arguement
            # it its not an image, don't care about shape
            # if its not an image, still need to check value type matches type arguement
            
            if dtype in DataType.image_types:
                # if its a member of image_types, then the the actual value should be Image class
                if not isinstance(value,Image):
                    raise TypeError(f"For input {key}, image inputs should be of Image class, not {type(value)}")

                # next, check data type of image.array and image.dtype arguement match input.dtype
                if not isinstance(value.array, dtype):
                    raise ValueError(f"For input {key}, image inputs type {type(value.array)} does not match dtype arguement {dtype}")
                if value.array_dtype != dtype:
                    raise ValueError(f"For input {key}, image.dtype {value.array_dtype} does not match dtype arguement {dtype}")

                # next, check shape is a tuple/list, has size between Shape.min_image_dimensions and Shape.max_image_dimensions and is filled with integers
                if not isinstance(shape,tuple) and not isinstance(shape,list):
                    raise TypeError(f"For input {key}, Shape should be a tuple or list, not {type(shape)}")

                if len(shape) > Shape.max_image_dimensions or len(shape) < Shape.min_image_dimensions:
                    raise ValueError(f"For input {key}, Shape should be in the range {Shape.min_image_dimensions}-{Shape.max_image_dimensions} (defined in Shape.py), not {len(shape)}")

                if not isinstance(shape[0], int) and not isinstance(shape[0],np.integer):
                    raise TypeError(f"Shape should be integers, not {type(shape[0])}")

            elif dtype in DataType.value_types:
                # for non-image values, just need to check that the dtype arguement matches the actual type of the value
                if not isinstance(value,dtype):
                    raise TypeError(f"For input {key}, value type {type(value)} does not match dtype {dtype}")

            # if the data passed in is not from DataType, raise a type error
            else:
                raise TypeError(f"For input {key}, dtype should be a member of DataType classes, not {dtype}")

            #TODO repeat setter for outputs (pretty much identical) and parameters. Parameters cannot pass in images, so simpler process
    @property
    def outputs(self):
        return self._outputs

    @outputs.setter
    def outputs(self,out):
        for key, item in out.items():
            if not isinstance(item, Parameter):
                raise TypeError(f"For output {key}, output should be passed using the Parameter class, not {type(item)}")
            if item["value"] not in DataType.image_types and item["value"] not in DataType.value_types:
                raise TypeError(f"For output {key}, values should be passed using DataType classes, not {type(item["value"])}")
            if type(item["value"]) != item["dtype"]:
                raise TypeError(f"For output {key}, value data type ({type(item["value"])}) does not match defined data type {item["dtype"]}")
