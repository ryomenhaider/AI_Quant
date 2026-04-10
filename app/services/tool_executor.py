import importlib
import logging
from typing import Any

from app.services.tool_registry import TOOL_MAP

logger = logging.getLogger(__name__)


def execute_tool(name: str, arguments: dict) -> dict:
    if name not in TOOL_MAP:
        return {"status": "error", "error": f"Unknown tool: {name}"}

    logger.info(f"Executing tool: {name} with args: {arguments}")

    try:
        module_path, function_name = TOOL_MAP[name].rsplit(".", 1)
        module = importlib.import_module(module_path)
        function = getattr(module, function_name)

        result = function(**arguments)

        logger.info(f"Tool {name} executed successfully")
        return result

    except Exception as e:
        logger.error(f"Tool {name} failed: {str(e)}")
        return {"status": "error", "error": str(e)}
