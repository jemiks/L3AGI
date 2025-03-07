from typing import Optional, Type
from pydantic import BaseModel, Field
from langchain.tools import DuckDuckGoSearchRun
from langchain.callbacks.manager import (
    CallbackManagerForToolRun,
)
from tools.base import BaseTool


class DuckDuckGoSearchSchema(BaseModel):
    query: str = Field(
        ...,
        description="The search query for DuckDuckGo search.",
    )


class DuckDuckGoSearchTool(BaseTool):
    name = "DuckDuckGo Search"
    
    description = (
        "A tool for performing a DuckDuckGo search and extracting snippets and webpages."
        "useful for when you need to answer questions about current events"
    )

    args_schema: Type[DuckDuckGoSearchSchema] = DuckDuckGoSearchSchema

    tool_id = "6b4cfbf9-8420-4e52-a6f0-384c82b1cc2b"

    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Search DuckDuckGo and return the results."""
        search = DuckDuckGoSearchRun()
        return search.run(query)

