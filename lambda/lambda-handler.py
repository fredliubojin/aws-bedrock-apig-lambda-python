import boto3
import json
import logging

bedrock = boto3.client(service_name='bedrock-runtime')
modelId = 'anthropic.claude-v2'
accept = 'application/json'
contentType = 'application/json'

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    http_method = event.get('httpMethod')

    if http_method == 'GET':
        return _handle_get_request()
    elif http_method == 'POST':
        return _handle_post_request(event)
    else:
        return _handle_unsupported_http_method(http_method)

def _handle_get_request():
    return _create_response(200, 'Lambda was invoked successfully through GET.')

def _handle_post_request(event):
    body = event.get('body')
    if not _is_valid_json_body(body, ["prompt", "max_tokens_to_sample", "temperature"]):
        logger.error(f'Invalid JSON body: {json.loads(body)}')
        return _create_response(400, f'Invalid JSON body: {body=}')

    body_obj, stream_enabled = _process_body(body)
    response = _invoke_model(body_obj)

    if stream_enabled:
        response = f'event: completion\ndata:{response}\n\n'

    return _create_response(200, response)

def _handle_unsupported_http_method(http_method):
    logger.error(f'Unsupported HTTP method: {http_method}')
    return _create_response(400, f'Unsupported HTTP method: {http_method}')

def _is_valid_json_body(json_string, fields):
    try:
        data = json.loads(json_string)
    except json.JSONDecodeError:
        return False

    return all(field in data for field in fields)

def _process_body(body):
    body_obj = json.loads(body)
    body_obj.pop("model", None)
    stream_enabled = body_obj.pop("stream", False)
    body_obj['anthropic_version'] = 'bedrock-2023-05-31'

    return json.dumps(body_obj), stream_enabled

def _invoke_model(body):
    response = bedrock.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)
    return response.get('body').read().decode('utf-8')

def _create_response(status_code, body):
    return {
        'statusCode': status_code,
        'body': body
    }