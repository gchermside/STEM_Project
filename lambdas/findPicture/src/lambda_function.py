import json
from library import two

def lambda_handler(event, context):
    # TODO implement

    print(f"the event is {event}")
    landmarks = event['body']
    print(landmarks)
    print(two())


    return {
        'statusCode': 200,
        'body': json.dumps({"bestGuess": "f"}),
        'headers': {
            "Access-Control-Allow-Origin" : "*",
        }
    }
