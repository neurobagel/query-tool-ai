import argparse
import json
import re
import os
import requests
from typing import List, Dict
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import PromptTemplate
from app.fetch_termURLs.termURL_mappings import (
    sex_mapping,
    diagnosis_url,
    assessment_url,
    image_modality_mapping,
)


def fetch_diagnosis_labels(url: str) -> List[str]:
    """
    Fetches diagnosis terms from the given API URL.

    Args:
        url (str): The API URL to fetch terms from.

    Returns:
        List[str]: A list of diagnosis terms.
    """
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(
            f"Failed to fetch data from {url} with status code {response.status_code}"
        )

    data = response.json()
    return [
        term.get("Label", "").strip()
        for term in data.get("nb:Diagnosis", [])
        if term.get("Label")
    ]


def fetch_assessment_labels(url: str) -> List[str]:
    """
    Fetches assessment terms from the given API URL.

    Args:
        url (str): The API URL to fetch terms from.

    Returns:
        List[str]: A list of assessment terms.
    """
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(
            f"Failed to fetch data from {url} with status code {response.status_code}"
        )

    data = response.json()
    return [
        term.get("Label", "").strip()
        for term in data.get("nb:Assessment", [])
        if term.get("Label")
    ]


def fetch_sex_labels(mapping: Dict[str, str]) -> List[str]:
    """
    Fetches sex labels from the hardcoded mapping.

    Args:
        mapping (Dict[str, str]): The hardcoded mapping for sex terms.

    Returns:
        List[str]: A list of sex labels.
    """
    return list(mapping.keys())


def fetch_image_modality_labels(mapping: List[Dict[str, str]]) -> List[str]:
    """
    Fetches image modality labels from the hardcoded mapping.

    Args:
        mapping (List[Dict[str, str]]): The hardcoded mapping for image modality terms.

    Returns:
        List[str]: A list of image modality labels.
    """
    return [item["label"] for item in mapping]


def generate_abbreviations(input_terms: List[str], output_file: str) -> None:
    """
    Generates abbreviations for a list of terms using ChatOllama model and saves them in a Python file.

    Args:
        input_terms (List[str]): List of terms for which abbreviations are generated.
        output_file (str): Output Python file to save abbreviations.
    """
    llm = ChatOllama(model="llama3")
    prompt = PromptTemplate(
        template="""Please respond with abbreviations most commonly used for the
following term: {term}.
Give only the abbreviations as output and prefer the ones used in research
data and papers.
For example:
Input:'diabetes mellitus'
Output:'DM', 'DM2', 'DM1'.
Do Not Give any explanation in the output.
Input: "{term}"
Output= <abbreviations>
    """,
        input_variables=["term"],
    )
    chain = prompt | llm

    abbreviations_list = []
    for term in input_terms:
        if not term:
            continue

        response = chain.invoke({"term": term})
        response = str(response)
        match = re.search(r"content='(.*?)'", response)

        if match:
            content_part = match.group(1)
        else:
            content_part = ""
        abbreviations = (
            [abbr.strip() for abbr in content_part.split(",")]
            if content_part
            else []
        )
        abbreviations_dict = {"label": term, "abbreviations": abbreviations}
        abbreviations_list.append(abbreviations_dict)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, output_file)

    with open(output_path, "w") as py_file:
        py_file.write(
            f"{os.path.splitext(os.path.basename(output_file))[0]} = {json.dumps(abbreviations_list, indent=4)}\n"
        )

    print(f"Abbreviations saved to {output_path}")


def main(output_file_prefix: str) -> None:
    """
    Main function to fetch labels and generate abbreviations for diagnosis, assessment, sex, and image modality terms.
    Saves each type of labels in a separate Python file.

    Args:
        output_file_prefix (str): Prefix for output Python files.
    """

    diagnosis_terms = fetch_diagnosis_labels(diagnosis_url)
    generate_abbreviations(
        diagnosis_terms, f"{output_file_prefix}_diagnosis.py"
    )

    assessment_terms = fetch_assessment_labels(assessment_url)
    generate_abbreviations(
        assessment_terms, f"{output_file_prefix}_assessment.py"
    )

    sex_terms = fetch_sex_labels(sex_mapping)
    generate_abbreviations(sex_terms, f"{output_file_prefix}_sex.py")

    image_modality_terms = fetch_image_modality_labels(image_modality_mapping)
    generate_abbreviations(
        image_modality_terms, f"{output_file_prefix}_image_modality.py"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process terms.")
    parser.add_argument(
        "--output-prefix",
        type=str,
        default="abbreviations",
        help="The prefix for output Python files to save abbreviations.",
    )
    args = parser.parse_args()
    main(args.output_prefix)
