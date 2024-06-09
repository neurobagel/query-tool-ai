from langchain_core.prompts import PromptTemplate
from langchain_community.llms import HuggingFaceHub
from langchain.chains import LLMChain
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def extract_min_age(user_query: str) -> float:
    """
    Extracts the minimum age mentioned in the given user query.

    Args:
        user_query (str): The query containing information about age criteria.

    Returns:
        float: The extracted minimum age if mentioned, otherwise NaN.
    """
    examples = """
    Examples:
    1. user_query: "The study includes subjects older than 20 years."
       Output: 20
    2. user_query: "Participants must be younger than 30 years."
       Output: null
    3. user_query: "The minimum age for subjects is 18 years."
       Output: 18
    4. user_query: "Subjects aged more than 25 years are included."
       Output: 25
    5. user_query: "Individuals less than 40 years old are excluded."
       Output: null
    6. user_query: "Eligible participants are at least 21 years old."
       Output: 21
    7. user_query: "The age range is from 22 to 60 years."
       Output: 22
    """

    prompt = PromptTemplate(
        input_variables=["user_query"],
        template=f"""
        Extract the minimum age from the following user_query if given,
        otherwise put 'null'.
        {examples}
        user_query: {{user_query}}
        Output:
        """,
    )

    llm = HuggingFaceHub(
        repo_id="google/flan-t5-xxl", model_kwargs={"temperature": 0.01}
    )
    chain = LLMChain(prompt=prompt, llm=llm)

    output = chain.invoke({"user_query": user_query})
    min_age = output["text"].strip()

    try:
        return float(min_age)
    except ValueError:
        return float("nan")  # Return NaN if it's not a number


def extract_max_age(user_query: str) -> float:
    """
    Extracts the maximum age mentioned in the given user query.

    Args:
        user_query (str): The query containing information about age criteria.

    Returns:
        float: The extracted maximum age if mentioned, otherwise NaN.
    """
    examples = """
    Examples:
    1. user_query: "The study includes subjects younger than 80 years."
       Output: 80
    2. user_query: "Participants must be older than 30 years."
       Output: null
    3. user_query: "The maximum age for subjects is 65 years."
       Output: 65
    4. user_query: "Subjects aged less than 50 years are included."
       Output: 50
    5. user_query: "Individuals more than 40 years old are excluded."
       Output: null
    6. user_query: "Eligible participants are at most 55 years old."
       Output: 55
    7. user_query: "The age range is from 22 to 60 years."
       Output: 60
    """

    prompt = PromptTemplate(
        input_variables=["user_query"],
        template=f"""
        Extract the maximum age from the following user_query if given,
        otherwise put 'null'.
        {examples}
        user_query: {{user_query}}
        Output:
        """,
    )

    llm = HuggingFaceHub(
        repo_id="google/flan-t5-xxl", model_kwargs={"temperature": 0.01}
    )
    chain = LLMChain(prompt=prompt, llm=llm)

    output = chain.invoke({"user_query": user_query})
    max_age = output["text"].strip()

    try:
        return float(max_age)
    except ValueError:
        return float("nan")  # Return NaN if it's not a number


if __name__ == "__main__":
    user_query = input("Enter user_query: ")
    min_age = extract_min_age(user_query)
    max_age = extract_max_age(user_query)

    print("min_age:", min_age)
    print("max_age:", max_age)
