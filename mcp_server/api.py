from fastapi import FastAPI, HTTPException
from typing import Optional, List, Dict
import os
import json
from contextlib import asynccontextmanager

from .tools.search_tools import SearchTools
from .tools.data_query import DataQueryTools
from .server import mcp  # Try to import the MCP object to mount it if possible, or just for tools

# Initialize tools
project_root = os.getenv("CONFIG_PATH", "/app/config").replace("/config/config.yaml", "")
if project_root == "/app/config": # Fallback if env var is just the config dir
     project_root = "/app"

search_tools = SearchTools(project_root)
data_tools = DataQueryTools(project_root)

app = FastAPI(title="TrendRadar API", version="1.0")

@app.get("/")
def read_root():
    return {"status": "ok", "service": "TrendRadar API"}

@app.get("/api/news/search")
def search_news(
    query: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    limit: int = 50,
    include_url: bool = True
):
    date_range = None
    if start_date and end_date:
        date_range = {"start": start_date, "end": end_date}

    try:
        # SearchTools returns a dict or list
        result = search_tools.search_news_unified(
            query=query,
            date_range=date_range,
            limit=limit,
            include_url=include_url
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/news/latest")
def get_latest_news(
    limit: int = 50,
    include_url: bool = True
):
    try:
        result = data_tools.get_latest_news(limit=limit, include_url=include_url)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Mount MCP if possible?
# FastMCP usually doesn't expose the raw app easily in the 0.x versions,
# but if we run this API, we provide REST.
# We can run the MCP server on a different port or same app if we knew how.
# For now, this REST API is sufficient for HAQTS.
