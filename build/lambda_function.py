import json
import boto3
from boto3.dynamodb.conditions import Key

db = boto3.resource('dynamodb')

table = db.Table('visitortbl')

def lambda_handler(event, context):
    
    try: 
        response = table.get_item(
            Key={
                'ID' : 'vis1',
            }    
        )
    
        visitorCount = response['Item']['num']

    except:

        table.put_item(
            Item={
                'ID': 'vis1',
                'num': 0,
            }
        )

        visitorCount = 0
    
    table.update_item(
        Key={
            'ID' : 'vis1',
        },
        UpdateExpression="set num = :i",
        ExpressionAttributeValues={
            ':i' : visitorCount + 1
        },
        ReturnValues="UPDATED_NEW"
    )
    
    strVisitorCount = str(visitorCount)
    
    print("In lambda handler")
    
    resp = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
        },
        "body": strVisitorCount
    }

    return resp