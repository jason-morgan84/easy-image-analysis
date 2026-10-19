assume imported imageoperations have input image and at least one output - this is checked when imported, but not required for running an ImageOperation or attaching it to a Node.

This is because hardcoded I/O ImageOperations (in io_image_operations.py for example) do not necessarily have image inputs or outputs.

In all other cases, ImageOperations should have at least one image as an input. This is a design choice to stay towards image analysis, and not data analysis. Likewise, all ImageOperations should have an output of some form (image or data). Where it is absolutely necessary to break this convension, consider hard coding the ImageOperation rather than importing it.