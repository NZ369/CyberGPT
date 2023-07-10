from typing import Any, Optional, List

from langchain.schema.retriever import BaseRetriever
from langchain.schema.document import Document;

import requests;
import json;

from langchain.callbacks.manager import (
    AsyncCallbackManagerForRetrieverRun,
    CallbackManagerForRetrieverRun,
    Callbacks,
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
            lambda doc: Document(page_content = doc[1], metadata={'source': doc[0]}),
            response
        )
    )

    print(documents);

    return documents

class KendraRetriever(BaseRetriever):

    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:
        return get_relevant_documents(query)
    async def _aget_relevant_documents(
        self, query: str, *, run_manager: AsyncCallbackManagerForRetrieverRun
    ) -> List[Document]:
        raise NotImplementedError()