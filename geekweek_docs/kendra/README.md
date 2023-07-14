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

#### 2.1 Create AWS Lambda function

#### 2.2 Getting info from Kendra using Boto3

#### 2.3 Create an API endpoint
 - Create AWS API Endpoint
 - Link to Lambda function to get

#### 2.4 Accessing API endpoint
 - Simple HTTP request

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