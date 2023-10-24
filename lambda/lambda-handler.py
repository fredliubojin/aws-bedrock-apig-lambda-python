import boto3
import json
bedrock = boto3.client(service_name='bedrock-runtime')

def handler(event, context):
    # if the method is GET, return a 200 OK with a message
    if event['httpMethod'] == 'GET':
        return {
            'statusCode': 200,
            'body': 'Lambda was invoked successfully through GET.'
        }
    if event['httpMethod'] == 'POST':
        # if the method is POST, retrieve the body of the request
        prompt = event['body']
        body = json.dumps({
            "prompt": f"\n\nHuman:{prompt}\n\nAssistant:",
            "max_tokens_to_sample": 300,
            "temperature": 0.1,
            "top_p": 0.9,
            "stop_sequences": [ "\\n\\nHuman:"]
        })

        modelId = 'anthropic.claude-v2'
        accept = 'application/json'
        contentType = 'application/json'

        response = bedrock.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)

        response_body = json.loads(response.get('body').read())
        # text
        # completion = response_body.get('completion')

        return {
            'statusCode': 200,
            'body': f'{response_body}'
        }
    return {
        'statusCode': 200,
        'body': f'Lambda was invoked successfully. {event=}, {context}'
    }