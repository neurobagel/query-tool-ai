from langchain_core.prompts import PromptTemplate
from langchain_community.llms import HuggingFaceHub
from langchain.chains import LLMChain
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def extract_min_num_imaging_sessions(user_query: str) -> int:
    """
    Extracts the minimum number of imaging sessions mentioned in the given user query.

    Args:
        user_query (str): The query containing information about the imaging sessions.

    Returns:
        int: The extracted minimum number of imaging sessions if mentioned, otherwise None.
    """
    prompt = PromptTemplate(
        input_variables=["user_query"],
        template="""
        Extract the minimum number of imaging sessions from the following user_query if given,
        otherwise put 'null'.
        user_query: {user_query}
        Output:
        """,
    )

    llm = HuggingFaceHub(
        repo_id="google/flan-t5-xxl", model_kwargs={"temperature": 0.01}
    )
    chain = LLMChain(prompt=prompt, llm=llm)

    output = chain.invoke({"user_query": user_query})
    min_num_imaging_sessions = output["text"].strip()

    try:
        return int(min_num_imaging_sessions)
    except ValueError:
        return -1  # Return -1 if it's not a number


def extract_min_num_phenotypic_sessions(user_query: str) -> int:
    """
    Extracts the minimum number of phenotypic sessions mentioned in the given user query.

    Args:
        user_query (str): The query containing information about the phenotypic sessions.

    Returns:
        int: The extracted minimum number of phenotypic sessions if mentioned, otherwise None.
    """

    prompt = PromptTemplate(
        input_variables=["user_query"],
        template="""
        Extract the minimum number of phenotypic sessions from the following user_query if given,
        otherwise put 'null'.
        user_query: {user_query}
        Output:
        """,
    )

    llm = HuggingFaceHub(
        repo_id="google/flan-t5-xxl", model_kwargs={"temperature": 0.01}
    )
    chain = LLMChain(prompt=prompt, llm=llm)

    output = chain.invoke({"user_query": user_query})
    min_num_phenotypic_sessions = output["text"].strip()

    try:
        return int(min_num_phenotypic_sessions)
    except ValueError:
        return -1  # Return -1 if it's not a number


if __name__ == "__main__":
    user_query = input("Enter user_query: ")
    min_num_imaging_sessions = extract_min_num_imaging_sessions(user_query)
    min_num_phenotypic_sessions = extract_min_num_phenotypic_sessions(
        user_query
    )

    print("min_num_imaging_sessions:", min_num_imaging_sessions)
    print("min_num_phenotypic_sessions:", min_num_phenotypic_sessions)
