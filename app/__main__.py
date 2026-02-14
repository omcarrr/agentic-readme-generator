from fastapi import FastAPI
import uvicorn
from app.models import ReadmeRequest, ReadmeResponse
from app.agents import run_readme_agent

app = FastAPI(title="Nasiko README Generation Agent API")

@app.post("/generate-readme", response_model=ReadmeResponse)
def generate_readme_endpoint(payload: ReadmeRequest):
    try:
        readme_md = run_readme_agent(payload.folder_path)
        return ReadmeResponse(readme_content=readme_md, status="success")
    except Exception as e:
        return ReadmeResponse(readme_content=str(e), status="error")

if __name__ == "__main__":
    # Allows the script to be run directly via `python app/__main__.py`
    uvicorn.run("app.__main__:app", host="0.0.0.0", port=8000, reload=True)