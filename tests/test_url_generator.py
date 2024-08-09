import pytest
from unittest.mock import patch
from app.api.url_generator import get_api_url


def test_json_decode_error():
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
    "user_query, mock_llm_response, mock_input_side_effect, expected_output",
    [
        (
            "How many subjects between 20 and 80 yrs old who have at least 3 phenotypic sessions and 2 imaging sessions?",
            '{"min_age": 20, "max_age": 80, "min_num_imaging_sessions": 2, "min_num_phenotypic_sessions": 3}',
            None,
            "https://api.neurobagel.org/query/?min_age=20&max_age=80&min_num_imaging_sessions=2&min_num_phenotypic_sessions=3",
        ),
        (
            "male healthy control subjects",
            '{"sex": "male", "is_control": true}',
            None,
            "https://api.neurobagel.org/query/?sex=snomed:248153007&is_control=true",
        ),
        (
            "subjects diagnosed with traumatic brain injury assessed with balloon analogue risk task and T2 weighted image modality",
            '{"diagnosis": "traumatic brain injury", "assessment": "balloon analogue risk task", "image_modal": "T2 weighted"}',
            None,
            "https://api.neurobagel.org/query/?diagnosis=snomed:127295002&is_control=false&assessment=cogatlas:trm_4d559bcd67c18&image_modal=nidm:T2Weighted",
        ),
        (
            "female healthy control subjects with parkinsons",
            '{"sex": "female", "is_control": true, "diagnosis": "parkinsons"}',
            None,
            "Subjects cannot both be healthy controls and have a diagnosis.",
        ),
        (
            "Female subjects suffering from Arachnoiditis assessed by regulated heat stimulation",
            '{"sex": "female", "diagnosis": "arachnoiditis", "assessment": "regulated heat stimulation"}',
            None,
            "Unfortunately, Neurobagel does not yet support searches for the following terms: arachnoiditis diagnosis, regulated heat stimulation assessment",
        ),
        (
            "subjects with maximum age 6 and minimum age 20",
            '{"min_age": 20, "max_age": 6}',
            ["no"],
            "Sorry but minimum age can’t be bigger than maximum age.",
        ),
        (
            "subjects with maximum age 6 and minimum age 20",
            '{"min_age": 20, "max_age": 6}',
            ["yes"],
            "https://api.neurobagel.org/query/?min_age=6&max_age=20",
        ),
        (
            "females suffering from ocd assessed by balloon analogue risk task with eeg image modal",
            '{"sex": "female", "diagnosis": "ocd", "assessment": "balloon analogue risk task", "image_modal": "eeg"}',
            None,
            "https://api.neurobagel.org/query/?sex=snomed:248152002&diagnosis=snomed:191736004&is_control=false&assessment=cogatlas:trm_4d559bcd67c18&image_modal=nidm:EEG",
        ),
        (
            "",
            "{}",
            None,
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
    mock_input_side_effect,
    expected_output,
):
    with patch(
        "app.api.url_generator.extract_information",
        return_value=mock_llm_response,
    ):
        if mock_input_side_effect is not None:
            with patch("builtins.input", side_effect=mock_input_side_effect):
                result = get_api_url(user_query)
        else:
            result = get_api_url(user_query)
        assert result == expected_output
