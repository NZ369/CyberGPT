from langchain.agents.tools import Tool
from llms.azure_llms import create_llm
from tools.prebuilt_tools import python_tool, wikipedia_tool, duckduckgo_tool
from tools.qa_tools import qa_retrieval_tool
from tools.kendra.tool import kendra_retrieval_tool;

tool_llm = create_llm()

base_tools=[
    python_tool,
    wikipedia_tool,
    duckduckgo_tool
]

qa_tools=[
    kendra_retrieval_tool
]