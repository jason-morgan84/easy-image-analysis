from core.constants import DataPolicy
from core.type_policies import ImageInt, ImageFloat, ImageBinary, ValueInt, ValueFloat
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

    actual_types = {member.name for member in DataPolicy}
    assert expected_types.issubset(actual_types), f"Missing expected types from enum: {expected_types - actual_types}"

    # test there's no empty enum values
    values = [member.value for member in DataPolicy]
    assert len(values) == len(set(values))

    # test every enum member has an associated class written
    for member in DataPolicy:
        try:
            resolved_class = member.name
            assert resolved_class is not None
        except NotImplementedError:
            pytest.fail(f"Enum member {member.name} was added but has no class implementation!")


# test each enum member returns correct class name
@pytest.mark.parametrize("enum_member, expected_name", [
(DataPolicy.ImageInt, "ImageInt"),
(DataPolicy.ImageFloat, "ImageFloat"),
(DataPolicy.ImageBinary, "ImageBinary"),
(DataPolicy.ValueInt, "ValueInt"),
(DataPolicy.ValueFloat, "ValueFloat")])
def test_enum_resolves_to_correct_class_name(enum_member, expected_name):
    resolved_class = enum_member.name
    assert resolved_class == expected_name

# test each class refers to correct enum member
@pytest.mark.parametrize("enum_member, data_type", [
(DataPolicy.ImageInt, ImageInt),
(DataPolicy.ImageFloat, ImageFloat),
(DataPolicy.ImageBinary, ImageBinary),
(DataPolicy.ValueInt, ValueInt),
(DataPolicy.ValueFloat, ValueFloat)])
def test_data_type_resolves_to_correct_class_type(enum_member, data_type):
    assert data_type.data_type == enum_member



