# Code does nothing but just a place to store the lambda func
# 
# Todo()! set up a git repo and add actions such that each commit into main updates the lambda func
from typing import Tuple, Optional
import json
import boto3
'''
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
import io
'''
kendra_client = boto3.client('kendra')
s3_client = boto3.client('s3')

def badRequest(code: int, reason = None):
    if reason is None:
        return {'statusCode': code}
    
    return {'statusCode': code, 'body': json.dumps(reason)}

#BUCKET_NAME = "kendra-test-bucket-5-2";
def response_mapper(file_data):
    try:
        uri = file_data["DocumentURI"].replace("http://", "").replace("https://", "")
        
        # Extract text from the PDF using textract
        text_content = file_data["DocumentExcerpt"]["Text"]
        
        return file_data["Id"], text_content
    except Exception as e:
        print(e)
        raise e

def lambda_handler(event, context):
    
    # extract body from event
    if 'headers' not in event:
        return badRequest(500, "No Header");
    header = event['headers']
    if 'body' not in event:
        return badRequest(500, "No body");
    body = event['body']
    
    # extract query json
    if body is None:
        return badRequest(400, reason = "No query");


    if 'content-type' not in header or header['content-type'] != 'application/json':
        return badRequest(400, reason = "Invalid content-type");
    
    query_json = None;
    try:
        query_json = json.loads(body);
    except json.JSONDecodeError:
        return badRequest(400, "Failed to parse json - do better");

    # query data
    if 'query' not in query_json:
        return badRequest(400, reason="No query");

    response = kendra_client.query(
        IndexId='81dec93a-0c04-4fa3-9bee-7db0da2c2d98',
        QueryText=query_json["query"]
    )

    response = filter(
        lambda r: r["ScoreAttributes"]["ScoreConfidence"] in ["HIGH", "MEDIUM"], #replace list with item in input json
        response['ResultItems']
    );

    # return data


    return {
        'statusCode': 200,
        'body': json.dumps([response_mapper(r) for r in response])
    }
