# Kendra
## Set Up
### 1. Vector DB Set-up
#### 1.1. Creating S3 Bucket

![alt text](/geekweek_docs/kendra/1.png)

#### 1.2. Creating kendra instance

#### 1.3. Permissions

#### 1.4 Indexing/Syncing DB

### 2. Connecting To Kendra

#### 2.1 Create an API endpoint

#### 2.2 Linking AWS endpoint

#### 2.3 Getting info from Kendra using Boto3

#### 2.5 Accessing API endpoint

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