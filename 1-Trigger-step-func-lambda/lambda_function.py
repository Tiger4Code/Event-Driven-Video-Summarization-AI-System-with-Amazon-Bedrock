# Code snippets belong to www.youtube.com/@tiger4code channel

import boto3
import uuid
import datetime
import os

# Get the current date and time
current_time = datetime.datetime.now()
# Format the timestamp as a string
timestamp = current_time.strftime("%Y-%m-%d_%H-%M-%S")


def generate_state_machine_name():
    random_string = str(uuid.uuid4())[:8]  # Get the first 8 characters of the UUID
    state_machine_name = f"MyStateMachine-{random_string}"
    return state_machine_name
    
def lambda_handler(event, context):
    # Extract the necessary information from the S3 event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']
    
    state_machine_arn = os.environ['STATE_MACHINE_ARN']
    execution_name =  generate_state_machine_name()
    input_data = '{"bucket": "%s", "key": "%s"}' % (bucket_name, object_key)

    # Start the Step Functions execution
    stepfunctions = boto3.client('stepfunctions')
    response = stepfunctions.start_execution(
        stateMachineArn=state_machine_arn,
        name=execution_name,
        input=input_data
    )

    return {
        'statusCode': 200,
        'body': 'Step Functions execution started.'
    }
    