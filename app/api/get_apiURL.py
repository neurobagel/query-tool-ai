import json
from app.LLM_extractions.extractions import extract_information
from app.api.validations import (
    validate_age_order,
    validate_diagnosis_and_control,
)
from app.fetch_termURLs.get_termURLs import (
    get_diagnosis_termURL,
    get_assessment_termURL,
    get_sex_termURL,
    get_image_modality_termURL,
)


def getApiURL(user_query: str) -> str:
    """
    Constructs the API URL using extracted parameters from the user's query.

    Args:
        user_query (str): The query provided by the user.

    Returns:
        str: The constructed API URL.
    """
    base_api_url = "https://api.neurobagel.org/query/?"
    llm_response = extract_information(user_query)

    try:
        if isinstance(llm_response, str):
            llm_response = json.loads(llm_response)
        if not llm_response:
            return "Please enter a correct query"

        params = []
        unsupported_terms = []

        # Validate the response
        age_validation_result = validate_age_order(llm_response)
        if isinstance(age_validation_result, str):
            return age_validation_result
        elif isinstance(age_validation_result, dict):
            llm_response = age_validation_result

        diagnosis_validation_result = validate_diagnosis_and_control(
            llm_response
        )
        if diagnosis_validation_result:
            return diagnosis_validation_result

        if "min_age" in llm_response:
            params.append(f"min_age={llm_response['min_age']}")

        if "max_age" in llm_response:
            params.append(f"max_age={llm_response['max_age']}")

        if "sex" in llm_response:
            sex_term_url = get_sex_termURL(llm_response["sex"])

            if sex_term_url == "None":
                unsupported_terms.append(f"{llm_response['sex']} sex")
            else:
                params.append(f"sex={sex_term_url}")

        if "diagnosis" in llm_response:
            diagnosis_term_url = get_diagnosis_termURL(
                llm_response["diagnosis"]
            )

            if diagnosis_term_url == "None":
                unsupported_terms.append(
                    f"{llm_response['diagnosis']} diagnosis"
                )
            else:
                params.append(f"diagnosis={diagnosis_term_url}")

        if "is_control" in llm_response:
            params.append(
                f"is_control={str(llm_response['is_control']).lower()}"
            )

        if "min_num_imaging_sessions" in llm_response:
            params.append(
                f"min_num_imaging_sessions={llm_response['min_num_imaging_sessions']}"
            )

        if "min_num_phenotypic_sessions" in llm_response:
            params.append(
                f"min_num_phenotypic_sessions={llm_response['min_num_phenotypic_sessions']}"
            )

        if "assessment" in llm_response:
            assessment_term_url = get_assessment_termURL(
                llm_response["assessment"]
            )

            if assessment_term_url == "None":
                unsupported_terms.append(
                    f"{llm_response['assessment']} assessment"
                )
            else:
                params.append(f"assessment={assessment_term_url}")

        if "image_modal" in llm_response:
            image_modal_term_url = get_image_modality_termURL(
                llm_response["image_modal"]
            )

            if image_modal_term_url == "None":
                unsupported_terms.append(
                    f"{llm_response['image_modal']} image modality"
                )
            else:
                params.append(f"image_modal={image_modal_term_url}")

        # Check for unsupported terms and construct the error message if any
        if unsupported_terms:
            return f"Unfortunately, Neurobagel does not yet support searches for the following terms: {', '.join(unsupported_terms)}"

        # Construct the full API URL by joining the base URL with the parameters
        api_url = base_api_url + "&".join(params)
        return api_url

    except json.JSONDecodeError:
        return "I'm sorry, but I couldn't find the information you're looking for. Could you provide more details or clarify your question?"


if __name__ == "__main__":

    while True:
        user_query = input("Enter user query (or 'exit' to quit): ")
        if user_query.lower() == "exit":
            break

        api_url = getApiURL(user_query)
        print("Response:", api_url)
        print("")
