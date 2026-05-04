from fastapi import APIRouter, HTTPException, status, UploadFile
from service import file_service
from client import s3_client

router = APIRouter()

@router.post("/upload")
async def upload_file(files: list[UploadFile]):
    result = file_service.upload_file_to_s3(files, s3_client.BUCKET_NAME)
    return result

@router.get("/download/:token")
async def download_file(token):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")

@router.get("/files/:id/status")
async def get_files_status(id):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")
