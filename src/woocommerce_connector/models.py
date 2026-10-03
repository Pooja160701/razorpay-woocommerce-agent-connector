from typing import Any
from pydantic import BaseModel


class PageInfo(BaseModel):
    page: int
    per_page: int
    total: int | None = None
    total_pages: int | None = None


class ToolResult(BaseModel):
    items: list[dict[str, Any]]
    page_info: PageInfo
