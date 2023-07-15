# Kendra
## Set Up
### 1. Vector DB Set-up
#### 1.1. Creating S3 Bucket

To create an S3 bucket for storing your vector data, follow these steps:

- Open the [S3 console](https://console.aws.amazon.com/s3/) and click **Create bucket**.

![Create bucket button](/geekweek_docs/kendra/1.png)

- Enter a unique name for your bucket and select a region. Make sure your bucket does not block public access and click **Create bucket**.

![Bucket name and region](/geekweek_docs/kendra/3.jpeg)

- Go to the **Properties** tab of your bucket and note down the **ARN** of your bucket. You will need it later to grant permissions to Kendra.

![Bucket ARN](/geekweek_docs/kendra/4.png)

- To upload files to your S3 bucket, use the AWS CLI or the S3 console. For optimal performance, use plain text documents with minimal formatting, such as markdown, txt, etc.

#### 1.2. Creating Kendra Index

To create a Kendra index for searching your vector data, follow these steps:

- Open the [Kendra console](https://console.aws.amazon.com/kendra/) and click **Create index**.

![Create index button](/geekweek_docs/kendra/5.png)

- Enter a name for your index and select an edition. Choose **Create a new role** and enter a name for the role. This role will allow Kendra to access your S3 bucket and other AWS services. Click **Create index**.

![Index name and role](/geekweek_docs/kendra/7.png)

- Go to the **IAM console** and find the role you just created. Note down the **ARN** of the role. You will need it later to grant permissions to S3.

![Role ARN](/geekweek_docs/kendra/8.png)

#### 1.3. Granting Permissions

To grant permissions for Kendra to access your S3 bucket, follow these steps:

- Go to the **IAM console** and select **Policies** from the left menu.

![Policies menu](/geekweek_docs/kendra/10.png)

- Search for the policy attached to the role you created for Kendra and click on it.

![Policy search](/geekweek_docs/kendra/11.png)

- Click **Edit policy** and then **Add additional permissions**.

![Edit policy button](/geekweek_docs/kendra/12.png)

- In the **Service** field, select **S3**. In the **Actions** field, select **GetObject** and **ListBucket**. In the **Resources** field, enter the ARN of your S3 bucket and click **Add**.

![Add statement](/geekweek_docs/kendra/13.png)

- Click **Review policy** and then **Save changes**.

#### 1.4 Indexing/Syncing Data

To index and sync your vector data from S3 to Kendra, follow these steps:

- Go back to the **Kendra console** and select the index you created.

![Select index](/geekweek_docs/kendra/14.png)

- Click **Add data sources** and then select **Amazon S3 connector**.

![Add data sources button](/geekweek_docs/kendra/15.png)

- Enter a name for your data source and select the role you created for Kendra.

![Data source name and role](/geekweek_docs/kendra/17.png)

- Enter the URL of your S3 bucket in the **Bucket name** field. Optionally, you can specify a prefix or a suffix to filter the files you want to index. Select how often you want to sync your data with Kendra and click **Next**.

![Data source settings](/geekweek_docs/kendra/19.png)

- On the next page, select **Use Amazon S3 metadata fields as attributes in Amazon Kendra** and click **Next**.

![Data source mapping](/geekweek_docs/kendra/20.png)

- Review your data source configuration and click **Next**. Then click **Sync now** to start indexing your data.

### 2. Connecting To Kendra

To connect to your Kendra index and query your vector data, you need to create an API endpoint and a Lambda function.

#### 2.1 Create AWS Lambda Function

A Lambda function is a serverless function that can execute your code in response to an event, such as an API request. To create a Lambda function for querying Kendra, follow these steps:

- Go to the [Lambda console](https://console.aws.amazon.com/lambda/) and click **Create function**.

![Create function button](/geekweek_docs/kendra/22.png)

- Choose **Author from scratch**, enter a name for your function, and select **Python 3.8** as the runtime. Click **Create function**.

![Function settings](/geekweek_docs/kendra/36.png)

- On your local machine, create a folder for your Lambda function and install `boto3` in it using `pip install boto3 -t .`. This is because Amazon's Lambda function does not use the latest version of `boto3`, which is the AWS SDK for Python.
- In the same folder, create a file named `lambda_function.py` and write a function named `lambda_handler` that will handle requests for queries on the Kendra index. You can use the file `tools\kendra\lambda_function.py` as a reference on what needs to be done.
- Zip the folder and upload it to your Lambda function using the **Upload from** option.

![Upload zip file](/geekweek_docs/kendra/23.png)

- Go to the **Configuration** tab of your Lambda function and select **Permissions**. Click on the role name under **Execution role**. This will take you to the IAM console where you can add permissions for your Lambda function to access Kendra.

![Execution role](/geekweek_docs/kendra/25.png)

- In the IAM console, click **Attach policies** and search for Kendra in the filter. Select `AmazonKendraFullAccess` and click **Attach policy**. Note: It is unknown if `AmazonKendraReadOnlyAccess` would work, but if it does, it might be a better permission.

![Attach policy](/geekweek_docs/kendra/27.png)

#### 2.3 Create an API Endpoint

An API endpoint is a URL that allows you to interact with your Lambda function over the internet. To create an API endpoint for your Lambda function, follow these steps:

- Go to the [API Gateway console](https://console.aws.amazon.com/apigateway/) and click **Create API**.

![Create API button](/geekweek_docs/kendra/29.png)

- Choose **REST API** and click **Build**.

![REST API option](/geekweek_docs/kendra/30.png)

- Enter a name for your API and click **Create API**.

![API name](/geekweek_docs/kendra/31.png)

- Under **Resources**, select **/** and click **Actions**. Then select **Create Method** and choose **GET** from the dropdown menu.

![Create method](/geekweek_docs/kendra/32.png)

- Under **Integration type**, select **Lambda Function** and enter the name of your Lambda function. Click **Save**.

![Integration settings](/geekweek_docs/kendra/32.png)

- Click **Actions** again and select **Deploy API**.

![Deploy API](/geekweek_docs/kendra/33.png)

- Choose **[New Stage]** from the dropdown menu, enter a name for your stage, and click **Deploy**.

![Stage settings](/geekweek_docs/kendra/34.png)

#### 2.4 Accessing API Endpoint

To access your API endpoint and query your Kendra index, follow these steps:

- Go to the **Stages** tab of your API and select your stage name.

![Stages tab](/geekweek_docs/kendra/35.png)

- Copy the **Invoke URL** from the top of the page. This is the URL of your API endpoint.


### 3. LLM Integration

Langchain allows you to integrate external tools to enhance your LLMs. One of the tools you can use is Kendra, a vector-based search engine that can retrieve relevant documents for your queries.

#### 3.1 Retriever

A [Retriever](https://github.com/hwchase17/langchain/blob/master/langchain/schema/retriever.py) class defines methods to get documents from a data source. To create a Retriever class for Kendra, you need to do the following:

- Define a class that inherits from Retriever and implements the abstract methods `_get_relevant_documents` and `_aget_relevant_documents`. These methods should return a list of [Documents](https://github.com/hwchase17/langchain/blob/master/langchain/schema/document.py), which are objects that contain the content and metadata of a document.
- In the implementation of these methods, you need to perform the following steps:
  - Send a GET request to the API endpoint of your Kendra index with the query as a parameter. For example, in Python, you can use the `requests` library:

  ```python
  response = requests.get(
    'https://nc6toszo09.execute-api.ca-central-1.amazonaws.com/dev',
    headers= {"content-type":"application/json"},
    data = json.dumps({"query":query})
  )
  ```

  - Parse the JSON response and map each result to a Document object. For example, in Python, you can use the `json` and `map` libraries:

  ```python 
  response = json.loads(response.text)

  # map to document
  documents = list(
    map(
      # Parsing api request into documents
      lambda doc: Document(page_content = doc[1], metadata={'source': doc[0]}),
      response
    )
  )
  ```

  - Check if any documents were retrieved. If not, add a dummy document that says "No information available for the topic" to prevent the LLM from hallucinating.

  ```python
  if len(documents) == 0:
    documents = [
      Document(
        page_content="No information available for the topic",
        metadata={'source': "404 Not Found"}
      )
    ]
  ```

  - Return the list of documents.

  ```python
  return documents
  ```

#### 3.2 Tool

A [Tool](https://github.com/hwchase17/langchain/blob/master/langchain/tools/base.py#L132) is a class that defines methods and variables required for an LLM chain to use the Kendra retrieval tool over other tools. To create a Tool class for Kendra, you need to do the following:

- Define a class that inherits from BaseTool and implements the abstract methods `_run` and `_arun`. These methods should take an input query and return an output answer.
- Define the static variables `name` and `description` for your tool. These variables will help the LLM decide whether or not to use your tool.
- In the implementation of these methods, you need to perform the following steps:
  - Create a [QA chain](https://python.langchain.com/docs/modules/chains/popular/vector_db_qa) to process Kendra data. This chain will use your LLM and other components to generate an answer from the retrieved documents. For example, in Python, you can use the `load_qa_chain` function:

  ```python
  chain = load_qa_chain(tool_llm, chain_type="stuff");
  ```

  - Use your Retriever class to query a list of documents from Kendra. For example, in Python, you can instantiate your class and call its method:

  ```python
  retriever=KendraRetriever()

  docs = retriever.get_relevant_documents(query)
  ```

  - Feed the documents into the QA chain and get the answer. For example, in Python, you can call the chain's method:

  ```python
  return chain.run(input_documents=docs, question=query)
  ```

#### 3.3 LLM Integration

You can integrate your Tool and Retriever classes into your LLM in two ways:

- You can add your Tool class to a list of tools when instantiating an agent. This way, your tool will be available for any chain that uses that agent. For example, in Python, you can use the `initialize_agent` function:

```python
llm = create_llm(max_tokens=2000, temp=0.5)

base_agent = initialize_agent(
  [KendraTool()],
  llm,
  agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
  max_iterations=4,
  verbose=True,
  memory=memory
  )
```

- You can pass your Retriever class to a chain when instantiating it. This way, your retriever will be used only by that chain and no other tool or retriever will be used. For example, in Python, you can use the `ConversationalRetrievalChain.from_llm` function:

```python
llm = create_llm()

memory = ConversationBufferWindowMemory(memory_key="chat_history", k=3, return_messages=True)
qa_chain = ConversationalRetrievalChain.from_llm(
  llm,
  retriever=KendraRetriever(),
  memory=memory,
  verbose=True
  )
```

The former approach is better when you want the retriever to be used with a variety of other tools, while the latter is better when you want the chain not to use any other tool or retriever.

## Challenges

During the development of the Kendra integration, we faced some challenges that we would like to share and discuss possible solutions.

1. AWS Setup
The most time-consuming part of the project was setting up the AWS infrastructure. We had to deal with various issues related to accessing AWS services and configuring permissions for Kendra, S3, Lambda, and API Gateway.

2. Hallucinations
The LLM sometimes hallucinated when no documents were retrieved by Kendra for a given query. We tried to mitigate this by adding a dummy document that says "No information available for the topic", but this did not completely eliminate the problem. The hallucinations were more likely to occur when querying in an ongoing conversation, as the LLM tried to use the previous context to generate an answer. A possible solution might be to reduce the conversation history or maintain context blocks and only use previous questions when they are relevant to the current query.

## What We Achieved

In this project, we accomplished the following goals:

- We set up an AWS Kendra index to store and search our vector data. We configured the permissions, data sources, and sync settings for our index.
- We learned about the foundational schema classes for Langchain, such as Retriever, Document, and Tool. We used these classes to create more complex and custom tools, retrievers, and chains for our LLMs.

## Future Improvements

For future work, we suggest the following improvements:

- We can set up another vector-based search engine and compare its performance and features with Kendra. This will help us evaluate the strengths and weaknesses of different models and choose the best one for our needs.
- We can host our application on AWS and use secret keys to directly connect to Kendra. This will improve the security and reliability of our API endpoint and avoid exposing sensitive data to unauthorized users.