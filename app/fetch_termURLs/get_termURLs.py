import requests
from typing import Optional, Dict, Any
from termURL_mappings import (
    sex_mapping,
    diagnosis_url,
    assessment_url,
    image_modality_mapping,
)


def fetch_termURL_mappings(url: str) -> Optional[Dict[str, Any]]:
    """
    Fetches the term URL mappings from the given URL.

    Args:
        url (str): The URL to fetch the term URL mappings from.

    Returns:
        Optional[Dict[str, Any]]: The JSON response containing the term URL mappings,
        or None if an error occurred during the request.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching mapping data: {e}")
        return None


def get_diagnosis_termURL(diagnosis: str) -> str:
    """
    Retrieves the TermURL for a given diagnosis.

    Args:
        diagnosis (str): The diagnosis label to search for.

    Returns:
        str: The TermURL corresponding to the diagnosis label, or "None" if not found.
    """
    diagnosis_mapping = fetch_termURL_mappings(diagnosis_url)
    if diagnosis_mapping:
        for item in diagnosis_mapping.get("nb:Diagnosis", []):
            if (str(item.get("Label"))).lower() == diagnosis:
                return item.get("TermURL", "None")
    return "None"


def get_assessment_termURL(assessment: str) -> str:
    """
    Retrieves the TermURL for a given assessment.

    Args:
        assessment (str): The assessment label to search for.

    Returns:
        str: The TermURL corresponding to the assessment label, or "None" if not found.
    """
    assessment_mapping = fetch_termURL_mappings(assessment_url)
    if assessment_mapping:
        for item in assessment_mapping.get("nb:Assessment", []):
            if (str(item.get("Label"))).lower() == assessment:
                return item.get("TermURL", "None")
    return "None"


def get_sex_termURL(sex: str) -> str:
    """
    Retrieves the TermURL for a given sex.

    Args:
        sex (str): The sex label to search for.

    Returns:
        str: The TermURL corresponding to the sex label, or "None" if not found.
    """
    if sex in sex_mapping:
        return sex_mapping[sex]
    return "None"


def get_image_modal_termURL(image_modal: str) -> str:
    """
    Retrieves the TermURL for a given image_modality.

    Args:
        image_modality (str): The image_modality label to search for.

    Returns:
        str: The TermURL corresponding to the image_modality label, or "None" if not found.
    """
    for item in image_modality_mapping:
        if (str(item.get("label"))).lower() == image_modal:
            return item.get("termURL")
    return "None"


if __name__ == "__main__":

    diagnosis = input("Enter diagnosis: ")
    print(f"Diagnosis TermURL: {get_diagnosis_termURL(diagnosis)}")

    assessment = input("Enter assessment: ")
    print(f"Assessment TermURL: {get_assessment_termURL(assessment)}")

    sex = input("Enter sex: ")
    print(f"Sex TermURL: {get_sex_termURL(sex)}")

    image_modal = input("Enter image modality: ")
    print(f"image_modality TermURL: {get_image_modal_termURL(image_modal)}")
