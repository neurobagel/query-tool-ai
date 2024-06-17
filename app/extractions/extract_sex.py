from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models import ChatOllama
from langchain.chains import LLMChain
import re


def extract_output(output: str) -> str:
    """
    Extracts the sex from the given output string.
    Args:
        output (str): The output string from the LLM.
    Returns:
        str: The extracted sex ('male', 'female', or 'null').
    """
    match = re.search(
        r"output\s*=\s*(male|female|null)", output, re.IGNORECASE
    )
    if match:
        return match.group(1).lower()
    else:
        return "null"


def extract_sex(user_query: str) -> str:
    """
    Extracts the sex mentioned in the given user query.
    Args:
        user_query (str): The query containing information about sex.
    Returns:
        str: The extracted sex if mentioned, otherwise 'null'.
    """
    prompt = PromptTemplate(
        input_variables=["user_query"],
        template="""
        Extract the sex (male,female,other) from the following user_query if given, otherwise return 'null' in the following format:
        output = <extracted_sex>
        user_query: {user_query}
        """,
    )
    llm = ChatOllama(model="gemma")
    chain = LLMChain(llm=llm, prompt=prompt)
    output = chain.run(user_query)
    return extract_output(output)


if __name__ == "__main__":
    user_query = input("Enter user_query: ")
    sex = extract_sex(user_query)

    print("sex:", sex)
