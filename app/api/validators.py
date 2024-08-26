from typing import Optional, Union


def validate_age_order(
    filtered_ordered_response: dict,
) -> Optional[Union[dict, str, None]]:
    """
    Validate that min_age is not greater than max_age.
    If validation fails, prompt user for confirmation to swap ages.

    Args:
        filtered_ordered_response (dict): Filtered dictionary of extracted parameters.

    Returns:
        dict or str or None: Validated response with swapped ages or error message.
                    Returns None if no action is required.
    """

    if (
        "min_age" in filtered_ordered_response
        and "max_age" in filtered_ordered_response
    ):
        min_age = int(filtered_ordered_response["min_age"])
        max_age = int(filtered_ordered_response["max_age"])

        if min_age > max_age:
            return (
                "Sorry but minimum age can’t be bigger than maximum age."
            )

    return None


def validate_diagnosis_and_control(
    filtered_ordered_response: dict,
) -> Optional[str]:
    """
    Validate that subjects cannot be both healthy controls and have a diagnosis.

    Args:
        filtered_ordered_response (dict): Filtered dictionary of extracted parameters.

    Returns:
        str or None: Error message if validation fails, otherwise None.
    """
    if "diagnosis" in filtered_ordered_response:
        if (
            "is_control" in filtered_ordered_response
            and filtered_ordered_response["is_control"]
        ):
            return "Subjects cannot both be healthy controls and have a diagnosis."

    return None
