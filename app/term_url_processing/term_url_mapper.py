import requests
from typing import Optional, Dict, Any
import difflib
from term_url_mappings import (
    sex_mapping,
    diagnosis_url,
    assessment_url,
    image_modality_mapping,
)
from abbreviations.abbreviations_diagnosis import abbreviations_diagnosis
from abbreviations.abbreviations_assessment import abbreviations_assessment
from abbreviations.abbreviations_sex import abbreviations_sex
from abbreviations.abbreviations_image_modality import (
    abbreviations_image_modality,
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
        diagnosis = diagnosis.lower()
        labels = [
            (str(item.get("Label"))).lower()
            for item in diagnosis_mapping.get("nb:Diagnosis", [])
        ]

        # Direct match
        if diagnosis_mapping:
            for item in diagnosis_mapping.get("nb:Diagnosis", []):
                if (str(item.get("Label"))).lower() == diagnosis:
                    return item.get("TermURL", "None")

        # Partial match
        closest_matches = difflib.get_close_matches(
            diagnosis, labels, n=1, cutoff=0.6
        )
        if closest_matches:
            closest_match = closest_matches[0]
            for item in diagnosis_mapping.get("nb:Diagnosis", []):
                if (str(item.get("Label"))).lower() == closest_match:
                    return item.get("TermURL")

        # Abbreviation match
        for item in abbreviations_diagnosis:
            if diagnosis.lower() in (
                abbr.lower() for abbr in item["abbreviations"]
            ):
                return get_diagnosis_termURL(str(item["label"]).lower())

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
        assessment = assessment.lower()
        labels = [
            (str(item.get("Label"))).lower()
            for item in assessment_mapping.get("nb:Assessment", [])
        ]

        # Direct match
        for item in assessment_mapping.get("nb:Assessment", []):
            if (str(item.get("Label"))).lower() == assessment:
                return item.get("TermURL")

        # Partial match
        closest_matches = difflib.get_close_matches(
            assessment, labels, n=1, cutoff=0.6
        )
        if closest_matches:
            closest_match = closest_matches[0]
            for item in assessment_mapping.get("nb:Assessment", []):
                if (str(item.get("Label"))).lower() == closest_match:
                    return item.get("TermURL")

        # Abbreviation match
        for item in abbreviations_assessment:
            if assessment.lower() in (
                abbr.lower() for abbr in item["abbreviations"]
            ):
                return get_assessment_termURL(str(item["label"]).lower())

    return "None"


def get_sex_termURL(sex: str) -> str:
    """
    Retrieves the TermURL for a given sex.

    Args:
        sex (str): The sex label to search for.

    Returns:
        str: The TermURL corresponding to the sex label, or "None" if not found.
    """
    sex = sex.lower()
    sex_mapping_lower = {k.lower(): v for k, v in sex_mapping.items()}

    # Direct match
    if sex in sex_mapping_lower:
        return sex_mapping_lower[sex]

    # Partial match
    closest_matches = difflib.get_close_matches(
        sex, sex_mapping_lower.keys(), n=1, cutoff=0.6
    )
    if closest_matches:
        return sex_mapping_lower[closest_matches[0]]

    # Abbreviation match
    for item in abbreviations_sex:
        if sex.lower() in (abbr.lower() for abbr in item["abbreviations"]):
            return get_sex_termURL(str(item["label"]).lower())

    return "None"


def get_image_modality_termURL(image_modality: str) -> str:
    """
    Retrieves the TermURL for a given image_modality, including partial matches.

    Args:
        image_modality (str): The image_modality label to search for.

    Returns:
        str: The TermURL corresponding to the image_modality label, or None if not found.
    """
    image_modality = image_modality.lower()
    labels = [
        (str(item.get("label"))).lower() for item in image_modality_mapping
    ]

    # Direct match
    for item in image_modality_mapping:
        if (str(item.get("label"))).lower() == image_modality:
            return item.get("termURL")

    # Partial match
    closest_matches = difflib.get_close_matches(
        image_modality, labels, n=1, cutoff=0.6
    )
    if closest_matches:
        closest_match = closest_matches[0]
        for item in image_modality_mapping:
            if (str(item.get("label"))).lower() == closest_match:
                return item.get("termURL")

    # Abbreviation match
    for item in abbreviations_image_modality:
        if image_modality.lower() in (
            abbr.lower() for abbr in item["abbreviations"]
        ):
            return get_image_modality_termURL(str(item["label"]).lower())

    return "None"


if __name__ == "__main__":

    diagnosis = input("Enter diagnosis: ")
    print(f"Diagnosis TermURL: {get_diagnosis_termURL(diagnosis)}")

    assessment = input("Enter assessment: ")
    print(f"Assessment TermURL: {get_assessment_termURL(assessment)}")

    sex = input("Enter sex: ")
    print(f"Sex TermURL: {get_sex_termURL(sex)}")

    image_modal = input("Enter image modality: ")
    print(f"image_modality TermURL: {get_image_modality_termURL(image_modal)}")
