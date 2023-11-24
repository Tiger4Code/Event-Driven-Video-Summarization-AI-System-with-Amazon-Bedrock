# Code snippets belong to www.youtube.com/@tiger4code channel

import json
import boto3
from datetime import datetime
OUTPUT_KEY = 'video-captions-text-content-files/'

def parse_transcript(response_uri):    
    split_uri = response_uri.split('/')
    bucket_name = split_uri[3]
    object_key = "/".join(split_uri[4:])

    s3 = boto3.client('s3', region_name='us-east-1')
    response = s3.get_object(Bucket=bucket_name, Key=object_key)
    json_response = response['Body'].read().decode('utf-8')
    # Parse the JSON response and extract the "transcript"
    parsed_json = json.loads(json_response)
    transcribed_text = parsed_json['results']['transcripts'][0]['transcript']
    print(f" transcribed_text= {transcribed_text}")   

    return transcribed_text 
    

def transcribe_audio(job_name, bucket, file_name, output_bucket_name, languageCode='en-US'):
    transcribe = boto3.client('transcribe', region_name='us-east-1')
    job_uri = f"s3://{bucket}/{file_name}"
    transcribe.start_transcription_job(
                                    TranscriptionJobName = job_name,
                                    Media = {
                                    'MediaFileUri': job_uri
                                    },
                                    OutputBucketName = bucket,
                                    OutputKey = OUTPUT_KEY,
                                    LanguageCode = 'en-US',
                                    Subtitles = {
                                    'Formats': [
                                    'vtt','srt'
                                    ],
                                    'OutputStartIndex': 1
                                    }
    )

    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break

    if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
        response_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
        transcribed_text = parse_transcript(response_uri)
        return transcribed_text
    else:
        return None


def lambda_handler(event, context):

    bucket = event['bucket']
    key = event['key']
    
    output_bucket_name = bucket
    
    job_name = "audio2text-transcribe-job-" + datetime.now().strftime("%Y%m%d%H%M%S")
    transcribed_text  = transcribe_audio(job_name=job_name, bucket=bucket, 
                                        file_name=key, 
                                        output_bucket_name=output_bucket_name, 
                                        languageCode='en-US')     

    output_key_name = f"{OUTPUT_KEY}{job_name}"
    output_video_text_key = f"{output_key_name}.json"
    output_video_caption_key = f"{output_key_name}.srt"
    return {
        'statusCode': 200,
        'text': transcribed_text, 
        'bucket':bucket, 
        'output_video_text_key': output_video_text_key,
        'output_video_caption_key': output_video_caption_key
    }