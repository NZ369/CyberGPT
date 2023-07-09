import shodan
import re
# Import things that are needed generically
from langchain.tools import BaseTool, Tool
from typing import Optional
from llms.azure_llms import create_llm
from langchain.prompts import PromptTemplate
from langchain import PromptTemplate, LLMChain

tool_llm = create_llm(temp=0.4)

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)

# your shodan API key
SHODAN_API_KEY = 'QPWbPNV5UODo5TMNvUdFpXEiSG8DbnWm'
api = shodan.Shodan(SHODAN_API_KEY)

template = """Given the information provided {info} reformat all the data to be more readable and also append an analysis based on the data"""
prompt_template = PromptTemplate(input_variables=["info"], template=template)
answer_chain = LLMChain(llm=tool_llm, prompt=prompt_template)

def shodan_ip_search(ip):
    result = ""
    try:
        # Lookup the host
        host = api.host(ip)
        # Build general info string
        general_info = """
            IP: {}
            Organization: {}
            Operating System: {}
        """.format(host['ip_str'], host.get('org', 'n/a'), host.get('os', 'n/a'))
        # Append general info to result
        result += general_info
        # Build banners string
        banners = ""
        for item in host['data']:
            banner = """
                Port: {}
                Banner: {}

            """.format(item['port'], item['data'])
            banners += banner
        # Append banners to result
        result += banners

    except shodan.APIError as e:
        result = 'Error: {}'.format(e)

    return result

class ip_lookup_tool(BaseTool):
    name = "IP Lookup"
    description = "use for getting info about an IP address, provides a snapshot of the exposed services and potential vulnerabilities associated with a particular IP address"
    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        try:
            ip = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', query).group()
            response = shodan_ip_search(ip)
            prompt = "Include all previous information and also append a detailed analysis based on the data"
            return (response + prompt)
        except:
            return "Tool not available for use."

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")
    
ip_lookup = ip_lookup_tool()
ip_lookup_tool = Tool(
    name = "IP Lookup",
    description = "use for getting info about an IP address, provides a snapshot of the exposed services and potential vulnerabilities associated with a particular IP address",
    func= ip_lookup.run
    )
