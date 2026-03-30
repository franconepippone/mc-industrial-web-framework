from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from mc_version_fetcher import get_minecraft_versions
from spec_schemas import BaseDeviceSpec

from repo_interface import RepoInterface

import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("GITHUB_TOKEN")
repo = RepoInterface(token)
repo.load_design_specs()
specs_dicts = [spec.model_dump(mode="json") for spec in repo.design_specs]
app = FastAPI()

# Templates folder
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

versions_java, versions_bedrock = get_minecraft_versions()
print("got java and bedrock versions")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # Convert Pydantic objects to JSON-friendly dicts for rendering in the template
    
    print(specs_dicts[0]["specsheet_url"])
    return templates.TemplateResponse(
        request,
        "index.html",
        context={
            "specs": specs_dicts,
            "versions_java": versions_java,
            "versions_bedrock": versions_bedrock
        }
    )