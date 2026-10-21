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

1. Where metadata exists, it must be a dictionary.
2. Where metadata exists, it must be a dictionary of ImageMetadata or ParameterMetadata class.
3. Data cannot be set (either as an input to the ImageOperation or as an output following code execution) if relevant metadata doesn't exist to describe it.
4. When code is run, it must not alter the input values.

### ImageOperationDirectory class requirements

ImageOperationDirectory holds a dictionary of all ImageOperations. Hardcoded ImageOperations are directly added to this dictionary. ImageOperations that are imported from a file must pass the following tests:
1. They must describe the version of the backend API they were written for (described in more detail below).
2. They must not have imports that aren't in the permitted import list.
3. They must have at least one image input defined in input_image_metadata.
4. They must have at least one output defined (either in output_image_metadata or output_parameter_metadata).
5. When executed with randomised sample data matching the input metadata, they must provide an output that matches the format of the output metadata.



![System Class Structure](/docs/image_operation_checking.svg)

### Imported ImageOperations

Imported ImageOperations contain all of the 

### Hardcoded ImageOperations


## Writing ImageOperations

### Verison

### Metadata

#### Type

#### Shape

## Testing ImageOperations

assume imported imageoperations have input image and at least one output - this is checked when imported, but not required for running an ImageOperation or attaching it to a Node.

This is because hardcoded I/O ImageOperations (in io_image_operations.py for example) do not necessarily have image inputs or outputs.

In all other cases, ImageOperations should have at least one image as an input. This is a design choice to stay towards image analysis, and not data analysis. Likewise, all ImageOperations should have an output of some form (image or data). Where it is absolutely necessary to break this convension, consider hard coding the ImageOperation rather than importing it.


