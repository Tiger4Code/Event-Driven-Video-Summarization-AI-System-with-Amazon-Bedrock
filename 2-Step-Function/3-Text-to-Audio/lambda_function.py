# Code snippets belong to www.youtube.com/@tiger4code channel
import boto3
def gen_filename():
    import datetime

    # Get the current date and time
    current_time = datetime.datetime.now()

    # Format the timestamp as a string
    timestamp = current_time.strftime("%Y-%m-%d_%H-%M-%S")

    # Create a file name with the timestamp
    file_name = f"polly_audio_{timestamp}.mp3"  # Adjust the prefix and file extension as needed

    # print("Generated file name:", file_name)
    return file_name   
# load video extracted text from s3
def load_text_from_s3(s3client, bucket, file_key):
    
    try: 
        response = s3client.get_object(Bucket=bucket, Key=file_key)
        text_content = response['Body'].read().decode('utf-8')
        return text_content
    except Exception as e:
        print(f"Error loading text from s3: {e}")
        return None
        
def lambda_handler(event, context):
    # text = event['text']
    voice_id = event.get('voice_id', 'Joanna')  # Default voice_id is Joanna
    bucket = event['bucket']  # Replace with your S3 bucket name
    summarized_text_key = event['key'] # where the summarized text file is stored 
    
    s3client = boto3.client('s3')
    text = load_text_from_s3(s3client=s3client, bucket=bucket, file_key=summarized_text_key)
    
    file_name_no_ext = '.'.join(summarized_text_key.split('/')[-1].split('.')[:-1])
    file_name = f"{file_name_no_ext}.mp3" #  gen_filename()
    s3_key = f"polly-audio/{file_name}" 
    
    polly = boto3.client('polly')
    s3 = boto3.client('s3')

    response = polly.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        # OutputFormat="pcm",
        VoiceId=voice_id
    )

    s3.put_object(
        Bucket=bucket,
        Key=s3_key,
        Body=response['AudioStream'].read()
    )

    return {
        'statusCode': 200,
        'bucket': bucket, 
        'summarized_text_key': summarized_text_key,
        'key': s3_key, 
    }