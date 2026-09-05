# 1. Document Changelog

|Date		|Version	|Changes Made		|
|:--		|:--		|:--				|
|25/08/26	|0.1.0		|Initial notes on design	|
|26/08/26	|0.2.0		|Added description of project aims|
|27/08/26	|0.3.0		|Added description of DataType classes|
|28/08/26	|0.3.1		|Added description of Shape and Image classes|
|28/08/26	|0.3.2		|Added description of Parameter, ImageOperation and ImageOperation Directory classes|
|01/09/26	|0.3.3		|Added description of backend class structure|
|01/09/26	|0.3.4		|Added description of Node, Port, Connection classes|
|01/09/26	|0.3.5		|Added description of Workflow class|
|03/09/26	|0.4.0		|Added description of UI and UI diagram|
|05/09/26	|0.5.0		|Merged in test plans|
|05/09/26	|0.6.0		|Converted to markdown document|
|05/09/26   |0.7.0      |Added type and shape conversions to description of Shape|
# 2. Premise and Aims
Over the last 10 years, a lot of my research has been based on image analysis. I have developed my own workflows using one or a combination of FIJI, Python and C#. With the ease of high-definition microscopy at various levels, thorough, repeatable and robust image analysis is becoming more and more important – even with the advent of AI, there will always be a role for classical image analysis. However, getting into analysing your own images can have quite a high barrier to entry. This is exacerbated by some of the weaknesses in the image analysis tools mentioned above:
1.	It’s hard to compare the output to the input, particularly when stringing together multiple steps.
2.	It’s difficult to know what tools are out there – you might think you have complex needs when what you’re trying to do is a solved problem and can be done in a single step.
3.	Particularly when getting into coding for image analysis, it can be very difficult to get different functions to talk to one another. Frequently, the challenge is in understanding how to manipulate the image into the correct format and dimensions for a particular function. Once, you’ve done that, the actual analysis is simple.
With that in mind, I’ve got three main aims to this software:
1.	It needs to be educational by easing users into the image analysis tools that are available.
2.	It needs to be intuitive, with a simple UI where the same actions will always lead to the same effects.
3.	It needs to have a large, well-structured and well-documented list of functions. To aid this, it needs to be easily expandable.
This will be done by allowing the user to use drag-and-drop nodes and connections to draw an image analysis workflow. A pair of input/output images will allow immediate comparison between the original image and the changes at each step.
## 2.1 Educational
To be educational, it should not place unnecessary barriers to learning. This means things like conversions between data types and transposition of dimensions should be dealt with behind the scenes, EXCEPT where they are directly relevant to proper image analysis (for example, trying to do binary processes on non-binarised data).

Feedback should be immediate, so adding a new process into the workflow, or changing a parameter, will update the output image so the user can see its effect.

Image analysis processes will be categorised in such a way that the user can get some idea of what they do before trying them, and documented so that it’s easy to learn what they do and how they work.

You shouldn’t have to do something unrelated to image analysis (ie, learn to code) to analyse images. At the same time, it should provide the tools to develop the user’s ability to use code in image analysis. An end goal is to have the option to export the user’s image analysis workflow to functional, documented python code.
## 2.2 Intuitive

This largely comes down to the UI. It should be simple, with the more complex options present but not in the way, and focussed around the three main elements: the two image windows and the workflow.

It should have the capacity to deal automatically with data conversions that the user doesn’t need to see, while giving hints on how to fix conversions which are required to develop an understanding of image analysis (e.g., how to flatten a z-stack image, how to binarise an image).

## 2.3 Expandable

The ability for the software to organise the workflow should be independent of exactly which image analysis functions are included but should, within reason, work for any function.

This means new functions, with the correct formatting and using the correct classes, should be able to slot directly into the software simply by saving them into the correct folder.

Crucially, adding in a new function should not require messing with the UI or base code.

# 3. System Architecture & Class Structure

![System Class Structure](/docs/Structure.svg)

The main image analysis workflow will be made up of a series of interconnected nodes, ports and connections. 
Nodes take an input image, carry out a given ImageOperation on that image (based on the input data and any specific parameters provided by the user), and present the adjusted image.

Ports attach to nodes and provide a layer of separation between the functions manipulating the image and the Connections carrying the data between Nodes. In the future, if changes are made to how data is stored and transmitted, this should only require changes to a single Port class, not all the image analysis functions.

Connections transmit images and other parameters between nodes (via ports). They carry out type- and shape-checking on transmitted images to ensure they match what is expected by the next input port, carry out simple shape and type conversions (where required) and prompt the user to adjust the workflow where simple conversions are not sufficient to fit the image to the next node.

ImageOperations are the actual image analysis functions carried out by nodes. They can use existing image analysis libraries (such as scikit image) or custom functions. To allow easy expandability, each ImageOperation is held in its own file which are imported to an ImageOperationDirectory on startup. They also contain definitions of input/output data types and image shape.
To allow consistent data transfer through the workflow, a number of classes are used to define the structure of the data. These include custom DataTypes, and classes defining the image and its shape, and input parameters to ImageOperations. These are used to streamline user input and data transmission, but are not used in actual image analysis, where standard NumPy data types are used.

## 3.1 Interaction between backend classes and frontend UI

The UI is defined in more detail in the Frontend section, but the Backend interacts with the UI in a few main ways. Firstly, users drag-and-drop nodes based on their desired image analysis workflow.

Each node is associated with a given ImageOperation and the parameters of that operation are designed to allow the UI to automatically draw a dialog requesting the required information in a relevant format, without each new operation requiring adjustments to the UI.

They can then draw connections between the nodes. A single node has a defined number of inputs (defined by the ImageOperation) but can output to as many other nodes as required. On drawing the connection, the WorkFlow class checks that the connection can provide an image/value in the proper data type and shape. If so, the ImageOperation is carried out allowing immediate feedback in one of the two image views. If not, and the connection cannot carry out simple shape or type conversions, the user is warned of the problem. Where possible, this warning will provide hints towards available ImageOperations that could be used to fix the problems with the data (for example, carry out a Z-projection to flatten the image). 

## 3.2 Classes

### 3.2.1 DataType Classes

The aim of the data classes is to allow data to be transferred through the workflow in a reliable and predictable way. When developing image analysis functions, this should make the permissible input and output formats clear, it should allow automatic conversion between compatible formats and give clear feedback to users where formats aren't compatible. 

These data types exist purely for transferring data between nodes in the workflow: actual image manipulation within image analysis functions will be carried out using standard numpy data types. This means there's no requirement to be able to carry out calculations or comparisons with these data types.

There will be three data types for image data and two for non-image data:

ImageInt - 0 ≤ int ≤ 255
ImageFloat - 0 ≤ float ≤ 1
ImageBinary - 0 or 1
ValueInt - int
ValueFloat - float

Each Image type will have __init__, value property and value.getter functions along with conversion functions for the other two image types and the relevant standard numpy type.

The value types will have similar functions for converting between themselves.

They will all be wrapped in an Enum to help ensure type safety. Also, if data types need to be changed in the future, this will help with refactoring.

### 3.2.2 Shape class

This exists to hold data related to the shape of transmitted images. It will hold integer values for:
* c (channels)
* z (depth)
* y (height)
* x (width) 

It has __iter__ dunder to return values in the order c --> z --> y --> x

Shape will be used to hold shape related information in a number of classes and contexts:

* Image class – this will reflect which dimension of the multi-dimensional array holds which dimension of the image.
* ImageOperation class:
    1.	Constraints on input – does the operation need a specific shape (eg Z = 1 for a flat image) or accept any size for a specific dimension (in which case, -1 is used).
    2.	Effects on output – what effect an operation will have on the image shape, for example Z-projection will result in a Z of 1, while other dimensions will be left unchanged (-1).
* Node and Port classes – this will mirror the usage in ImageOperation classes
* Connection class – this may be required to reshape the image from the shape given by the input port to the shape given by the output port.

### 3.2.3 Image Class

This holds the image data. As for the data type class, it exists purely to transmit images between nodes with a clearly defined shape and data type. It contains four instance variables:

1.	Image pixel data, in a multi-dimensional array of defined size and type.
2.	Image data type, as a member of DataType.
3.	Image shape, using Shape class.
4.	Mapping from image dimensions (C, Z, Y, X) to image array dimensions (0,1,2,3) using Shape class.

It also contains functions required to:
* Convert between DataTypes
* Carry out shape changes

### 3.2.4 Parameters Class
The parameter class holds information for ImageOperations defining the required user inputs (as opposed to image/values inputted via the workflow). The aim is to allow the frontend to automatically create a dialogue box for the user to enter values, without each ImageOperation requiring its own hardcoded UI elements. 
* Name – the name of the parameter
* dtype – the data type of the parameter
* value – its value
* ui_element – the desired UI element for input (text box, drop down box, check box, slider etc)
* ui_element_options – Any other options related to that UI element (slider min/max, drop down box options etc).

### 3.2.5 ImageOperation Class/File
A key aim of this project is expandability, to allow the inclusion of new image analysis functions with no need to edit the base code. To achieve this, each image analysis function will be a separate file written as an instance of the ImageOperation class which will contain all the information required to run the function and will be imported using imagelib. The ImageOperation class will contain:
* name: name of ImageOperation
* category: logical category (“Threshold”, “Filter” etc)
* inputs: list of workflow input names
* input_types: list of workflow input data types
* input_shapes – list of workflow input shapes
* outputs – list of workflow output names
* output_types – list of workflow output data types
* output_shapes – list of workflow output shapes
* parameters – dictionary of parameter classes for input variables from frontend
* docs – documentation to explain function, effects, parameters etc.
* alerts – any warnings to user (e.g, “Background subtraction with a large radius is a very slow process”)
* version – version of software code ImageOperation was written for. This is to future proof code, so changes to base code that affect ImageOperations don’t mean all existing ImageOperations need to be rewritten. 
* execute – function with code to execute

### 3.2.6 ImageOperationDirectory Class
This class acts as a holder for a list of all ImageOperation classes, along with the code required to import them.

### 3.2.7 Node Class
The ImageOperation class defines the image analysis function to be carried out on the image. The Node class is responsible for positioning an ImageOperation in the WorkFlow – this means there can be multiple nodes containing the same ImageOperation. While the ImageOperation class is responsible purely for image analysis, the Node class is responsible for interacting with other elements of the WorkFlow. As such, it has the following instance variables:
* image_operation – the image analysis function to be run, as an ImageOperation class
* output – Image or value holding output data from the ImageOperation
* Various flags:
    - is_ready – whether the correct inputs have been connected allowing the ImageOperation to be run.
    - needs_update – whether this node needs to be (re)run, either because it hasn’t been run yet or because an upstream node has been changed.
* input_ports – a list of members of the port class defining the required inputs to the node.
* output_ports – a list of members of the port class defining the presented output(s) from the node.

### 3.2.8 Port Class

The port class acts as a buffer between a node and an ImageOperation. It has two main roles: to make sure that, in the future, changes can be made to the overall WorkFlow without impacting on the data sent to ImageOperations and to convert between data types used for transmitting data through the WorkFlow and those used for image analysis. Two lists of ports are created with each node, and ports do not exist independently of nodes. Each port has the following:

* node_id – unique identifier for connected node
* connection_id – unique identifier for connected connections
* is_input – flag for whether port is an input or output. Inputs only allow one connection, outputs allow multiple
* to_workflow – converts data types from those used in ImageOperations to those used in WorkFlow
* from_workflow – converts data types from those used in WorkFlow to those used in ImageOperations
* type – WorkFlow associated data type
* shape – WorkFlow associated image shape

### 3.2.9 Connection Class

Connections form the links between nodes and ports through which data travels through the WorkFlow. They have a defined direction, with an input and an output, and are created by the user. On their initiation, type and shape checking are carried out by the WorkFlow (explained in more detail below). If they find a simple type or shape conversion can be made, they will do so, and if not, they will prompt the user to make changes to the WorkFlow. They will be discarded if both ends of the connection are not appropriately typed/shaped. Connections only contain two instance variables:

* input_port_id
* output_port_id

### 3.2.10 WorkFlow Class

![Workflow Graph Map](/docs/Workflow%20Graph%20Map.svg)

The WorkFlow class does the bulk of the work in initiating, defining and checking the graph through which image data flows.
It contains lists of all existing nodes, connections and ports, contains functions to safely add, edit and remove new nodes, ports and connections.

On creation of new nodes, it interacts with the frontend to get node parameters.

On creation of new connections, it checks the validity of those connections and, if necessary, gives feedback to the user.
It defines the starting node in the graph, allowing it to generate upstream and downstream paths through the WorkFlow.
It contains instance variables:

* nodes – dictionary of all extant nodes by unique ID
* ports – dictionary of all extant ports by unique ID
* connections – dictionary of all connections by unique ID
* starting_node – ID of starting node

It also contains the following functions:
* get_downstream_nodes
* get_previous_node
* get_next_node
* node_create
* node_edit
* node_remove
* connection_create
* connection_edit
* connection_remove
* port_create
* port_edit
* port_remove

On creation of a new connection, it will check for structure, constraint or type violations. Where these can be fixed through image type or shape changes, it will do so, otherwise it will prompt the user to adjust the WorkFlow. 

 ## 4 Frontend and UI

![UI diagram](/docs/UI.svg)
 
1.	Input* image view
2.	Output* image view
3.	Workflow view
4.	Z-slice selector if Z-stack and mouse-over
5.	Lock the windows – if windows are locked, changes to zoom/pan on one effects the other – otherwise, can move and zoom independently.
6.	View node toggle
7.	Add connector button
8.	Node view, categorised by tabs
9.	Menu bar
10.	Channel options view toggle (allows selection of LUTs, what channels are visible etc)

*both views can be toggled to view the outputs of other nodes by clicking the node (for the output view) or shift-clicking the node (for the input view). Zoom using mouse wheel, double right clicking/left clicking. Pan by dragging and/or scroll bars. 
# 5 Development Plan
## Stage 0 - Planning
* Plan overall design.
* Plan class structure.
* Plan graph flow.
* Plan main UI elements.
* Set up project and directory structure for development and testing.
## Stage 1 - Backend
### Stage 1.1 – Backend Image Classes
* Plan unit testing for DataType, Shape and Image classes.
* Implement DataType, Shape and Image classes.
* Test DataType, Shape and Image classes.
### Stage 1.2 – Backend Image Operation Classes
* Plan unit testing for Parameters, ImageOperation and ImageOperationDirectory classes.
* Implement Parameters, ImageOperation and ImageOperationDirectory classes.
* Test Parameters, ImageOperation and ImageOperationDirectory classes.
### Stage 1.3 – Backend Workflow Sub-classes
* Plan unit testing for Port, Node and Connection classes.
* Implement Port, Node and Connection classes.
* Test Port, Node and Connection classes.
### Stage 1.4 – Backend Workflow Class
* Plan unit testing for Workflow class.
* Implement Workflow class.
* Test Workflow class.
## Stage 2 - Frontend
### Stage 2.1 – Frontend Planning
* Detailed plans for frontend from initial overview.
* Plan implementation of frontend.
# 6 Testing - Backend
## 6.1 – Backend Image Classes
### 6.1.1 DataType
**All DataTypes**
|Component  | Test  | Expected Outcome  | Undesired Outcome |
|:--        |:--    |:--                |:--                |  
|Type constraints|	Insert wrong type|	Type Error	| <ul><li>Type converted to correct type</li><li>Wrong type ignored</li></ul>|
|Value constraints |Insert out of bounds value |	Value Error |	<ul><li>Out-of-bounds value added to type</li><li>Value coerced to bounds</li></ul>
|Immutability   |   Define DataType *x* based on variable *y*, then change *y* |	Values in DataType do not change |<ul><li> Values in DataType change </li></ul>|
|Type Conversions | Member of DataType *x* converted to DataType *y* | Correctly converted with expected value | <ul><li>Not converted to expected DataType</li><li>Not converted to expected value</li></ul>|
|Type conversions | Convert to standard NumPy type | Array/values type matches that expected | <ul><li>Array/value data type does not match that expected</li></ul>|
|Type conversions|	Convert between int and float types then back again repeatedly	| Array values are consistent over time	|	<ul><li>Array values drift over time</ul></li>|

**Image DataTypes**
|Component  | Test  | Expected Outcome  | Undesired Outcome |
|:--        |:--    |:--                |:--                |  
|Matrix input| Input 4D numpy array|Array shape maintained|<ul><li>Array shape changes</li></ul>
|Type conversions|Test each conversion on array|Array elements change type correctly| <ul><li>Array elements do not change to correct type</li></ul>|
|Type conversions| Test each conversion on 4D numpy array|Array shape maintained|<ul><li>Array shape changes</ul></li>|



### 6.1.2 Shape
|Component  | Test  | Expected Outcome  | Undesired Outcome |
|:--        |:--    |:--                |:--                |  
|Type constraints	|Insert wrong type	|Type Error	| <ul><li>Type converted to correct type</li><li>Wrong type ignored</li></ul>|
|Immutability|Input values based on variable then change variable |Values in DataType do not change|<ul><li>Values change</ul></li>
|Itterability|Test iteration|Iteration returns correct values|<ul><li>Iteration returns incorrect values</ul></li>

### 6.1.3 Image
|Component  | Test  | Expected Outcome  | Undesired Outcome |
|:--        |:--    |:--                |:--                |  
|Type constraints	|Insert type	|Type Error	|<ul><li>Type converted to correct type</li><li>Wrong type ignored</li></ul>|
|Type constraints	|Insert acceptable type where array type does not match DataType	|Type Error	|<ul><li>Wrong type ignored</li></ul>|
|Type constraints	|Insert wrong type	|Type Error	|<ul><li>Type converted to correct type</li><li>Wrong type ignored</li></ul>|
|Shape constraints	|Input pixel data with different number of dimensions to image_shape|Value Error	|	<ul><li>Wrong shape ignored</li></ul>
|Shape constraints	|Input incorrect mapping (ie, shape data says z_dim = 5, but mapping associates z with an array dimension of size 3)  |	Shape Error	|<ul><li>Wrong shape ignore</li></ul>|
|Type conversions|Pixel data array shape| Same shape after type conversion | <ul><li>Different shape after type conversion</li></ul>|
|Type conversions|Pixel data array value | Expected values after type conversion | <ul><li>Wrong values after type conversion</li></ul>|
|Type conversions|Converts to correct type | Expected type after type conversion | <ul><li>Wrong type after type conversion</li></ul>|
|Shape conversions|Converts to correct shape | Expected shape after shape conversion | <ul><li>Wrong shape after shape conversion</li></ul>|
|Shape conversions|Maintains values | Expected values after type conversion  | <ul><li>Wrong values after shape conversion</ul></li>|
|Shape conversions|Maintains type |Expected type after type conversion | <ul><li>Wrong type after shape conversion</li></ul>|
|Shape conversions|Image shape variable updated to new shape | Image shape variable matches new shape | <ul><li>Image shape variable changes to incorrect values</li><li>Image shape variable doesn't change</li></ul>
|Shape conversions|Dimension mapping updated to new shape | Each image dimension maps to correct new array dimension | <ul><li>Image dimensions map to incorrect values</li><li>Image dimension map doesn't change</li></ul>

## Stage 6.2 – Backend Image Operation Classes
* Parameters
* ImageOperation
* ImageOperationDirectory




## 7 Other Notes
* Changes to image shape should always be explicit, never incidental. For example, z-projection will reduce z dimension to 1 because that’s what z projection does, but thresholding a 5 slice z-stack will output 5 thresholds, not just 1.
* Function code does not deal with type changes, checking of types, displaying images, UI input. The role of each function is purely to take its defined input, process it according to the supplied parameters, and produce an output in defined shape. As part of this role, it should include error handling to minimise/deal with possible errors (with the assumption that the input is of the required format). 
* To allow for simple additions of new functions without affecting the base code, each function will be in a separate module. Along with the code itself, this module should include other data required to integrate into the software (definitions of parameters required, input and output data types, input and output image shape) and documentation (what the function does, how it affects the image shape, how changes to parameters affect output, any other points of interest). 
* Type checking etc will be carried out by the pipeline functions, along with checking that the input and output image shapes are as expected.
* Functions can have multiple outputs, but defined inputs. For example, a z-stack could have one output getting z-projected, another getting processes slice by slice etc, but two images could not enter the same z-projection function. Some functions may require multiple inputs, eg applying a threshold will require thresholds and an image to apply thresholds to.
* Some thought is going to have to be given to how to deal with segmented images. Are segments treated as an image of size y * x with integer values defining segment locations? Is each segment treated like its own sub-image (like channels or z-slices)? Is a segmented image treated as the original image with an added layer defining the segments? Leaning towards the first option, but the other options may have advantages in specific situations.
* Some type changes should be dealt with automatically (ie, int to float). Some type changes should be highlighted to user as a flaw in the workflow (ie, trying to carry out a binary process on a non-binarised image) with pointers on how to fix the issue).
* It should be possible to add new functions without programming new UI elements. The data included with a function must be sufficient to automatically generate a UI element for the user to enter the required parameters.
* If its educational, it needs documentation. Consider whether this should be included as a string within any new function or as a separate file.
* The UI should be unintimidating. Consider what is necessary to see (input image, output image for comparison, channel and slice controls, current workflow diagram) and what can be hidden except when needed (LUTs, adding functions, changing function parameters, defining channel image parameters (channel names etc)).
* One of the challenges of image analysis I would like to simplify here is making sure an input image to a function is in the right format. Transposition of shape (eg, 3*1024*1024 image to 1024*1024*3 image) and data type (int to float) will be handled automatically. The user will be responsible for making sure a function that requires a 1*1024*1024 image doesn’t get sent a 3*5*1024*1024 image. For this to be intuitive, each function must have a clearly defined and invariable effect on image shape (eg, z-projection will reduce Z to 1. Isolating a channel will reduce channels to 1 or conversely, z-projection won’t affect channels so channels in = channels out). This allows the user to clearly see what effect each function has on the shape of the image, and also allows the software to give pointers (ie, if the user is trying to squeeze a 3 * 1024 * 1024 image into a function that requires a 1 * 1024 * 1024 image, or an integer image into a function that requires a binarized input, highlight potential functions that can be used to fit the image to the required shape).
* Implement a “pause updates” button – if the node graph gets big, make it possible to update multiple nodes then update all the images, rather than doing it repeatedly.

### 7.1 Class design notes
* Dimension class:
o	In images, need to know which dimension of the np.array holds C or Z.
o	Therefore image_shape class has c_dim, z_dim, y_dim, x_dim
o	Image class itself needs to be able to iterate through c, iterate through z, iterate through y and iterate through x.
o	The images returned form these iterations need their own image_shape class (i.e, an image iterated through z slices will have an image_shape class with z = -1 - so can then iterate through channels and so on.
o	The output from a function will be an image, this will have its own image_shape class so that role of a function is dealt with here.
o	The constraints on a node will also use this class. Node inputs can be "I need 1 channel, I don't care about x, I don't care about Y, I don't care about z" - this can fit into image_shape class as C = 1, y = x = z = -1.
o	This will also fit for outputs, given currently anticipated effects that a function will have. Either output dimensions are the same or they are reduced to 1. So outputs could be "-1" for no change or "1" for changed to 1, "2" to changed to 2. There’s a slight possibility of needing to use strings for other operations “-3” or “/6” etc, at which point this class may need rethinking.
* Workflow class:
o	Plans for defining graph topology of the workflow are to match the way they would be added in the UI. First, a node (e.g., node 2) would be dragged into the workflow; this would add the node to the workflow class as a workflow element, but with no input or output connections specified. Next, the user would connect the node to the preceding node (node 1). At this point a function would be called within the workflow class to check what type conversions might be needed (in pseudo code, node2 input = int(node1 float output)) or whether there were larger problems with the input to node 2 that might need the user to add in intervening nodes to further process the data. If the function is satisfied that the connection between node 1 and node 2 is functional, the relevant inputs and outputs are added to the two node elements.
o	Key thing is that these checks need to be made when adding the connection as the image processing will update once the software is satisfied that the connection is valid. As such, there’s a few checks to make.



### 7.2 Node design notes
* Z-projection
* Select channel(s)
* Get threshold value
* Apply threshold value
* Gaussian blur
* Median blur
* Top hat filter
* Binary operations (erode, dilate, open, close, fill holes)
* Logical operations (and, or, etc)
* Measurements
* Compare intensities
* Edge detection
* Segmentation
* Watershedding

