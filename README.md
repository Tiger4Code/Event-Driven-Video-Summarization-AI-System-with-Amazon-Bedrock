# Video Summarization System using Amazon Bedrock and AWS Services

This repository contains the code for an Event-Driven Video Summarization AI System built with Amazon Bedrock LLM and other AWS services. The system works as follows:

## System Workflow

1. **Event Trigger**: When a user uploads a video file to an S3 bucket, an event notification triggers a Lambda function.

2. **Step Function Execution**: The Lambda function initiates a Step Function, which comprises the following steps:
   - **Video Transcription**: Utilizes Amazon Transcribe to extract text and generate a caption file (.srt) from the video content.
   - **Video Summarization**: Utilizes Amazon Bedrock service, leveraging Claude LLM from Anthropic, to summarize the extracted text from the video.
   - **Text-to-Speech Conversion**: Employs Amazon Polly to convert the generated summary into an audio format.
   - **User Notification**: Uses Amazon SNS to send notifications to users via email, providing links to the output files stored in S3 (summary, caption file, audio file).

## Video Link

- [Watch the Video Demonstration](https://youtu.be/VOqbVIKzFog)

## Solution Architecture

<!-- Placeholder for Solution Architecture Diagram -->
![Video Summarization Solution Architecture](Audio-Chatbot-solution-architecture.png)

### Usage

### Requirements

- AWS account with access to Amazon S3, Amazon Transcribe, Amazon Polly, AWS Lambda, Amazon SNS, and AWS Step Functions.
- Python 3.10 and necessary dependencies installed for local testing.

For any questions or support, please contact us at www.youtube.com/@tiger4code by writing a comment under the following video [Creating an Event-Driven Video Summarization AI System with Amazon Bedrock #LLM and ML Services](https://youtu.be/VOqbVIKzFog).

## Instructions for Usage

1. Clone the repository.
2. Follow the setup steps outlined in the [Creating an Event-Driven Video Summarization AI System with Amazon Bedrock #LLM and ML Services (video)](https://youtu.be/VOqbVIKzFog) to configure and set up the necessary resources on the cloud.
2. Follow the setup steps outlined in the [Lambda Langchain Layer](2-Step-Function/2-Video-Summarization-using-LLM/LLM-Lambda-layer/README.md)

## Contribution

Contributions, bug reports, and feature requests are welcome. Feel free to open an issue or create a pull request.


## License

This project is licensed under the [MIT License](LICENSE).