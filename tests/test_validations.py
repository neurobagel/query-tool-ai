import pytest
from unittest.mock import patch
from app.api.validations import (
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
def test_validate_age_order_no_swap(
    filtered_ordered_response, expected_response
):
    """
    Test validate_age_order function without user confirmation to swap ages.
    """
    with patch("builtins.input", return_value="no"):
        result = validate_age_order(filtered_ordered_response)
        assert result == expected_response


@pytest.mark.parametrize(
    "filtered_ordered_response, expected_response",
    [({"min_age": "49", "max_age": "30"}, {"min_age": "30", "max_age": "49"})],
)
def test_validate_age_order_with_swap(
    filtered_ordered_response, expected_response
):
    """
    Test validate_age_order function with user confirmation to swap ages.
    """
    with patch("builtins.input", return_value="yes"):
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
