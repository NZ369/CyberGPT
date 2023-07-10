# Import things that are needed generically
from langchain import ConversationChain
from langchain.tools import BaseTool, Tool
from typing import Any, Optional
from langchain.chains import RetrievalQA
from langchain.chains.question_answering import load_qa_chain
from llms.azure_llms import create_llm
from uploaders.main import get_pdf_text, get_text_chunks, get_vectorstore
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.chains.router import MultiRetrievalQAChain
from uploaders.main import load_pdfs_from_folder
import traceback

tool_llm = create_llm()

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)

qa: Any
vectorstore: None

tool_name = "Database Document Retrieval"
tool_description = "useful for getting contextually relevant and accurate information on various specialized topics including user guides and technical documentation"

def load_indexes():
    global qa_retrievers
    qa_retrievers = {
        "test-index": create_qa_retriever(path='./guides', type="azure", database="pinecone", index="test-index")
    }

def create_qa_retriever(path, type, database, index):
    # Split data into text chunks
    text_chunks = load_pdfs_from_folder(path)
    # Create vector store
    return get_vectorstore(text_chunks, type=type, database=database, index=index)

class db_retrieval_tool(BaseTool):
    name = tool_name
    description = tool_description

    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        try:
            if 'qa_retrievers' not in globals():
                load_indexes()
            global qa_retrievers
            docs = qa_retrievers["test-index"].similarity_search(query)
            chain = load_qa_chain(tool_llm, chain_type="stuff")
            return chain.run(input_documents=docs, question=query)
        except Exception as e:
            traceback.print_exc()
            return f"Tool not available for use."

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")

qa_retrieve = db_retrieval_tool()
db_retrieval_tool = Tool(
    name = tool_name,
    description = tool_description,
    func= qa_retrieve.run
    )