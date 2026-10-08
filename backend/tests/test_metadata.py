import pytest
import numpy as np
from core.shape import Shape
from core.constants import DataType
from core.metadata import ImageMetadata, ParameterMetadata

"""Test ImageMetadata Class"""
@pytest.mark.parametrize("dtype, image_shape_constraints, image_map, message", [
    # Supply dtype as not member of DataTypes.image_types
    (np.uint8, Shape(c=-1,z=-1,y=-1,x=-1), Shape(c=0,z=1,y=2,x=3),"expected type from DataType.image_type"),
    # Supply image_shape_constraints not as Shape class
    (DataType.ImageInt, [-1,-1,-1,-1], Shape(c=0,z=1,y=2,x=3),"for ImageMetadata class, expected image_shape_constraints to be of class Shape"),
    # Supply image_map not as Shape class
    (DataType.ImageInt, Shape(c = -1, z = -1, y = -1, x = -1), (0,1,2,3),"for ImageMetadata class, expected image_map to be of class Shape")
    ])
def test_ImageMetadata(dtype, image_shape_constraints, image_map, message):

    with pytest.raises(TypeError, match = message):
        ImageMetadata(dtype = dtype, 
                    image_shape_constraints = image_shape_constraints, 
                    image_map = image_map)

"""Test ParameterParcel Class"""
# test valid inputs
@pytest.mark.parametrize("dtype, shape, message", [
    # Supply dtype as not member of DataTypes.image_types
    (np.uint8, None, "expected type from DataType.value_type or DataType.array_type"),
    (DataType.ImageInt, None, "expected type from DataType.value_type or DataType.array_type")
])
def test_parameter_metadata(dtype, shape, message):

    with pytest.raises(TypeError, match = message):
        ParameterMetadata(dtype = dtype, 
                    shape = shape)

# test user_input flag as not boolean
def test_ParameterParcel_user_input_flag_boolean():
    with pytest.raises(TypeError, match = "user_input flag expected to be boolean, not "):
        ParameterMetadata(dtype = DataType.ValueInt, 
                    user_input = 4)

# test user_input true without user_interface element
def test_ParameterParcel_user_input_no_ui_element():
    with pytest.raises(ValueError, match = "defined UI element required where user_input flag is True"):
        ParameterMetadata(dtype = DataType.ValueInt,  
                    user_input = True)

