import pytest
import requests
from requests.exceptions import RequestException
from unittest.mock import patch
from app.fetch_termURLs.get_termURLs import (
    fetch_termURL_mappings,
    get_diagnosis_termURL,
    get_assessment_termURL,
    get_sex_termURL,
    get_image_modal_termURL
)


def test_fetch_termURL_mappings_success() -> None:
    url = "http://example.com/api/mappings"
    mock_response_data: List[Dict[str, str]] = [
        {"TermURL": "termURL1", "Label": "label1"},
        {"TermURL": "termURL2", "Label": "label2"},
    ]
    
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response_data
        
        result = fetch_termURL_mappings(url)
        assert result == mock_response_data


def test_fetch_termURL_mappings_http_error() -> None:
    url = "http://example.com/api/mappings"
    
    with patch('requests.get') as mock_get:
        mock_get.return_value.raise_for_status.side_effect = RequestException("HTTP Error")
        
        result = fetch_termURL_mappings(url)
        assert result is None


@pytest.mark.parametrize("diagnosis, expected_termURL", [
    ("attention deficit hyperactivity disorder", "snomed:406506008"),
    ("concussion injury of brain", "snomed:110030002"),
    ("unknown disease", "None"),
])
def test_get_diagnosis_termURL(diagnosis: str, expected_termURL: str) -> None:
    diagnosis_termURL = get_diagnosis_termURL(diagnosis)
    assert diagnosis_termURL == expected_termURL


@pytest.mark.parametrize("assessment, expected_termURL", [
    ("zuckerman sensation seeking scale", "cogatlas:trm_56abebfe9aaa3"),
    ("big five questionnaire", "cogatlas:trm_523f5c17d7edb"),
    ("unknown assessment", "None"),
])
def test_get_assessment_termURL(assessment: str, expected_termURL: str) -> None:
    assessment_termURL = get_assessment_termURL(assessment)
    assert assessment_termURL == expected_termURL


@pytest.mark.parametrize("sex, expected_termURL", [
    ("male", "snomed:248153007"),
    ("female", "snomed:248152002"),
    ("unknown", "None"),
])
def test_get_sex_termURL(sex: str, expected_termURL: str) -> None:
    sex_termURL = get_sex_termURL(sex)
    assert sex_termURL == expected_termURL


@pytest.mark.parametrize("image_modal, expected_termURL", [
    ("arterial spin labeling", "nidm:ArterialSpinLabeling"),
    ("flow weighted", "nidm:FlowWeighted"),
    ("unknown image modality", "None"),
])
def test_get_image_modal_termURL(image_modal: str, expected_termURL: str) -> None:
    image_modal_termURL = get_image_modal_termURL(image_modal)
    assert image_modal_termURL == expected_termURL

