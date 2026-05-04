import os
import io
import boto3
from botocore.exceptions import ClientError
from fastapi.responses import StreamingResponse

BUCKET_NAME = os.getenv("BUCKET_NAME", "mybucket")
S3_ENDPOINT = os.getenv("S3_ENDPOINT", "localhost:9000")
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY", "admin")
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY", "adminStrong")

s3 = boto3.client(
    "s3",
    endpoint_url=f"http://{S3_ENDPOINT}",
    aws_access_key_id=S3_ACCESS_KEY,
    aws_secret_access_key=S3_SECRET_KEY,
    region_name="us-east-1"
)

def create_bucket(bucket_name):
    try:
        s3.head_bucket(Bucket=bucket_name)
    except ClientError:
        s3.create_bucket(Bucket=bucket_name)

def upload_to_s3(file, bucket_name):
    try:
        file.file.seek(0)
        s3.upload_fileobj(file.file, bucket_name, file.filename)
        return file.filename, True
    except ClientError as e:
        print(e)
        return file.filename, False

def download_from_s3(filename, bucket_name):
    try:
        fileobj = io.BytesIO()
        s3.download_fileobj(bucket_name, filename, fileobj)
        fileobj.seek(0)
        return StreamingResponse(fileobj, media_type="application/octet-stream")
    except ClientError as e:
        print(e)
        return None