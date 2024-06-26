import pytest
import warnings
from typing import Dict
from app.extractions import extract_information


@pytest.mark.parametrize(
    "context, expected_response",
    [
        (
            "How many subjects between 20 and 80 yrs old who have at least 3 phenotypic sessions and 2 imaging sessions?",
            {
                "max_age": "80",
                "min_age": "20",
                "min_num_imaging_sessions": "2",
                "min_num_phenotypic_sessions": "3",
            },
        ),
        ("", {}),
    ],
)
def test_extract_information(
    context: str, expected_response: Dict[str, str]
) -> None:
    """
    Parameterized test case for extract_information function.
    """
    with warnings.catch_warnings(record=True) as w:
        result = extract_information(context)

        assert result == expected_response
        assert len(w) == 0, f"Unexpected warnings: {w}"
