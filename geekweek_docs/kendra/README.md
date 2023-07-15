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

#### 3.1 Retriever

#### 3.2 Tool

#### 3.3 LLM integration

## Problems

 - AWS permissions
 - A lot of AWS permission
 - Hallucinating when no documents are found

## What we learned

 - AWS is a pain to set up & connect to


## What We Achieved

 - Setting up AWS kendra DB
 - Learned about the foundational schema classes for langchain - to create more complex and custom tools, retrievers & chains

## Future improvements
 - Set up another vector DB and compare & contrast different models against Kendra
 - Hosting on AWS
   - Has access to secret keys to directly connect to kendra rather than using an insecure api endpoint