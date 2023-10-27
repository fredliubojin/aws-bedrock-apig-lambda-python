# REST Endpoint for Anthropic Claude2 on AWS Bedrock

Welcome to the AWS Bedrock APIG Lambda Python project! This project sets up a REST endpoint that exposes the dedicated Anthropic Claude2 model on Bedrock in your own AWS account. It uses API Gateway with Lambda to invoke the AWS Bedrock Claude2 Anthropic LLM model, with complete privacy and data protection in mind.

## Features

1. Expose AWS Bedrock Claude2 Anthropic model through a REST endpoint on AWS.
2. Enterprise level data security and privacy (your data remains in your AWS account, never goes to any 3rd party service)
2. REST API is compatible with the official Anthropic API.
3. Serverless setup (no need to pay if you don't use it).
4. Automatic and secure API key provisioning, with configurable usage plan capability (per key throttling, quota, etc.).
5. Infrastructure as Code (IaC) setup using AWS Cloud Development Kit (CDK).

## Prerequisites

Before you can deploy the code, you need to:

1. Install and configure AWS CLI
2. Install CDK
3. Enable Bedrock Claude2 model in AWS console
4. Set up a Lambda Layer in Python with the latest boto3 library.

## Installation

### AWS CLI

To install AWS CLI, follow the official instruction [here](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

### Configure AWS CLI
```
aws configure
```

### AWS CDK

Install AWS CDK by running the following command:

```bash
npm install -g aws-cdk
```

### Enable Bedrock Claude2 Model

Go to AWS console and enable Bedrock Claude2 model.

### Set Up Lambda Layer

You can set up a Lambda Layer in Python with the latest boto3 library by running the following commands:

```bash
mkdir python
pip install boto3 -t python/
zip -r my-python-lib.zip python/
aws lambda publish-layer-version --layer-name my-python-lib --zip-file fileb://my-python-lib.zip
```

This will create a new directory named "python", install the latest boto3 library into it, package the directory into a zip file, and publish the layer to AWS Lambda.

Make sure to note down the ARN of the layer version returned by the last command. You will need it in the next step.

## Deployment

To deploy the code to AWS, follow these steps:

1. Clone the repository:

```bash
git clone https://github.com/yourusername/aws-bedrock-apig-lambda-python.git
```

2. Navigate to the repository:

```bash
cd aws-bedrock-apig-lambda-python
```

3. Install the necessary dependencies:

```bash
pip install -r requirements.txt
```

4. Synthesize the CloudFormation template for this code:

```bash
cdk synth
```

5. Deploy the stack to AWS:

```bash
cdk deploy
```

This command deploys the stack and outputs the URL of the deployed API Gateway.

6. Configure the Lambda function to use the layer:

```bash
aws lambda update-function-configuration --function-name YourFunctionName --layers YourLayerARN
```

Replace `YourFunctionName` with the name of your Lambda function and `YourLayerARN` with the ARN of the layer version you noted down earlier.

You could also manually add the layer to your lambda using the AWS Console.

## Usage

After deployment, please retrieve the API Gateway endpoint from your AWS console. Also you would need to retrieve the auto provisioned API key from the API Gateway console. You can invoke your endpoint with the followig command
```
curl --header "x-api-key: <Your-API-Key>" \
     -X POST \
     -H "Content-Type: application/json" \
     -d '{
          "prompt": "\n\nHuman: Please tell me a joke.\n\nAssistant:",
          "max_tokens_to_sample": 300,
          "temperature": 0.5,
          "top_k": 250,
          "top_p": 1,
          "stop_sequences": ["\n\nHuman:"],
          "anthropic_version": "2023-06-01"
         }' \
     https://<Your-API-Endpoint>/v1/complete
```
Please replace <Your-API-Key> with your actual API key and <Your-API-Endpoint> with your actual API endpoint.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!