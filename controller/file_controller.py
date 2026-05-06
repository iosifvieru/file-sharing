from fastapi import APIRouter, UploadFile, Form
from service import file_service, message_service
from client import s3_client

router = APIRouter()

@router.post("/upload")
async def upload_file(files: list[UploadFile], emails: list[str] = Form(...)):
    result = file_service.upload_file_to_s3(files, s3_client.BUCKET_NAME)

    unique_key = result["unique_key"]
    if unique_key:
        message_service.publish_message_to_all_participants(emails, unique_key)

    return result

@router.get("/download/{uuid}/{filename}")
async def download_file(uuid: str, filename: str):
    return file_service.download_file_from_s3(uuid, filename)

@router.get("/files/{uuid}")
async def get_files_informations(uuid: str):
    return file_service.get_files_informations(uuid)
