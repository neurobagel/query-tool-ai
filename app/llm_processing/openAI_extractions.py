from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from typing import Optional, Union
from tenacity import retry, stop_after_attempt
from langchain_community.chat_models import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()


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
    sex: Optional[str] = Field(
        description="sex, only accepts 'male' or 'female' or 'other'",
        default=None,
        examples=["male", "female", "other"],
    )
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


class ChatOpenRouter(ChatOpenAI):
    openai_api_base: str
    openai_api_key: str
    model_name: str

    def __init__(
        self,
        model_name: str,
        openai_api_key: Optional[str] = None,
        openai_api_base: str = "https://openrouter.ai/api/v1",
        **kwargs
    ):
        openai_api_key = openai_api_key or os.getenv("OPENROUTER_API_KEY")
        super().__init__(
            openai_api_base=openai_api_base,
            openai_api_key=openai_api_key,
            model_name=model_name,
            **kwargs
        )


@retry(stop=stop_after_attempt(3))
def extract_information(context: str) -> Optional[Union[dict, str, None]]:
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

    # Initialize LLM
    llm = ChatOpenRouter(model_name="openai/chatgpt-4o-latest")

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
            k: (
                float(v)
                if k in ["min_age", "max_age"] and v is not None
                else (
                    int(v)
                    if k
                    in [
                        "min_num_phenotypic_sessions",
                        "min_num_imaging_sessions",
                    ]
                    and v is not None
                    else (
                        v.lower()
                        if isinstance(v, str)
                        and k
                        in ["diagnosis", "assessment", "image_modal", "sex"]
                        else v
                    )
                )
            )
            for k, v in ordered_response.items()
            if v is not None and v != "None"
        }

        if "diagnosis" in filtered_ordered_response:
            if "is_control" not in filtered_ordered_response:
                filtered_ordered_response["is_control"] = False

        # Return the filtered ordered information as a dictionary
        return filtered_ordered_response

    except Exception:
        raise  # This will trigger the retry

    print(
        "Sorry the model failed to understand the query. Could you be more precise?"
    )
    return {}


def main():
    while True:
        user_query = input("Enter user query (or 'exit' to quit): ")
        if user_query.lower() == "exit":
            break

        response = extract_information(user_query)
        print("Model response:", response)
        print("")


if __name__ == "__main__":
    main()
