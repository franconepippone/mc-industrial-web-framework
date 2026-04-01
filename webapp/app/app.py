from pathlib import Path
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


from mc_version_fetcher import get_minecraft_versions
from repo_interface import RepoInterface
from filtering import FilterRequest, filter_design_specs, build_results_summary

import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

token = os.getenv("GITHUB_TOKEN")
repo = RepoInterface(token)
repo.load_design_specs()
app = FastAPI()

# Templates folder
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

versions_java, versions_bedrock = get_minecraft_versions()
print("got java and bedrock versions")

github_repo_url = f"https://github.com/{repo.REPO_NAME}"
downgit_base_url = "https://downgit.github.io/#/home?url="

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    default_filters = FilterRequest()
    results = filter_design_specs(repo.design_specs, default_filters)

    return templates.TemplateResponse(
        request,
        "index.html",
        context={
            "versions_java": versions_java,
            "versions_bedrock": versions_bedrock,
            "github_repo_url": github_repo_url,
            "downgit_base_url": downgit_base_url,
            "specs": results,
            "results_summary": build_results_summary(default_filters, len(results)),
        },
    )


@app.post("/filter", response_class=HTMLResponse)
async def filter_items(request: Request, filters: FilterRequest):
    results = filter_design_specs(repo.design_specs, filters)
    return templates.TemplateResponse(
        request,
        "partials/device_results.html",
        context={
            "github_repo_url": github_repo_url,
            "downgit_base_url": downgit_base_url,
            "specs": results,
            "results_summary": build_results_summary(filters, len(results)),
        },
    )