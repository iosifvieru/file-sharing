from fastapi import UploadFile, status, HTTPException
from client import s3_client

def upload_file_to_s3(files: list[UploadFile], bucket_name: str):
    if not files:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="No files provided")
    
    uploaded = []
    failed = []

    for file in files:
        result = s3_client.upload_to_s3(file=file, bucket_name=bucket_name)
        if result:
            uploaded.append(file.filename)
        else:
            failed.append(file.filename)

    if failed:
        raise HTTPException(status_code=500, detail={
            "message": "Some files failed to upload",
            "uploaded": uploaded,
            "failed": failed
        })
    
    return {
        "message": "Upload successful",
        "files": uploaded
    }