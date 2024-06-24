import pytest
import warnings
from typing import Tuple, Dict
from app.LLM_Extractions.extractions import extract_information


@pytest.fixture
def setup_successful_extraction() -> Tuple[str, Dict[str, str]]:
    """
    Fixture to set up a valid non-empty context for extract_information function.
    """
    context = "How many subjects between 20 and 80 yrs old who have at least 3 phenotypic sessions and 2 imaging sessions?"
    expected_response: Dict[str, str] = {
        "max_age": "80",
        "min_age": "20",
        "min_num_imaging_sessions": "2",
        "min_num_phenotypic_sessions": "3",
    }

    return context, expected_response


@pytest.fixture
def setup_empty_context() -> Tuple[str, Dict[str, str]]:
    """
    Fixture to set up an empty context for extract_information function.
    """
    context = ""
    expected_response: Dict[str, str] = {}

    return context, expected_response


def test_extract_information_successful(
    setup_successful_extraction: Tuple[str, Dict[str, str]]
) -> None:
    """
    Test case for extract_information function with valid non-empty context.
    """
    context, expected_response = setup_successful_extraction

    with warnings.catch_warnings(record=True) as w:
        result = extract_information(context)

        assert result == expected_response
        assert len(w) == 0, f"Unexpected warnings: {w}"


def test_extract_information_with_empty_context(
    setup_empty_context: Tuple[str, Dict[str, str]]
) -> None:
    """
    Test case for extract_information function with empty context.
    """
    context, expected_response = setup_empty_context

    with warnings.catch_warnings(record=True) as w:
        result = extract_information(context)

        assert result == expected_response
        assert len(w) == 0, f"Unexpected warnings: {w}"
