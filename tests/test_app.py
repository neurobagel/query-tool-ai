import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to the Neurobagel Query Tool AI API"
    }


# Mock responses for get_api_url
mock_responses = {
    "How many subjects between 20 and 80 yrs old who have at least 3 phenotypic sessions and 2 imaging sessions?": "https://api.neurobagel.org/query/?min_age=20.0&max_age=80.0&min_num_imaging_sessions=2&min_num_phenotypic_sessions=3",
    "male healthy control subjects": "https://api.neurobagel.org/query/?sex=snomed:248153007&is_control=true",
    "subjects diagnosed with traumatic brain injury assessed with balloon analogue risk task and T2 weighted image modality": "https://api.neurobagel.org/query/?diagnosis=snomed:127295002&is_control=false&assessment=cogatlas:trm_4d559bcd67c18&image_modal=nidm:T2Weighted",
    "female healthy control subjects with parkinsons": "Subjects cannot both be healthy controls and have a diagnosis.",
    "Female subjects suffering from Arachnoiditis assessed by regulated heat stimulation": "Unfortunately, Neurobagel does not yet support searches for the following terms: arachnoiditis diagnosis, regulated heat stimulation assessment",
}


@pytest.mark.parametrize(
    "query, expected_status_code, expected_response",
    [
        (
            "How many subjects between 20 and 80 yrs old who have at least 3 phenotypic sessions and 2 imaging sessions?",
            200,
            {
                "response": "https://api.neurobagel.org/query/?min_age=20.0&max_age=80.0&min_num_imaging_sessions=2&min_num_phenotypic_sessions=3"
            },
        ),
        (
            "male healthy control subjects",
            200,
            {
                "response": "https://api.neurobagel.org/query/?sex=snomed:248153007&is_control=true"
            },
        ),
        (
            "subjects diagnosed with traumatic brain injury assessed with balloon analogue risk task and T2 weighted image modality",
            200,
            {
                "response": "https://api.neurobagel.org/query/?diagnosis=snomed:127295002&is_control=false&assessment=cogatlas:trm_4d559bcd67c18&image_modal=nidm:T2Weighted"
            },
        ),
        (
            "female healthy control subjects with parkinsons",
            200,
            {
                "response": "Subjects cannot both be healthy controls and have a diagnosis."
            },
        ),
        (
            "Female subjects suffering from Arachnoiditis assessed by regulated heat stimulation",
            200,
            {
                "response": "Unfortunately, Neurobagel does not yet support searches for the following terms: arachnoiditis diagnosis, regulated heat stimulation assessment"
            },
        ),
    ],
)
@patch(
    "app.router.routes.get_api_url",
)
def test_generate_url(
    mock_get_api_url, query, expected_status_code, expected_response
):
    mock_get_api_url.return_value = expected_response
    response = client.post("/generate_url/", json={"query": query})

    assert response.status_code == expected_status_code
    assert response.json() == expected_response
