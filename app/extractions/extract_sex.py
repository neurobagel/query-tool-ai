from langchain_core.prompts import PromptTemplate
from langchain_community.llms import HuggingFaceHub
from langchain.chains import LLMChain
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


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
        Given the information in {user_query} Extract sex from it
        if given otherwise put 'null'
        """,
    )
    llm = HuggingFaceHub(
        repo_id="google/flan-t5-xxl", model_kwargs={"temperature": 0.01}
    )
    chain = LLMChain(prompt=prompt, llm=llm)

    output = chain.invoke({"user_query": user_query})
    sex = str(output["text"]).strip()

    return sex


if __name__ == "__main__":
    user_query = input("Enter user_query: ")
    sex = extract_sex(user_query)

    print("sex:", sex)
