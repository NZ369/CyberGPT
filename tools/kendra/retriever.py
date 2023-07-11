from typing import Any, Optional, List

from langchain.schema import BaseRetriever;
from langchain.schema import Document;

import requests;
import json;

from langchain.callbacks.manager import (
    AsyncCallbackManagerForRetrieverRun,
    CallbackManagerForRetrieverRun,
    Callbacks
)

# Bucket Quick Reference
bucket = {
    "hog": "HOG-Spark",
    "data": "kendra-data-2-team-5-2",
    "test": "kendra-test-bucket-5-2"
}

class KendraRetriever(BaseRetriever):

    def get_relevant_documents(self, query: str) -> List[Document]:
        # request
        response = requests.get(
            'https://nc6toszo09.execute-api.ca-central-1.amazonaws.com/dev',
            headers= {"content-type":"application/json"},
            data = json.dumps({"query":query})
        )
        
        #parse json
        print(response.text[:200])

        response = json.loads(response.text)

        # map to document
        documents = list(
            map(
                lambda doc: Document(page_content = doc[1], metadata={'source': doc[0]}),
                filter(lambda doc: bucket['hog'] in doc[0] or bucket["data"] in doc[0], # 🐷
                       response
                )
            )
        )[:5]

        print(documents[:200]);

        return documents
    async def _aget_relevant_documents(
        self, query: str
    ) -> List[Document]:
        raise NotImplementedError()