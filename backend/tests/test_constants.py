from core.constants import DataType
from core.type import ImageInt, ImageFloat, ImageBinary, ValueInt, ValueFloat
import pytest
import numpy as np

def test_enum():

    # test all expected data types are present in Enm
    expected_types = {
        "ImageInt",
        "ImageFloat",
        "ImageBinary",
        "ValueInt",
        "ValueFloat"
    }  

    actual_types = {member.name for member in DataType}
    assert expected_types.issubset(actual_types), f"Missing expected types from enum: {expected_types - actual_types}"

    # test there's no empty enum values
    values = [member.value for member in DataType]
    assert len(values) == len(set(values))

    # test every enum member has an associated class written
    for member in DataType:
        try:
            resolved_class = member.name
            assert resolved_class is not None
        except NotImplementedError:
            pytest.fail(f"Enum member {member.name} was added but has no class implementation!")


# test each enum member returns correct class name
@pytest.mark.parametrize("enum_member, expected_name", [
(DataType.ImageInt, "ImageInt"),
(DataType.ImageFloat, "ImageFloat"),
(DataType.ImageBinary, "ImageBinary"),
(DataType.ValueInt, "ValueInt"),
(DataType.ValueFloat, "ValueFloat")])
def test_enum_resolves_to_correct_class_name(enum_member, expected_name):
    resolved_class = enum_member.name
    assert resolved_class == expected_name

# test each class refers to correct enum member
@pytest.mark.parametrize("enum_member, data_type", [
(DataType.ImageInt, ImageInt),
(DataType.ImageFloat, ImageFloat),
(DataType.ImageBinary, ImageBinary),
(DataType.ValueInt, ValueInt),
(DataType.ValueFloat, ValueFloat)])
def test_data_type_resolves_to_correct_class_type(enum_member, data_type):
    assert data_type.data_type == enum_member

@pytest.mark.parametrize("enum_member, test_value, core_type", [
(DataType.ValueInt, 2, ValueInt),
(DataType.ValueFloat, 12, ValueFloat)])
def test_value_data_type_instantiates_correct_class(enum_member, test_value, core_type):
    x = enum_member(test_value)
    assert(isinstance(x, core_type))
    assert(x.value == test_value)

@pytest.mark.parametrize("enum_member, test_value, core_type", [
(DataType.ImageInt, [5,2], ImageInt),
(DataType.ImageFloat, [0.5,0.1], ImageFloat),
(DataType.ImageBinary, [1,0], ImageBinary)])
def test_image_data_type_instantiates_correct_class(enum_member, test_value, core_type):
    x = enum_member(test_value)
    assert(isinstance(x, core_type))
    assert(x.value.all() == np.array(test_value).all())


@pytest.mark.parametrize("enum_member, test_value", [
(DataType.ValueInt, 2.5),
(DataType.ValueFloat, "12")])
def test_value_data_type_raises_type_error(enum_member, test_value):
    with pytest.raises(TypeError):
        enum_member(test_value)

@pytest.mark.parametrize("enum_member, test_value", [
(DataType.ImageInt, [215.2,5]),
(DataType.ImageFloat, ["2", 0.5]),
(DataType.ImageBinary, ["2",1])])
def test_image_data_type_raises_type_error(enum_member, test_value):
    with pytest.raises(TypeError):
        enum_member(test_value)


@pytest.mark.parametrize("enum_member, test_value", [
(DataType.ImageInt, [298,-5]),
(DataType.ImageFloat, [2, 0.5]),
(DataType.ImageBinary, [2,1])])
def test_image_data_type_raises_value_error(enum_member, test_value):
    with pytest.raises(ValueError):
        enum_member(test_value)