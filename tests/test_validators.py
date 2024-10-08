import pytest
from unittest.mock import patch
from app.api.validators import (
    validate_age_order,
    validate_diagnosis_and_control,
)


@pytest.mark.parametrize(
    "filtered_ordered_response, expected_response",
    [
        ({"min_age": "20", "max_age": "30"}, None),
        (
            {"min_age": "49", "max_age": "30"},
            "Sorry but minimum age can’t be bigger than maximum age.",
        ),
    ],
)
def test_validate_age_order(
    filtered_ordered_response, expected_response
):
    """
    Test validate_age_order function without user confirmation to swap ages.
    """
    result = validate_age_order(filtered_ordered_response)
    assert result == expected_response



@pytest.mark.parametrize(
    "filtered_ordered_response, expected_response",
    [
        (
            {"diagnosis": "mild depression", "is_control": True},
            "Subjects cannot both be healthy controls and have a diagnosis.",
        ),
        ({"diagnosis": "mood disorder", "is_control": False}, None),
        ({"diagnosis": "traumatic brain injury"}, None),
        ({"is_control": True}, None),
    ],
)
def test_validate_diagnosis_and_control(
    filtered_ordered_response, expected_response
):
    """
    Test validate_diagnosis_and_control function.
    """
    result = validate_diagnosis_and_control(filtered_ordered_response)
    assert result == expected_response
