# ImageOperations

## Introduction

This software provides a graph-based UI for testing and developing image analysis pipelines. These pipelines are made up of interconnected Nodes, each of which applies a specific image analysis function to the inputted image.

These image analysis functions are described by the ImageOperation class. These define the function themselves, their required input(s) and expected format, their output(s) and expected format and documentation to identify the function and explain its usage to the user.

In order to allow expandability, the majority of ImageOperations are not hardcoded, but are inported from .py files in the image_operations directory.

## ImageOperation attributes

The first three attributes are set by the code:

* id - This is the id used within the code and is based on the file name, e.g. "guassian_blur"
* category - This is the category the function falls into and is based on its folder location, e.g. "thresholding" for files in .\image_operations\thresholding
* version - This is defined based on the file version, described in more detail below.

Other attributes are defined when writing the ImageOperation
* name - This is the user facing name for the function, e.g. "Gaussian blur"
* docs - documentation explaining the function, how it works, the required inputs and the given outputs
* alerts - any alerts given to the user prior to using the function. For example, an alert may warn a user that carrying out background subtraction on a high resolution image with a large resolution is likely to take a long time.
* input_image_metadata - This provides a dictionary of all expected input, and their format. This is absolutely required for an ImageOperation to be imported and is described in more detail below.
* output_image_metadata - A similar dictionary of format(s) of output image(s).
* input_parameter_metadata - A dictionary of non-image inputs, for example, for a gaussian blur function this would include "sigma". This can be defined as an input through the graph or via the UI.
* output_parameter_metadata - A dictionary of non-image outputs, for example, a threshold value.

The final attributes are set during execution. They contain the actual image pixel arrays or parameter values. They are created as a dictionary with the same keys as the respective metadata.

* input_parameter
* output_parameter
* input_image
* output_image


## ImageOperation Checking

ImageOperations are checked to ensure their compatibilty at multiple points in program execution. This process varies slightly between imported ImageOperations and hard coded ImageOperations. There are two key requirements for imported ImageOperations: 

1. ImageOperations exist to process images. As such, they're expected to define at least one input image and provide some kind of output.

2. As imported code, for security reasons ImageOperations are limited to what modules they can import (hardcoded as permitted_imports in the ImageOperationDirectory class).

The exception to these two rules are modules to load and save images, which by definition by lack input images/outputs and may require modules that are not in the permitted imports list (e.g. sys). These modules are not imported, but are hardcoded in io_image_operations.py.

Because of this, requirements 1 and 2 above are checked at the import stage, rather than by the ImageOperation class.

### ImageOperation class requirements

ImageOperation is described in image_operation.py and has the following requirements:

1. Where metadata exists, it must be a dictionary.
2. Where metadata exists, it must be a dictionary of ImageMetadata or ParameterMetadata class.
3. Data cannot be set (either as an input to the ImageOperation or as an output following code execution) if relevant metadata doesn't exist to describe it.
4. When code is run, it must not alter the input values.

### ImageOperationDirectory class requirements

ImageOperationDirectory (defined in image_operation_directory.py) holds a dictionary of all ImageOperations. Hardcoded ImageOperations are directly added to this dictionary. ImageOperations that are imported from a file must pass the following tests:
1. They must describe the version of the backend API they were written for (described in more detail below).
2. They must not have imports that aren't in the permitted import list.
3. They must have at least one image input defined in input_image_metadata.
4. They must have at least one output defined (either in output_image_metadata or output_parameter_metadata).
5. When executed with randomised sample data matching the input metadata, they must provide an output that matches the format of the output metadata.



![System Class Structure](/docs/image_operation_checking.svg)

## Writing ImageOperations

A sample ImageOperation file can be found in docs/sample_image_operation.py. The required elements of an ImageOperation are required below.

### Imports

The following imports are required for an ImageOperation to function:
```
from core.image_operation import ImageOperation
from core.metadata import ImageMetadata, ParameterMetadata
from core.shape import Shape
from core.constants import DataPolicy
```
They include all the classes to create an ImageOperation and describe its inputs and outputs.

Beyond these, any standard image analysis and numerical libraries needed should be imported here (eg, numpy, math, pillow, sci-kit image etc). Any library needed that isn't in the permitted_imports list in image_operation_directory.py may need to be added. 

### Version

Following the imports, the version of the code the ImageOperation was written for should be:

```
version = "1.0.2"
```
The version should be written in major.minor.patch format. This is used when importing files to keep backward compatibility between versions. If the version is not present or not in the correct format, the file won't be imported. Note that version is also a class attribute in ImageOperation. This will be overwritten with the file version.

### Metadata

The metadata describes the expected format of any input or output images or parameters (non-image inputs/outputs). There are four metadata attributes:

* input_image_metadata - describes input images, this is required.
* input_parameter_metadata - includes non-image inputs, including via the UI
* output_image_metadata - describes output images
* output_parameter_metadata - describes non-image outputs

Metadata must be described following these rules:
1. If no inputs/outputs of that format are expected, metadata should be None.
2. If inputs/outputs are expected, the relevant metadata must exist in a dictionary.
3. The metadata dictionary key **must** match the name of the input/output.
4. If a metadata key is created for an output, data matching that key **must** be created by the function.

Functions that break these rules are likely to fail import testing and not be imported.

Within metadata dictionaries, values should be supplied using either the ImageMetadata or ParameterMetadata classes.

The following example shows metadata definitions for an ImageOperation that inputs an image and outputs a parameter:

```
            input_image_metadata={ "input":  ImageMetadata(dtype=DataPolicy.ImageInt,
                                                  image_shape_constraints=Shape(c=-1, z=-1, y=-1, x=-1),
                                                  image_map=Shape(c=0, z=1, y=2, x=3))},
            input_parameter_metadata=None
            output_image_metadata=None
            output_parameter_metadata={ "output": ParameterMetadata(dtype=DataPolicy.ValueInt)}
```
#### ImageMetadata

The ImageMetadata class describes the metadata for inputted and outputted images, and must be used as the values for input_image_metadata and output_image_metadata dictionaries. 

It is defined in metadata.py and contains the following attributes:
* dtype - this defines the data policy describing the format required for the input image or the format the output image is delivered in. Described in more detail in the type section below.
* image_shape_constraints - this defines the dimensions required of the input image, using the Shape class (described in more detail below). For example, if a function required a single channel input image, it would define c=1. Where the function is indifferent to the size of a dimension, it should set dimension=-1. Dimensions should never be set to 0.
* image_map - this defines the order of the image dimensions in the pixel array and is given as a Shape class (e.g Shape(c=0, z=1, y=2, x=3)). It must be correct for data to flow properly through the graph, for example, if the ImageOperation of one node provides an image as ZCYX and the ImageOperation for the next node requests CZYX, the pixel array must be transposed before being sent to the second node.

#### ParameterMetadata

The ParameterMetadata class describes the metadata for non-image inputs and outputs, including inputs from the UI. To get inputs from the UI, it includes a number of attributes to define how that data should be gathered from the user. This will then be provided to the ImageOperation when activated. When writing an ImageOperation with user input, it is therefore not necessary to provide any UI coding.

ParameterMetadata must be used as the values for input_parameter_metadata and output_parameter_metadata dictionaries. 

It is defined in metadata.py and contains the following attributes:
* dtype - defines the data policy describing the format of the data. This is required.
* shape - if dtype defines an array, this gives the expected shape of that array as a list/tuple/np.ndarray.
* user_input - a boolean flag. If set to true, data will be gathered from the user
* ui_element - the type of UI element to be used to get this data (eg, text box, drop down box etc). This is described in more detail in the UI input section below. It is required if user_input is set to True.
* ui_element_options - any other options associated with the UI element. This varies per element and may include min/max slider values, drop-down box options etc. It is described in more detail in the UI input section below.

#### Type policies

To ensure data is delivered to ImageOperations in a predictable format, all ImageMetadata and ParameterMetadata members must provide a dtype. This defines a data policy describing how that particular input should be delivered and how the ImageOperation will provide an output.

Data policies are divided into image policies and array policies, which expect a multi-dimensional nd.array, and value policies which expect a scalar value.

Each policy defines a numpy format. For policies defining an array, data should be an nd.array with elements of the given numpy format. For policies defining a scalar value, data should be of the given numpy format (not part of a collection or nd.array). If the output provided by the ImageOperation does not match what's expected based on the output metadata, the ImageOperation output will not be accepted and it will likely fail import checks.

It may also define minimum and maximum values. If data is provided outside those values, this will not be coerced into that range but will assume a failure in the ImageOperation code and log an error.

Where possible, outputs from one node will be converted to match the expected input of the next node. To aid in this, each policy defines other policies it can be converted into silently, and policies it can be converted into with a warning. For example, an integer image can be converted into a float image silently. A binary image can be converted into a float image with a warning ("This will effectively unbinarise your image"). An integer image cannot be automatically converted into a binary image, this requires a thresholding function.

##### Image Policies

ImageInt - expects a uint8 value between 0 and 255 exclusive. Can be converted into ImageFloat.
ImageFloat - expects a float64 value between 0 and 1 exclusive. Can be converted into ImageInt.
ImageBinary - expects a uint8 value of either 0 or 1. Can be converted into ImageFloat or ImageInt with a warning.

##### Array Policies

ArrayInt - expects a np.ndarray of uint8 values. Can be converted to ArrayFloat.
ArrayFloat - expects a np.ndarray of float64 values. Can be converted to ArrayFloat.

##### Value Policies

ValueInt - expects a uint8 value. Can be converted to ValueFloat.
ValueFloat - expects a float64 value. Can be converted to ValueInt.

#### Shape

Shape class is used when describing images with 4 defined dimensions:

* channel (c)
* position in z (z)
* position in y (y)
* position in x (x)

These dimensions are defined in Shape.dimensions and all 4 must be present when describing a shape. Currently, all images must have all 4 dimensions. If you're not interested in a dimension, it should still be present in input and output images with size=1.

Defining a Shape class member with missing dimensions or other dimensions will result in an error. As it stands, F/T dimensions describing frames or time are not implemented or planned to be implemented.

### Data

Input data will be provided as a dictionary of values defined by the metadata. For example:

* Your input_image_metadata includes a value with key "input_image_1". Your input will be found in input_image["input_image_1"] and will match the type/shape definitions in your metadata.
* Your input_parameter_metadata includes two values, one with key "min_region_size" and one with key "min_region_intensity". Your input will be found in input_parameter["min_region_size"] and input_parameter["min_region_intensity"] in the format described in your metadata.

Similarly, output data should be provided in a similar format:
* If your ImageOperation defines metadata for an output image with key "thresholded_image" then your code, when executed, must set output_image["thresholded_image"] to an image that matches the description in the metadata.
* If your ImageOperation defines metadata for two output parameters, "total_intensity" and "area", then you must set both output_parameter["total_intensity"] and output_parameter["area"] to values that match their descriptions in the metadata.

If an output is described in the metadata but no value is set for a key that matches the metadata, the ImageOperation will fail import tests.

Input images should be expected as 4D arrays and will meet the constraints described in your metadata. Output images are also expected as 4D arrays. Other image shapes will result in an error. If your ImageOperation is indifferent to the shape of the input/output images the input and output metadata should set image_shape_constraints to -1 for those dimensions. If image_shape_constraints is set to a given value, inputs that are not of that shape will not be sent to the ImageOperation and outputs that are not of that shape will result in an error.

### The function

The code to be executed should be defined in the execute function within the ImageOperation.

The code will be run on import given sample data matching that defined in the metadata. Any exceptions will result in the ImageOperation not being imported.

In general, as long as the code only uses the permitted imports, doesn't generate an exception, provides some output and that output matches what is defined in the metadata, the software is indifferent to the code thats executed by the ImageOperation. 

## Testing ImageOperations


WHERE SHOULD THE FUNCTION BE SAVED?

New ImageOperations can be tested by running .... in terminal.

This test function will test the ImageOperation on sample biological data transformed to match input_image_metadata. To use the test function if input parameters are required, a dictionary of test inputs should be added to the ImageOperation as instance variable test_input_parameters.

The test function will carry out the same checks made during ImageOperation import by ImageOperationDirectory. A text file will be provided ... describing which of these tests were passed and which were failed.

These tests a randomised data set is provided to the ImageOperation to tests its function and outputs as well as real sample image adjust to match your input image metadata. The outputted image can be found at ......


## ImageOperation failure

Where ImageOperations fail consistently, they are likely to fail import testing and never be imported. ImageOperations that fail import testing are logged in the log file.

If an ImageOperation fails on a particular run, that will be reported to the user and logged in the log file. In general, exception messages are chained upwards until they are logged by the WorkFlow, so check the log to see exactly what went wrong.


