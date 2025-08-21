from typing import List, Dict, Any, Callable
from dataclasses import dataclass

from .user import get_user_info
from .guild import get_guild_info
from .messages import send_message
from .search import search_web
from .calculator import multiply, add
from langchain_core.tools import BaseTool

@dataclass
class ToolConfig:
    tool: BaseTool
    executing_message: str
    category: str = "general"

def get_tools() -> List[ToolConfig]:
    return [
        ToolConfig(
            tool=multiply,
            executing_message="Multiplying numbers...",
            category="math"
        ),
        ToolConfig(
            tool=add,
            executing_message="Adding numbers...",
            category="math"
        ),
        ToolConfig(
            tool=get_guild_info,
            executing_message="Getting guild information...",
            category="guild"
        ),
        ToolConfig(
            tool=get_user_info,
            executing_message="Getting user information...",
            category="user"
        ),
        ToolConfig(
            tool=send_message,
            executing_message="Sending a message...",
            category="utility"
        )
    ]

def get_tool_config(tool_name:str) -> ToolConfig:
    return next((t for t in get_tools() if t.tool.name == tool_name))