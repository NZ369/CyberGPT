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

def create_qa_chain():
    # TODO: get docs from front-end
    global qa_retrievers
    global browser_pdf_docs
    qa_retrievers = [
        {
            "name": "user guide retrieval",
            "description": "useful for getting contextually relevant and accurate information on how to use Spark, Airflow, OAuth, NBGallery, Spellbook, JupyterLab, Superset, Trino, Fission Functions, Unifi, and DataHub.",
            "retriever": create_qa_retriever(path='./guides', type="azure", database="pinecone")
        }
    ]

def create_qa_retriever(path, type, database):
    # Split data into text chunks
    text_chunks = load_pdfs_from_folder(path)
    # Create vector store
    return get_vectorstore(text_chunks, type=type, database=database)

class db_retrieval_tool(BaseTool):
    name = tool_name
    description = tool_description

    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        try:
            global qa_retrievers
            default_chain=ConversationChain(llm=tool_llm, prompt=prompt_default, input_key='query', output_key='result')
            chain = MultiRetrievalQAChain.from_retrievers(tool_llm, qa_retrievers, verbose=True)
            return chain.run(query)
        except Exception as e:
            traceback.print_exc()
            return f"Tool not available for use."

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")

create_qa_chain()
qa_retrieve = db_retrieval_tool()
db_retrieval_tool = Tool(
    name = tool_name,
    description = tool_description,
    # description = "use for getting contextually relevant and accurate information on various specialized topics",
    func= qa_retrieve.run
    )