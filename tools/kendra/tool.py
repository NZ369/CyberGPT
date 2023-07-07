from typing import Any, Optional, List

from llms.azure_llms import create_llm

import requests;
import json;

from langchain.schema.document import Document;

from langchain.tools import BaseTool, Tool

from langchain.chains.question_answering import load_qa_chain

tool_llm = create_llm()

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)

# initializing Amazon kendra retriever
'''
mfa_serial_number = None
retriever = None

def initialize_client():
    if mfa_serial_number is not None:
        response = sts_client.get_session_token(
            SerialNumber=mfa_serial_number, TokenCode=mfa_totp)
    else:
        response = sts_client.get_session_token()
    temp_credentials = response['Credentials']

    client = boto3.client(
        "kendra",
        aws_access_key_id=temp_credentials['AccessKeyId'],
        aws_secret_access_key=temp_credentials['SecretAccessKey'],
        aws_session_token=temp_credentials['SessionToken']
    )
    
    return client

if retriever is None:
    retriever = AmazonKendraRetriever(
        index_id=os.environ.get('KENDRA_INDEX_ID'),
        region_name="ca-central-1",
        client=initialize_client()
    )
'''

def get_relevant_documents(query: str) -> List[Document]:
    # request
    print(json.dumps({"query":query}))
    response = requests.get('https://nc6toszo09.execute-api.ca-central-1.amazonaws.com/dev', headers={"content-type":"application/json"}, data = json.dumps({"query":query}))
    #parse json
    print(response.text)

    response = json.loads(response.text)

    # map to document
    documents = list(
        map(
            lambda doc: Document(page_content = doc[1], metadata={}),
            response
        )
    )

    print(documents);

    return documents

# setting up kendra tool class
class KendraTool(BaseTool):
    name = "Kendra Document Retrieval"
    description = "use for getting contextually relevant information for answers"

    def _run(self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        docs = get_relevant_documents(query);

        chain = load_qa_chain(tool_llm, chain_type="stuff");

        return chain.run(input_documents=docs, question=query)

    async def _arun(self, *args: Any, **kwargs: Any) -> str:
        raise NotImplementedError()
        pass

kendra_tool = KendraTool()

kendra_retrieval_tool = Tool(
    name = "Kendra Document Retrieval",
    description = "use for getting contextually relevant information for answers",
    func = kendra_tool.run
)