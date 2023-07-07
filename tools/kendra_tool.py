from typing import Any, Optional

from llms.azure_llms import create_llm

from aws import sts_client;

from langchain.tools import BaseTool, Tool

from langchain.chains import RetrievalQA
from langchain.chains.question_answering import load_qa_chain

from langchain.chains.conversation.memory import ConversationBufferWindowMemory

import boto3
from langchain.retrievers import AmazonKendraRetriever

tool_llm = create_llm()

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)

import os;

# initializing Amazon kendra retriever

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

# setting up kendra tool class
class KendraTool(BaseTool):
    name = "Kendra Document Retrieval"
    description = "use for getting contextually relevant information for answers"

    def _run(self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        docs = retriever.get_relevant_documents(query);

        chain = load_qa_chain(tool_llm, chain_type="stuff");

        return chain.run(input_documents=docs, question=query)

    async def _arun(self, *args: Any, **kwargs: Any) -> str:
        raise NotImplementedError()
        pass

kendra_tool = KendraTool()

kendra_retrieval_tool = Tool(
    name = KendraTool.name,
    description = KendraTool.description,
    func = kendra_tool.run
)