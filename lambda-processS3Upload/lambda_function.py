import json
import boto3
import urllib.parse
from datetime import datetime

sns_client = boto3.client('sns')
dynamodb = boto3.resource('dynamodb')

SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:750552037985:FileUploadNotifications'
DDB_TABLE = 'FileMetadata'

def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(record['s3']['object']['key'])
        size = record['s3']['object']['size']
        timestamp = datetime.utcnow().isoformat()
        uploader = key.split('/')[0]  # 'demo-user'

        # 1. Send SNS email
        message = f"A file was uploaded.\n\nUploader: {uploader}\nFile: {key}\nSize: {size} bytes\nTime: {timestamp}"
        sns_client.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject="New File Uploaded",
            Message=message
        )

        # 2. Save to DynamoDB
        table = dynamodb.Table(DDB_TABLE)
        table.put_item(Item={
            'file_key': key,
            'uploader': uploader,
            'size': size,
            'timestamp': timestamp
        })

    return {'statusCode': 200}