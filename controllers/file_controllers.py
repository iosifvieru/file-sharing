from fastapi import APIRouter, HTTPException, status

router = APIRouter()

@router.post("/upload")
async def upload_file():
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")

@router.get("/download/:token")
async def download_file(token):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")

@router.get("/files/:id/status")
async def get_files_status(id):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")
