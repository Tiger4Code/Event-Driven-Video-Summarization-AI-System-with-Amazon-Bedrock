import json
import os
import sys
import boto3
from utils import bedrock, print_ww
SUMMARIZED_TEXT_KEY = 'video_summary_text'

# load video extracted text from s3
def load_json_from_s3(s3client, bucket, file_key):
    try: 
        response = s3client.get_object(Bucket=bucket, Key=file_key)
        json_response = response['Body'].read().decode('utf-8')
        parsed_json = json.loads(json_response)
        transcribed_text = parsed_json['results']['transcripts'][0]['transcript']
        return transcribed_text
    except Exception as e:
        print(f"Error loading JSON from s3: {e}")
        return None
        
def upload_text_to_s3(s3client, bucket, file_key, text):
    try: 
        s3client.put_object(Bucket=bucket, Key=file_key, Body=text)
        print(f"Text uploaded to {file_key} in bucket {bucket}")
    except Exception as e: 
        print(f"Error uploading text content to S3: {e}")
    
def lambda_handler(event, context):
    s3client = boto3.client('s3')
    bucket = event['bucket']
    output_video_text_key = event['output_video_text_key']
    file_name_no_ext = '.'.join(output_video_text_key.split('/')[-1].split('.')[:-1])
    transcriped_text = load_json_from_s3(s3client=s3client, bucket=bucket, file_key=output_video_text_key)
        
    prompt = f"""
Human: Please provide a summary of the following text.
<text>
 {transcriped_text}
</text>
Assistant:"""
    module_path = ".."
    sys.path.append(os.path.abspath(module_path))
 
    boto3_bedrock = bedrock.get_bedrock_client(
        region="us-east-1"
    )    
    # Prepare prompt to feed to LLM         
    body = json.dumps({"prompt": prompt,
                 "max_tokens_to_sample":4096,
                 "temperature":0.5,
                 "top_k":250,
                 "top_p":0.5,
                 "stop_sequences":[]
                  }) 
                  
    # Invoke foundation model via Boto3
    modelId = 'anthropic.claude-v2' # change this to use a different version from the model provider
    accept = 'application/json'
    contentType = 'application/json'
    
    response = boto3_bedrock.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)
    response_body = json.loads(response.get('body').read())
    try:
        summarized_text = response_body.get('completion')
        summarized_text_file_key = f"{SUMMARIZED_TEXT_KEY}/{file_name_no_ext}.txt"
        upload_text_to_s3(s3client=s3client, bucket=bucket, file_key=summarized_text_file_key, text=summarized_text)
        
    except ValueError as error:
        if  "AccessDeniedException" in str(error):
            print(f"\x1b[41m{error}\
            \nTo troubeshoot this issue please refer to the following resources.\
            \nhttps://docs.aws.amazon.com/IAM/latest/UserGuide/troubleshoot_access-denied.html\
            \nhttps://docs.aws.amazon.com/bedrock/latest/userguide/security-iam.html\x1b[0m\n")      
            class StopExecution(ValueError):
                def _render_traceback_(self):
                    pass
            raise StopExecution        
        else:
            raise error
    return {
        'statusCode': 200,
        'text': summarized_text,
        'bucket': bucket, 
        'key': summarized_text_file_key
    }