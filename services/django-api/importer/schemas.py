from pydantic import BaseModel, HttpUrl


class GoogleDriveImportRequest(BaseModel):
    url: HttpUrl
