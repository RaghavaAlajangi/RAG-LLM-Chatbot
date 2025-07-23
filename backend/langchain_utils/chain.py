from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_openai import ChatOpenAI
from openai import OpenAI

from ..core.config import settings
from .retriever import get_retriever

openai_client = OpenAI(
    api_key=settings.GWDG_API_KEY, base_url=settings.GWDG_ENDPOINT
)


def llm_generator(model_name):
    return ChatOpenAI(
        model_name=model_name,
        api_key=settings.GWDG_API_KEY,
        base_url=settings.GWDG_ENDPOINT,
        temperature=0,
    )


def get_rag_chain(model_name, prompt):
    llm = llm_generator(model_name)
    retriever = get_retriever()
    llm_chain = create_stuff_documents_chain(llm, prompt)
    qa_chain = create_retrieval_chain(retriever, llm_chain)
    return qa_chain
