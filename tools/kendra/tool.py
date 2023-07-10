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


def get_relevant_documents(query: str) -> List[Document]:
    # request
    response = requests.get(
        'https://nc6toszo09.execute-api.ca-central-1.amazonaws.com/dev',
        headers= {"content-type":"application/json"},
        data = json.dumps({"query":query})
    )
    
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
    description = "Use to query relevant & contextual information related to technical documents, research papers and similar relevant data"

    def _run(self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        docs = get_relevant_documents(query);

        chain = load_qa_chain(tool_llm, chain_type="stuff");

        return chain.run(input_documents=docs, question=query)

    async def _arun(self, *args: Any, **kwargs: Any) -> str:
        raise NotImplementedError()
        pass

kendra_retrieval_tool = KendraTool()