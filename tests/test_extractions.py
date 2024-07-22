import pytest
import warnings
from typing import Dict
from app.LLM_extractions.extractions import extract_information


@pytest.mark.parametrize(
    "context, expected_response",
    [
        (
            "How many subjects between 20 and 80 yrs old who have at least 3 phenotypic sessions and 2 imaging sessions?",
            {
                "max_age": 80.0,
                "min_age": 20.0,
                "min_num_imaging_sessions": 2,
                "min_num_phenotypic_sessions": 3,
            },
        ),
        (
            "male healthy control subjects",
            {
                "sex": "male",
                "is_control": True,
            },
        ),
        (
            "subjects diagnosed with traumatic brain injury assessed with child behaviour checklist and T2 weighted image modality",
            {
                "diagnosis": "traumatic brain injury",
                "is_control": False,
                "assessment": "child behaviour checklist",
                "image_modal": "t2 weighted",
            },
        ),
        (
            "female subjects suffering from social phobia with 1 phenotypic session",
            {
                "sex": "female",
                "diagnosis": "social phobia",
                "is_control": False,
                "min_num_phenotypic_sessions": 1,
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
