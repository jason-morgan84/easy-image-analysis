from core.constants import DataType
from core.type import ImageInt, ImageFloat, ImageBinary, ValueInt, ValueFloat
import pytest

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


@pytest.mark.parametrize("enum_member, expected_name", [
(DataType.ImageInt, "ImageInt"),
(DataType.ImageFloat, "ImageFloat"),
(DataType.ImageBinary, "ImageBinary"),
(DataType.ValueInt, "ValueInt"),
(DataType.ValueFloat, "ValueFloat")])
def test_enum_resolves_to_correct_class_name(enum_member, expected_name):
    resolved_class = enum_member.name
    assert resolved_class == expected_name


@pytest.mark.parametrize("enum_member, data_type", [
(DataType.ImageInt, ImageInt),
(DataType.ImageFloat, ImageFloat),
(DataType.ImageBinary, ImageBinary),
(DataType.ValueInt, ValueInt),
(DataType.ValueFloat, ValueFloat)])
def test_data_type_resolves_to_correct_class_type(enum_member, data_type):
    assert data_type.data_type == enum_member