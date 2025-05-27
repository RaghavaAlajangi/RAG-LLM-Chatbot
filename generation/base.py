from langchain.chains import create_retrieval_chain
from langchain_core.output_parsers import StrOutputParser


class RAG:
    def __init__(self, retriever, prompt, generator):
        self.retriever = retriever
        self.prompt = prompt
        self.llm = generator

    def ask_quary(self, question):
        """Ask a question using the RAG system."""
        llm_chain = self.prompt | self.llm | StrOutputParser()
        qa_chain = create_retrieval_chain(self.retriever, llm_chain)

        response = qa_chain.invoke({"input": question})
        return response["answer"]
