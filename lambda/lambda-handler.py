import boto3
import json
import logging
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
        body = event['body']
        if not verify_json_fields(body,
                                  ["prompt", "max_tokens_to_sample", "temperature"]):
            # other potential fields "top_p", "top_k", "stop_sequences"
            # log the error with body of the request
            logging.error(f'Invalid JSON body: {json.loads(body)}')
            # return a 400 Bad Request if the body does not contain the required fields
            return {
                'statusCode': 400,
                'body': f'Invalid JSON body: {body=}'
            }
        # take out the "model", "stream"  field in the body if it exists, and convert it back to string
        body_obj = json.loads(body)
        if "model" in body_obj:
            body_obj.pop("model")
        stream_enabled = False
        if "stream" in body_obj:
            stream_enabled = body_obj["stream"]
            body_obj.pop("stream")
        body_obj['anthropic_version'] = 'bedrock-2023-05-31'
        body = json.dumps(body_obj)

        modelId = 'anthropic.claude-v2'
        accept = 'application/json'
        contentType = 'application/json'
        response = bedrock.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)

        response_body = response.get('body').read().decode('utf-8')
        if stream_enabled:
            response_body = f'event: completion\ndata:{response_body}\n\n'

        return {
            'statusCode': 200,
            'body': response_body
        }
    return {
        'statusCode': 200,
        'body': f'Lambda was invoked successfully. {event=}, {context}'
    }

def verify_json_fields(json_string, fields):
    try:
        data = json.loads(json_string)
    except json.JSONDecodeError:
        return False

    return all(field in data for field in fields)