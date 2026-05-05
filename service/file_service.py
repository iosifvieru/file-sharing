from fastapi import UploadFile, status, HTTPException
from concurrent.futures import ThreadPoolExecutor, as_completed
from client import s3_client
from uuid import uuid4

MAX_ALLOWED_UPLOAD_SIZE = 2_000_000_000 # bytes
MAX_ALLOWED_UPLOAD_SIZE_GB = MAX_ALLOWED_UPLOAD_SIZE / 10e8

def get_uploaded_files_size(uploaded_files: list[UploadFile]) -> int:
    file_sizes = 0

    for file in uploaded_files:
        file_sizes += file.size

    return file_sizes

def upload_file_to_s3(files: list[UploadFile], bucket_name: str):
    if not files:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="No files provided")

    if MAX_ALLOWED_UPLOAD_SIZE >= get_uploaded_files_size(files):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=f"Files are larger than {MAX_ALLOWED_UPLOAD_SIZE_GB} GB")

    uploaded = []
    failed = []

    unique_key = uuid4()

    with ThreadPoolExecutor(max_workers=min(len(files), 10)) as executor:
        futures = {
            executor.submit(s3_client.upload_to_s3, file, bucket_name, unique_key): file 
            for file in files
        }
        for future in as_completed(futures):
            filename, success = future.result()
            if success:
                uploaded.append(filename)
            else:
                failed.append(filename)

    if failed:
        raise HTTPException(status_code=500, detail={
            "message": "Some files failed to upload",
            "uploaded": uploaded,
            "failed": failed
        })
    
    return {
        "message": "Upload successful",
        "folder": unique_key,
        "files": uploaded
    }