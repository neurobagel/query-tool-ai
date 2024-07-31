import pytest
import warnings
from typing import Dict
from unittest.mock import patch
from app.llm_processing.extractions import extract_information, main


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
            "subjects diagnosed with traumatic brain injury assessed with balloon analogue risk task and T2 weighted image modality",
            {
                "diagnosis": "traumatic brain injury",
                "is_control": False,
                "assessment": "balloon analogue risk task",
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


def test_main_interactive():
    """
    Test the main interactive loop.
    """
    inputs = ["", "exit"]
    expected_outputs = [
        "Model response:",
        "",
    ]
    with patch("builtins.input", side_effect=inputs):
        with patch("builtins.print") as mock_print:
            main()
            actual_printed_outputs = [
                call.args[0] for call in mock_print.call_args_list
            ]
            assert actual_printed_outputs == expected_outputs
