import os
import io
import boto3
from botocore.exceptions import ClientError
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv

load_dotenv()

BUCKET_NAME = os.getenv("BUCKET_NAME", "mybucket")

s3 = boto3.client("s3")

def create_bucket(bucket_name):
    try:
        s3.head_bucket(Bucket=bucket_name)
    except ClientError:
        s3.create_bucket(Bucket=bucket_name)

def upload_to_s3(file, bucket_name, folder:str = "temp"):
    try:
        file.file.seek(0)

        object_key = f"{folder}/{file.filename}"
        s3.upload_fileobj(file.file, bucket_name, object_key)
        return object_key, True
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
    
def check_file_exists(s3_key: str, bucket_name: str = BUCKET_NAME) -> bool:
    try:
        s3.head_object(Bucket=bucket_name, Key=s3_key)
        return True
    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            return False
        
def list_files(prefix: str, bucket_name: str = BUCKET_NAME) -> list[dict]:
    try:
        paginator = s3.get_paginator("list_objects_v2")

        files = []
        for page in paginator.paginate(Bucket=bucket_name, Prefix=prefix):
            for obj in page.get("Contents", []):
                files.append({
                    "key": obj["Key"],
                    "filename": obj["Key"].split("/")[-1],
                    "size": obj["Size"],
                    "last_modified": obj["LastModified"].isoformat(),
                    "etag": obj["ETag"].strip('"'),
                })

        return files

    except ClientError as e:
        print(e)
        return []
