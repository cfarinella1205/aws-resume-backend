import json
import boto3
import os

# Initialize the DynamoDB client outside the handler for better performance
dynamodb = boto3.resource('dynamodb')
# Matches the TableName defined in your template.yaml
table_name = os.environ.get('DATABASE_TABLE_NAME', 'CloudResumeCounter')
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        # Atomically increment the 'visit_count' for the 'visitors' item
        # This prevents race conditions if two people visit at the same time
        response = table.update_item(
            Key={'id': 'visitors'},
            UpdateExpression="SET visit_count = if_not_exists(visit_count, :start) + :inc",
            ExpressionAttributeValues={
                ':inc': 1,
                ':start': 0
            },
            ReturnValues="UPDATED_NEW"
        )

        # Get the new count from the response
        count = response['Attributes']['visit_count']

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET,OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": json.dumps({
                "count": int(count)
            })
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET,OPTIONS"
            },
            "body": json.dumps({"error": "Internal Server Error"})
        }