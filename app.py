from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from aidercoder import AIDERCoder

from utils import parse_udiff, get_diff

app = FastAPI()

coder = AIDERCoder(
    model_name="openai/o1-mini-2024-09-12",
    auto_commits=False,
    edit_format="diff"
)

class UpdateRequest(BaseModel):
    repo_path: str
    fnames: list

class EditRequest(BaseModel):
    repo_path: str
    text_request: str

@app.post("/update")
async def update_aidercoder(request: UpdateRequest):
    repo_path = request.repo_path
    fnames = request.fnames
    try:
        coder.update_repo(repo_path=repo_path, fnames=fnames)
        return {
            "status": "success",
            "message": f"AIDERCoder updated for repository at {repo_path}"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@app.post("/edit_code")
async def edit_code(request: EditRequest):
    try:
        message = coder.run(request.text_request)
        diff = get_diff(message)
        changes = parse_udiff(diff)
        return {
            "status": "success",
            "message": message,
            "changes": changes
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "changes": None
        }