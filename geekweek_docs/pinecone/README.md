# Pinecone
## A vector database

### 1. Set up
Implementing Pinecone for a smaller vector database solution is a great first step!
Luckily, Pinecone makes it easy to get started.

Once we create an account we can create an index. Simply navigate to the indexes page and click "Create Index"


![Create Index](/geekweek_docs/kendra/1.png)

Then we can grab our key from the "API keys" section.

As for code, we can initialize the vector database and load the documents using this code snippet:

```
import os
import pinecone
from dotenv import load_dotenv
from langchain.vectorstores import Pinecone

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
index_name = 'test-index'

def pinecone_init():
    pinecone.init(
    api_key=PINECONE_API_KEY,
    environment=PINECONE_ENVIRONMENT,
    )

    if index_name not in pinecone.list_indexes():
        pinecone.create_index(name=index_name, metric='cosine', dimension=1536)

def pinecone_from_documents(docs, embeddings, index_name):
    pinecone_init()
    return Pinecone.from_documents(documents=docs, embedding=embeddings, index_name=index_name)
```

The key here is `Pinecone.from_documents()` which loads in our set of documents as a BytesIO object and uploads it to the index so we can query from it later.

Here is an example implementation of a tool that queries the vector database and passes it to the vector chain:

```
class db_retrieval_tool(BaseTool):
    name = tool_name
    description = tool_description

    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        try:
            if 'qa_retrievers' not in globals():
                load_indexes()
            global qa_retrievers
            docs = qa_retrievers["test-index"].similarity_search(query)
            chain = load_qa_chain(tool_llm, chain_type="stuff")
            return chain.run(input_documents=docs, question=query)
        except Exception as e:
            traceback.print_exc()
            return f"Tool not available for use."

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")
```

### Problems

The above implementation is great for getting you started, but if you want a robust system you don't want to be embedding and uploading your documents every time you start the program. Instead, we need to use `index = pinecone.Index(index_name)` and pass that along instead. We then need a separate tool or UI for uploading documents to the index.

### What we learned
Pinecone is amazing for getting the bare minimum up and running, for free! And if you're willing to pay, it can be a great tool in general. However, it takes some effort to get going in an efficient manner for more than just proof of concept.

### What we achieved
This was our fallback database in case our Kendra implementation failed, which was able to be quickly set up within a day.

### Future improvements
We likely won't be using Pinecone going forward but learning about a tool that's easy to implement is important in case we need it in the future.