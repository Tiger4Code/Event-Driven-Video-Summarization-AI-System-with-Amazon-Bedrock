# Lambda Layer Creation

This guide will help you create a Lambda layer compressed file for Python 3.10. Please follow the steps below:

1. **Set up a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2. **Create a directory for Python packages:**
    ```bash
    mkdir python
    cd python
    ```

3. **Install required packages:**
    ```bash
    pip install \
    --platform manylinux2014_x86_64 \
    --target=package \
    --implementation cp \
    --python-version 3.10 \
    --only-binary=:all: --upgrade \
    -r ../requirements.txt -t .
    ```

4. **Remove unnecessary files:**
    ```bash
    rm -rf *dist-info
    cd ..
    ```

5. **Compress the directory into a zip file:**
    ```bash
    zip -r archive.zip python
    ```

6. **Upload the compressed file to an S3 bucket (e.g., lambda-archive):**
    ```bash
    aws s3 cp archive.zip s3://lambda-archive/
    ```

## Creating a Lambda Layer

After uploading the compressed file to the S3 bucket, follow the steps below to create a Lambda layer:

1. Open the AWS Management Console and go to the Lambda service.
2. Navigate to Layers and click "Create layer."
3. Provide a name and description for the layer.
4. Choose the S3 location where the zip file is stored.
5. Specify the compatible runtimes (Python 3.10).
6. Add a custom policy if necessary.
7. Click "Create."

## Adding an Existing Layer to a Lambda Function

To add an existing Lambda layer to a Lambda function, follow these steps:

1. Open the AWS Management Console and go to the Lambda service.
2. Select the Lambda function to which you want to add the layer.
3. In the function's configuration, scroll down to the "Layers" section.
4. Click "Add a layer."
5. Choose an existing layer from the list of available layers (Custom Layer).
6. Configure the desired version if multiple versions are available.
7. Click "Add."

Your Lambda function is now equipped with the selected layer.
