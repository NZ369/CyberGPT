#####################################################
# 
#  General Sequential Multi-Tool
#
#  INPUT -> TOOL 1 -> TOOL 2 -> TOOL 3
#             v          v           v
#           SUMMARY -> SUMMARY -> SUMMARY -> REPORT
#####################################################

# Import things that are needed generically
from traceback import print_exc
from langchain import LLMChain, PromptTemplate
from langchain.tools import BaseTool, Tool
from typing import Any, Optional
from langchain.chains.question_answering import load_qa_chain
from llms.azure_llms import create_llm
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from tools.borealis_tools import borealis_tool
from langchain.chains.summarize import load_summarize_chain
from tools.ipapi_tools import ipapi_tool

from tools.opencti_tools import openCTI_tool
from tools.shodan_tools import shodan_ip_lookup_tool

tool_name = "IP Report Tool"
tool_description = "Queries all tools that require an IP address as the input. Produces a comprehensive, detailed report for the user."
tool_llm = create_llm()

template = """You have many IP analysis tools at your disposal.
At each step, you must summarize the data and generate a technical report based on the output provided from each tool.
For the technical report, output each module on a new line and provide a detailed, insightful summary of the information provided in as few words as possible.
Example:
VIRUSTOTAL:
    - Associated with 1 malicious file
    - Address belongs to the Example organization and has an ASN of 11111
    - VIRUSTOTAL report at https://www.virustotal.com/gui/ip-address/example
End of example
Report:
{report}"""
prompt_template = PromptTemplate(input_variables=["report"], template=template)
tool_chain = LLMChain(llm=tool_llm, prompt=prompt_template)

ip_tools=[
    borealis_tool,
    openCTI_tool,
    shodan_ip_lookup_tool,
    ipapi_tool
]

class ip_report_tool(BaseTool):
    name = tool_name
    description = tool_description

    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        try:
            # responses = [SequentialChain(chains=[tool])(query) for tool in ip_tools]
            responses = [f"Tool: {tool.name}\n" + tool(query) for tool in ip_tools]
            # summarizer = load_summarize_chain(tool_llm, chain_type="map_reduce")
            report = ""
            for response in responses:
                # report += summarizer.run(page_content=f"{report}\n{response}")
                print(response)
                report += tool_chain.run(f"{template}\n{report}\n{response}")
                # print(report)
            return report
        except:
            print_exc()
            return "Tool not available for use."


    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")
    
qa_retrieve = ip_report_tool()
ip_report_tool = Tool(
    name = tool_name,
    description = tool_description,
    func= qa_retrieve.run
    )