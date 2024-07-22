import pytest
from requests.exceptions import RequestException
from unittest.mock import patch
from typing import List, Dict
from app.fetch_termURLs.get_termURLs import (
    fetch_termURL_mappings,
    get_diagnosis_termURL,
    get_assessment_termURL,
    get_sex_termURL,
    get_image_modality_termURL,
)


def test_fetch_termURL_mappings_success() -> None:
    """
    Test fetch_termURL_mappings function for successful API call.

    Mocks a successful API response and checks if the returned data
    matches the expected mock response data.
    """
    url = "http://example.com/api/mappings"
    mock_response_data: List[Dict[str, str]] = [
        {"TermURL": "termURL1", "Label": "label1"},
        {"TermURL": "termURL2", "Label": "label2"},
    ]

    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response_data

        result = fetch_termURL_mappings(url)
        assert result == mock_response_data


def test_fetch_termURL_mappings_http_error() -> None:
    """
    Test fetch_termURL_mappings function for HTTP error.

    Mocks an HTTP error during the API call and checks if the function
    returns None.
    """
    url = "http://example.com/api/mappings"

    with patch("requests.get") as mock_get:
        mock_get.return_value.raise_for_status.side_effect = RequestException(
            "HTTP Error"
        )

        result = fetch_termURL_mappings(url)
        assert result is None


@pytest.mark.parametrize(
    "diagnosis, expected_termURL",
    [
        ("Concussion injury Of brain", "snomed:110030002"),
        ("adhd", "snomed:406506008"),
        ("OCD", "snomed:191736004"),
        ("Parkinsons", "snomed:49049000"),
        ("fibromalgia", "snomed:203082005"),
        ("unknown", "None"),
    ],
)
def test_get_diagnosis_termURL(diagnosis: str, expected_termURL: str) -> None:
    """
    Test get_diagnosis_termURL function with different diagnosis inputs.
    """
    mock_diagnosis_response = {
        "nb:Diagnosis": [
            {
                "TermURL": "snomed:406506008",
                "Label": "attention deficit hyperactivity disorder",
            },
            {
                "TermURL": "snomed:110030002",
                "Label": "concussion injury of brain",
            },
            {
                "TermURL": "snomed:191736004",
                "Label": "Obsessive-compulsive disorder",
            },
            {"TermURL": "snomed:49049000", "Label": "Parkinson's disease"},
            {"TermURL": "snomed:203082005", "Label": "Fibromyalgia"},
        ]
    }

    with patch(
        "app.fetch_termURLs.get_termURLs.fetch_termURL_mappings",
        return_value=mock_diagnosis_response,
    ):
        diagnosis_termURL = get_diagnosis_termURL(diagnosis)
        assert diagnosis_termURL == expected_termURL


@pytest.mark.parametrize(
    "assessment, expected_termURL",
    [
        ("zuckerman scale", "cogatlas:trm_56abebfe9aaa3"),
        ("big five questionnaire", "cogatlas:trm_523f5c17d7edb"),
        ("balloon analogue", "cogatlas:trm_4d559bcd67c18"),
        ("unknown", "None"),
    ],
)
def test_get_assessment_termURL(
    assessment: str, expected_termURL: str
) -> None:
    """
    Test get_assessment_termURL function with different assessment inputs.
    """
    mock_assessment_response = {
        "nb:Assessment": [
            {
                "TermURL": "cogatlas:trm_56abebfe9aaa3",
                "Label": "zuckerman sensation seeking scale",
            },
            {
                "TermURL": "cogatlas:trm_523f5c17d7edb",
                "Label": "big five questionnaire",
            },
            {
                "TermURL": "cogatlas:trm_4d559bcd67c18",
                "Label": "balloon analogue risk task",
            },
        ]
    }

    with patch(
        "app.fetch_termURLs.get_termURLs.fetch_termURL_mappings",
        return_value=mock_assessment_response,
    ):
        assessment_termURL = get_assessment_termURL(assessment)
        assert assessment_termURL == expected_termURL


@pytest.mark.parametrize(
    "sex, expected_termURL",
    [
        ("male", "snomed:248153007"),
        ("female", "snomed:248152002"),
        ("fem", "snomed:248152002"),
        ("M", "snomed:248153007"),
        ("other", "snomed:32570681000036106"),
        ("unknown", "None"),
    ],
)
def test_get_sex_termURL(sex: str, expected_termURL: str) -> None:
    """
    Test get_sex_termURL function with different sex inputs.
    """
    sex_termURL = get_sex_termURL(sex)
    assert sex_termURL == expected_termURL


@pytest.mark.parametrize(
    "image_modality, expected_termURL",
    [
        ("arterial labeling", "nidm:ArterialSpinLabeling"),
        ("flow weighted", "nidm:FlowWeighted"),
        ("EEG", "nidm:EEG"),
        ("unknown image modality", "None"),
    ],
)
def test_get_image_modality_termURL(
    image_modality: str, expected_termURL: str
) -> None:
    """
    Test get_image_modality_termURL function with different image modality inputs.
    """
    mock_image_modality_response = [
        {
            "termURL": "nidm:ArterialSpinLabeling",
            "label": "arterial spin labeling",
        },
        {"termURL": "nidm:FlowWeighted", "label": "flow weighted"},
        {"termURL": "nidm:EEG", "label": "Electroencephalogram"},
    ]

    with patch(
        "app.fetch_termURLs.get_termURLs.image_modality_mapping",
        mock_image_modality_response,
    ):
        image_modality_termURL = get_image_modality_termURL(image_modality)
        assert image_modality_termURL == expected_termURL
