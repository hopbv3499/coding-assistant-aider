from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from aidercoder import AIDERCoder

import os

from dotenv import load_dotenv

load_dotenv()

from utils import parse_udiff, get_diff

app = FastAPI()

coder = AIDERCoder(
    model_name="openai/o1-preview-2024-09-12",
    auto_commits=False,
    edit_format="udiff",
    repo_path=os.environ["REPO_PATH"]
)

class UpdateRequest(BaseModel):
    fnames: list

class EditRequest(BaseModel):
    text_request: str

@app.post("/update")
async def update_aidercoder(request: UpdateRequest):
    fnames = request.fnames
    try:
        coder.update_repo(fnames=fnames)
        return {
            "status": "success",
            "message": f"AIDERCoder updated for repository with files: {fnames}"
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