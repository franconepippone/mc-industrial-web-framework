from pathlib import Path
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from mc_version_fetcher import get_minecraft_versions
from repo_interface import RepoInterface

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

class FilterRequest(BaseModel):
    device_class: str = "rds-router"
    edition: str | None = None
    version_from: str | None = None
    version_to: str | None = None
    protocol: str | None = None
    package_tech: str | None = None
    min_throughput: int | None = None
    min_physical_input: int | None = None
    min_physical_output: int | None = None
    max_length: int | None = None
    max_width: int | None = None
    max_height: int | None = None
    survival_friendliness: str | None = None
    works_in_nether: bool | None = None
    queue_included: bool | None = None
    chunkloading_included: bool | None = None
    hierarchical_routing: bool | None = None
    non_directional: bool | None = None
    non_locational: bool | None = None


def compare_versions(left: str, right: str) -> int:
    left_parts = [int(part) for part in str(left).split(".")]
    right_parts = [int(part) for part in str(right).split(".")]
    max_length = max(len(left_parts), len(right_parts))

    for index in range(max_length):
        left_value = left_parts[index] if index < len(left_parts) else 0
        right_value = right_parts[index] if index < len(right_parts) else 0
        if left_value > right_value:
            return 1
        if left_value < right_value:
            return -1

    return 0


def meets_minimum(value: Any, minimum: int | None) -> bool:
    if minimum is None:
        return True
    if value is None:
        return False
    if isinstance(value, int):
        return value >= minimum

    value_str = str(value).strip()
    if value_str.isdigit():
        return int(value_str) >= minimum

    return True


def within_maximum(value: Any, maximum: int | None) -> bool:
    if maximum is None:
        return True
    if value is None:
        return False
    if isinstance(value, int):
        return value <= maximum

    value_str = str(value).strip()
    if value_str.isdigit():
        return int(value_str) <= maximum

    return True


def format_device_class(device_class: str) -> str:
    return device_class.replace("rds-", "RDS ").replace("-", " ").title()


def build_results_summary(filters: FilterRequest, count: int) -> str:
    summary_parts = [format_device_class(filters.device_class)]

    if filters.edition:
        summary_parts.append(f"Edition: {filters.edition}")
    if filters.version_from:
        summary_parts.append(f"From {filters.version_from}")
    if filters.version_to:
        summary_parts.append(f"To {filters.version_to}")
    if filters.protocol:
        summary_parts.append(f"Protocol: {filters.protocol}")
    if filters.package_tech:
        summary_parts.append(f"Tech: {filters.package_tech}")
    if filters.min_throughput is not None:
        summary_parts.append(f"Min throughput: {filters.min_throughput}")

    prefix = f"Showing {count} result" + ("" if count == 1 else "s") if count > 0 else "No results match the current selection"
    return f"{prefix} · {' · '.join(summary_parts)}"


def filter_design_specs(filters: FilterRequest) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []

    for spec in repo.design_specs:
        spec_device_class = getattr(spec.device_class, "value", spec.device_class)
        if filters.device_class and spec_device_class != filters.device_class:
            continue

        if filters.edition and spec.minecraft.edition not in (filters.edition, "Any"):
            continue

        if filters.version_from and compare_versions(spec.minecraft.upper, filters.version_from) < 0:
            continue

        if filters.version_to and compare_versions(spec.minecraft.lower, filters.version_to) > 0:
            continue

        if filters.survival_friendliness and spec.survival_friendliness != filters.survival_friendliness:
            continue

        if filters.works_in_nether and not spec.works_in_nether:
            continue

        if filters.non_directional and spec.directional:
            continue

        if filters.non_locational and spec.locational:
            continue

        if filters.device_class == "rds-router":
            if filters.protocol and getattr(spec, "protocol", None) != filters.protocol:
                continue

            if filters.package_tech and getattr(spec, "package_tech", "").lower() != filters.package_tech.lower():
                continue

            if filters.min_throughput is not None and getattr(spec, "throughput", 0) < filters.min_throughput:
                continue

            physical_ports = getattr(spec, "physical_ports", {}) or {}
            if not meets_minimum(physical_ports.get("input"), filters.min_physical_input):
                continue
            if not meets_minimum(physical_ports.get("output"), filters.min_physical_output):
                continue

            footprint = getattr(spec, "footprint", None)
            if footprint is not None:
                if not within_maximum(footprint.length, filters.max_length):
                    continue
                if not within_maximum(footprint.width, filters.max_width):
                    continue
                if not within_maximum(footprint.height, filters.max_height):
                    continue

            if filters.queue_included and not getattr(spec, "package_queue_included", False):
                continue

            if filters.chunkloading_included and not getattr(spec, "chunkloading_included", False):
                continue

            if filters.hierarchical_routing and not getattr(spec, "supports_hierarchical_routing", False):
                continue

        results.append(spec.model_dump(mode="json"))

    return sorted(results, key=lambda item: item.get("name", "").lower())


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    default_filters = FilterRequest()
    results = filter_design_specs(default_filters)

    return templates.TemplateResponse(
        request,
        "index.html",
        context={
            "versions_java": versions_java,
            "versions_bedrock": versions_bedrock,
            "github_repo_url": github_repo_url,
            "specs": results,
            "results_summary": build_results_summary(default_filters, len(results)),
        },
    )


@app.post("/filter", response_class=HTMLResponse)
async def filter_items(request: Request, filters: FilterRequest):
    results = filter_design_specs(filters)
    return templates.TemplateResponse(
        request,
        "partials/device_results.html",
        context={
            "github_repo_url": github_repo_url,
            "specs": results,
            "results_summary": build_results_summary(filters, len(results)),
        },
    )