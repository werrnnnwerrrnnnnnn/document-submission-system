import json
import boto3
import os
import uuid
from datetime import datetime, timedelta

s3_client = boto3.client('s3')
BUCKET_NAME = 'doc-submission-bucket'

def lambda_handler(event, context):
    file_name = event['queryStringParameters']['filename']
    fake_user = event['queryStringParameters'].get('user', 'anonymous')

    key = f"{fake_user}/{uuid.uuid4()}_{file_name}"

    presigned_url = s3_client.generate_presigned_url(
        'put_object',
        Params={'Bucket': BUCKET_NAME, 'Key': key},
         ExpiresIn=604800  # 7 days in seconds
    )

    return {
        'statusCode': 200,
        'body': json.dumps({'upload_url': presigned_url, 'file_key': key}),
        'headers': {'Content-Type': 'application/json'}
    }