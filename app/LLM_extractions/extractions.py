from langchain_community.chat_models import ChatOllama
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from typing import Optional, Any
from validations import validate_age_order, validate_diagnosis_and_control
 

class Parameters(BaseModel):
    """
    Parameters for information extraction.

    Attributes:
        max_age (Optional[str]): Maximum age if specified.
        min_age (Optional[str]): Minimum age if specified.
        sex (Optional[str]): Sex.
        diagnosis (Optional[str]): Diagnosis.
        is_control (Optional[bool]): Healthy control subjects.
        min_num_imaging_sessions (Optional[str]): Minimum number of imaging sessions.
        min_num_phenotypic_sessions (Optional[str]): Minimum number of phenotypic sessions.
        assessment (Optional[str]): Assessment tool used or assessed with.
        image_modal (Optional[str]): Image modal.
    """

    max_age: Optional[str] = Field(
        description="maximum age (upper age limit) if specified", default=None
    )
    min_age: Optional[str] = Field(
        description="minimum age (lower age limit) if specified", default=None
    )
    sex: Optional[str] = Field(description="sex", default=None)
    diagnosis: Optional[str] = Field(description="diagnosis", default=None)
    is_control: Optional[bool] = Field(
        description="healthy control subjects", default=None
    )
    min_num_imaging_sessions: Optional[str] = Field(
        description="minimum number of imaging sessions", default=None
    )
    min_num_phenotypic_sessions: Optional[str] = Field(
        description="minimum number of phenotypic sessions", default=None
    )
    assessment: Optional[str] = Field(
        description="assessment tool used or assessed with", default=None
    )
    image_modal: Optional[str] = Field(description="image modal", default=None)


def extract_information(context: str) -> Any:
    """
    Extract information using LangChain pipeline with retry mechanism.

    Args:
        context (str): Input context from which information is to be extracted.

    Returns:
        dict or str: Extracted information structured according to Parameters schema,
                    or error message if validation fails.
    """

    # Return empty dictionary if context is empty string
    if context == "":
        return {}

    # Initialize LLM (ChatOllama)
    llm = ChatOllama(model="mistral")

    # Initialize JSON output parser
    parser = JsonOutputParser(pydantic_object=Parameters)

    # Define prompt template
    prompt = PromptTemplate(
        template="Just extract the information as specified.\n{format_instructions}\n{context}\nIf not mentioned, put null.",
        input_variables=["context"],
        partial_variables={
            "format_instructions": parser.get_format_instructions()
        },
    )

    retries = 3 
    current_attempt = 0

    while current_attempt < retries:
        try:
            # Create extraction chain
            chain = prompt | llm | parser

            # Invoke chain with provided context
            response = chain.invoke({"context": context})

            # Ensure the order of keys matches the Parameters model
            ordered_response = {
                field: response.get(field, None)
                for field in Parameters.__fields__.keys()
            }

            # Filter out keys where the value is None or 'None' (string)
            filtered_ordered_response = {
                k: v
                for k, v in ordered_response.items()
                if v is not None and v != "None"
            }

            # Validate age order
            age_validation_result = validate_age_order(filtered_ordered_response)
            if isinstance(age_validation_result, str):
                return age_validation_result  

            # Validate diagnosis and control
            diagnosis_validation_result = validate_diagnosis_and_control(filtered_ordered_response)
            if diagnosis_validation_result:
                return diagnosis_validation_result  

            # Return the filtered ordered information as a dictionary
            return filtered_ordered_response

        except Exception as e:
            print(f"Error occurred: {e}")
            current_attempt += 1  
            print(f"Retrying... Attempt {current_attempt} of {retries}")

    print(f"Failed to retrieve valid response after {retries} attempts.")
    return {}


def main() -> None:
    """
    Main function to interactively extract information from user queries.
    """
    while True:
        user_query = input("Enter user query (or 'exit' to quit): ")
        if user_query.lower() == "exit":
            break

        response = extract_information(user_query)
        print("Model response:", response)
        print("")


if __name__ == "__main__":
    main()
