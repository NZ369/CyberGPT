from langchain.agents.tools import Tool
from llms.azure_llms import create_llm
from tools.prebuilt_tools import python_tool, wikipedia_tool, duckduckgo_tool
from tools.qa_tools import qa_retrieval_tool
#from tools.csv_tools import mitre_retrieve_tool

tool_llm = create_llm()
tools=[]

tools.append(python_tool)
tools.append(wikipedia_tool)
tools.append(duckduckgo_tool)
tools.append(qa_retrieval_tool)
#tools.append(mitre_retrieve_tool)