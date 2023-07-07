from langchain.agents.tools import Tool
from llms.azure_llms import create_llm
from tools.prebuilt_tools import python_tool, wikipedia_tool, duckduckgo_tool
from tools.qa_tools import qa_retrieval_tool
from tools.borealis_tools import borealis_tool
<<<<<<< HEAD
from tools.opencti_tools import openCTI_tool
from tools.shodan_tools import shodan_ip_lookup_tool
from tools.ipapi_tools import ipapi_tool
=======
from tools.kendra_tool import kendra_retrieval_tool;
>>>>>>> 72be8d5 (Implemented kendra tool)

tool_llm = create_llm()
tools=[]

tools.append(python_tool)
tools.append(wikipedia_tool)
tools.append(duckduckgo_tool)
tools.append(qa_retrieval_tool)
tools.append(borealis_tool)
tools.append(openCTI_tool)
tools.append(shodan_ip_lookup_tool)
tools.append(ipapi_tool)
tools.append(kendra_retrieval_tool)
