from constructs import Construct
from aws_cdk import (
    Duration,
    App, Stack,
    aws_iam as _iam,
    aws_lambda as _lambda,
    aws_apigateway as _apigw
)

class AwsBedrockApigLambdaPythonStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        base_lambda = _lambda.Function(self, 'AwsBedrockApigLambda',
                                       handler='lambda-handler.handler',
                                       runtime=_lambda.Runtime.PYTHON_3_9,
                                       timeout=Duration.seconds(300),
                                       code=_lambda.Code.from_asset('lambda'))

        # Lambda grant invoke to API Gateway
        base_lambda.grant_invoke(_iam.ServicePrincipal('apigateway.amazonaws.com'))


        base_api = _apigw.RestApi(self, 'BedrockApiGatewayWithCors',
                                  rest_api_name='BedrockApiGatewayWithCors', deploy=False)


        # setting up example entity
        claude2_entity = base_api.root.add_resource(
            'complete',
            default_cors_preflight_options=_apigw.CorsOptions(
                allow_methods=['GET', 'OPTIONS'],
                allow_origins=_apigw.Cors.ALL_ORIGINS)
        )
        claude2_entity_lambda_integration = _apigw.LambdaIntegration(
            base_lambda,
            proxy=True
        )
        # setting up GET method for example entity
        claude2_entity.add_method(
            'GET', claude2_entity_lambda_integration,
            method_responses=[
                _apigw.MethodResponse(
                    status_code="200",
                    response_parameters={
                        'method.response.header.Access-Control-Allow-Origin': True
                    }
                )
            ],
            api_key_required=True
        )
        # setting up POST method for example entity
        claude2_entity.add_method(
            'POST', claude2_entity_lambda_integration,
            method_responses=[
                _apigw.MethodResponse(
                    status_code="200",
                    response_parameters={
                        'method.response.header.Access-Control-Allow-Origin': True
                    }
                )
            ],
            api_key_required=True
        )

        # create an explicit Deployment construct
        deployment = _apigw.Deployment(self, 'Deployment', api=base_api)
        v1_stage = _apigw.Stage(self, 'v1Stage', deployment=deployment, stage_name='v1')
        base_api.deployment_stage = v1_stage

        # setup usage plan and key
        claude2_plan = base_api.add_usage_plan(
            "default"
        )
        claude2_key = base_api.add_api_key('apiKey')
        claude2_key2 = base_api.add_api_key('apiKey2')
        claude2_plan.add_api_key(claude2_key)
        claude2_plan.add_api_key(claude2_key2)
        claude2_plan.add_api_stage(
            stage=base_api.deployment_stage
        )


        # grant the lambda permission to invoke Bedrock AI models
        base_lambda.role.add_to_principal_policy(
            _iam.PolicyStatement(
                actions=['bedrock:InvokeModel'],
                resources=['arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-v2']
            )
        )