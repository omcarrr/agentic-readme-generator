from pydantic import BaseModel

class ReadmeRequest(BaseModel):
    folder_path: str

class ReadmeResponse(BaseModel):
    readme_content: str
    status: str