import json
import boto3
import os

# Initialize the DynamoDB resource
dynamodb = boto3.resource('dynamodb')
# The TableName will be passed in from our SAM template
table_name = os.environ.get('VISITOR_TABLE', 'CloudResumeCounter')
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    # Update the item with id 'visitors'. If it doesn't exist, it creates it.
    response = table.update_item(
        Key={'id': 'visitors'},
        UpdateExpression='ADD visit_count :inc',
        ExpressionAttributeValues={':inc': 1},
        ReturnValues='UPDATED_NEW'
    )
    
    count = response['Attributes']['visit_count']

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET"
        },
        "body": json.dumps({"count": int(count)})
    }