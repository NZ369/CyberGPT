import shodan
import re
# Import things that are needed generically
from langchain.tools import BaseTool, Tool
from typing import Optional
from llms.azure_llms import create_llm
from langchain.prompts import PromptTemplate
from langchain import PromptTemplate, LLMChain
from langchain.chains import LLMRequestsChain

tool_llm = create_llm(temp=0.4)
tool_llm_temp0 = create_llm(temp=0)

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)

# your shodan API key
SHODAN_API_KEY = 'QPWbPNV5UODo5TMNvUdFpXEiSG8DbnWm'
api = shodan.Shodan(SHODAN_API_KEY)

info_template = """Given the information provided {info} reformat all the data to be more readable and also append an analysis based on the data"""
info_prompt_template = PromptTemplate(input_variables=["info"], template=info_template)
answer_chain = LLMChain(llm=tool_llm, prompt=info_prompt_template)

extract_template = """Between >>> and <<< are the raw search result text from google.
Extract the answer to the question '{query}' or say "not found" if the information is not contained.
Use the format
Extracted:<answer or "not found">
>>> {requests_result} <<<
Extracted:"""
extract_prompt_template = PromptTemplate(input_variables=["query", "requests_result"], template=extract_template)
chain = LLMRequestsChain(llm_chain=LLMChain(llm=tool_llm_temp0, prompt=extract_prompt_template))

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
            url = "https://api.shodan.io/shodan/host/"+str(ip)+"?key=QPWbPNV5UODo5TMNvUdFpXEiSG8DbnWm"
            #response = shodan_ip_search(ip)
            inputs = {
                "query": query,
                "url": url + query.replace(" ", "+"),
            }
            prompt = "Include all previous information and also append a detailed analysis based on the data"
            response = chain(inputs)
            return (str(response) + prompt)
        except Exception as e:
            return str(e)

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
