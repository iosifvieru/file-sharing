from fastapi import UploadFile, status, HTTPException
from concurrent.futures import ThreadPoolExecutor, as_completed
from client import s3_client

def upload_file_to_s3(files: list[UploadFile], bucket_name: str):
    if not files:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="No files provided")
    
    uploaded = []
    failed = []

    with ThreadPoolExecutor(max_workers=min(len(files), 10)) as executor:
        futures = {
            executor.submit(s3_client.upload_to_s3, file, bucket_name): file 
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
        "files": uploaded
    }