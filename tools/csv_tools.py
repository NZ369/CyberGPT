# Import things that are needed generically
from langchain.tools import BaseTool, Tool
from typing import Any, Optional
from langchain.chains import RetrievalQA
from agents.csv_agent import mitre_csv_agent
from llms.azure_llms import create_llm
from uploaders.main import get_pdf_text, get_text_chunks, get_vectorstore
from langchain.chains.conversation.memory import ConversationBufferWindowMemory

tool_llm = create_llm()

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)

class MitreCsvRetrievalTool(BaseTool):
    name = "Mitre Csv Retrieval"
    description = "Use this tool for interacting with MITRE data. Includes information on malware techniques, software families, and mitigations."

    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        try:
            #vectorstore.similarity_search(query)[0].page_content
            print(f"Sending query to mitre csv: {query}")
            return mitre_csv_agent.run(query)
        except:
            return "Tool not available for use."


    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")
    
mitre_retrieve = MitreCsvRetrievalTool()
mitre_retrieve_tool = Tool(
    name = "Mitre Csv Retrieval",
    description = "Use for querying data loaded from tables in python with pandas.",
    func= mitre_retrieve.run
    )