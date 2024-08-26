import pytest
from unittest.mock import patch
from app.api.url_generator import get_api_url,main


def test_get_api_url_without_env_var(monkeypatch):
    # Unset the environment variable
    monkeypatch.delenv("NB_API_QUERY_URL", raising=False)

    user_query = "Some query"
    
    with pytest.raises(RuntimeError, match="The application was launched but could not find the NB_API_QUERY_URL environment variable."):
        get_api_url(user_query)


def test_json_decode_error():
    with patch.dict(
        "os.environ",
        {"NB_API_QUERY_URL": "https://api.neurobagel.org/query/?"},
    ):
        with patch(
            "app.api.url_generator.extract_information",
            return_value="{invalid_json: true",
        ):
            result = get_api_url("some user query")
            assert (
                result
                == "I'm sorry, but I couldn't find the information you're looking for. Could you provide more details or clarify your question?"
            )


# Define the mock responses for diagnosis and assessment term URLs
mock_diagnosis_mappings = {
    "traumatic brain injury": "snomed:127295002",
    "ocd": "snomed:191736004",
}

mock_assessment_mappings = {
    "balloon analogue risk task": "cogatlas:trm_4d559bcd67c18",
}


@pytest.mark.parametrize(
    "user_query, mock_llm_response, expected_output",
    [
        (
            "How many subjects between 20 and 80 yrs old who have at least 3 phenotypic sessions and 2 imaging sessions?",
            '{"min_age": 20, "max_age": 80, "min_num_imaging_sessions": 2, "min_num_phenotypic_sessions": 3}',
            "https://api.neurobagel.org/query/?min_age=20&max_age=80&min_num_imaging_sessions=2&min_num_phenotypic_sessions=3",
        ),
        (
            "male healthy control subjects",
            '{"sex": "male", "is_control": true}',
            "https://api.neurobagel.org/query/?sex=snomed:248153007&is_control=true",
        ),
        (
            "subjects diagnosed with traumatic brain injury assessed with balloon analogue risk task and T2 weighted image modality",
            '{"diagnosis": "traumatic brain injury", "assessment": "balloon analogue risk task", "image_modal": "T2 weighted"}',
            "https://api.neurobagel.org/query/?diagnosis=snomed:127295002&assessment=cogatlas:trm_4d559bcd67c18&image_modal=nidm:T2Weighted",
        ),
        (
            "female healthy control subjects with parkinsons",
            '{"sex": "female", "is_control": true, "diagnosis": "parkinsons"}',
            "Subjects cannot both be healthy controls and have a diagnosis.",
        ),
        (
            "Female subjects suffering from Arachnoiditis assessed by regulated heat stimulation",
            '{"sex": "female", "diagnosis": "arachnoiditis", "assessment": "regulated heat stimulation"}',
            "Unfortunately, Neurobagel does not yet support searches for the following terms: arachnoiditis diagnosis, regulated heat stimulation assessment",
        ),
        (
            "subjects with maximum age 6 and minimum age 20",
            '{"min_age": 20, "max_age": 6}',
            "Sorry but minimum age can’t be bigger than maximum age.",
        ),
        (
            "females suffering from ocd assessed by balloon analogue risk task with eeg image modal",
            '{"sex": "female", "diagnosis": "ocd", "assessment": "balloon analogue risk task", "image_modal": "eeg"}',
            "https://api.neurobagel.org/query/?sex=snomed:248152002&diagnosis=snomed:191736004&assessment=cogatlas:trm_4d559bcd67c18&image_modal=nidm:EEG",
        ),
        (
            "",
            "{}",
            "Please enter a correct query",
        ),
    ],
)
@patch(
    "app.api.url_generator.get_diagnosis_termURL",
    side_effect=lambda diagnosis: mock_diagnosis_mappings.get(
        diagnosis, "None"
    ),
)
@patch(
    "app.api.url_generator.get_assessment_termURL",
    side_effect=lambda assessment: mock_assessment_mappings.get(
        assessment, "None"
    ),
)
def test_get_api_url(
    mock_get_diagnosis_termURL,
    mock_get_assessment_termURL,
    user_query,
    mock_llm_response,
    expected_output,
):
    with patch.dict(
        "os.environ",
        {"NB_API_QUERY_URL": "https://api.neurobagel.org/query/?"},
    ):
        with patch(
            "app.api.url_generator.extract_information",
            return_value=mock_llm_response,
        ):
            result = get_api_url(user_query)
            assert result == expected_output

def test_main_interactive():
    """
    Test the main interactive loop.
    """
    inputs = ["", "exit"]
    expected_outputs = [
        "Response:",
        "",
    ]
    with patch("builtins.input", side_effect=inputs):
        with patch("builtins.print") as mock_print:
            main()
            actual_printed_outputs = [
                call.args[0] for call in mock_print.call_args_list
            ]
            assert actual_printed_outputs == expected_outputs