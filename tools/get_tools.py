from langchain.agents.tools import Tool
from llms.azure_llms import create_llm
from tools.prebuilt_tools import python_tool, wikipedia_tool, duckduckgo_tool
from tools.qa_tools import qa_retrieval_tool
from tools.db_retrievers import db_retrieval_tool

tool_llm = create_llm()
tools=[
    # python_tool,
    # wikipedia_tool,
    # duckduckgo_tool,
    # qa_retrieval_tool,
    db_retrieval_tool
]