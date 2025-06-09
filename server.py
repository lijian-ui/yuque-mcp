#from mcp.server.fastmcp import FastMCP
from fastmcp import FastMCP
from fastmcp.server.dependencies import get_http_request
from starlette.requests import Request
import asyncio
from pathlib import Path
import importlib.util
from mcp_instance import mcp


# 加载工具模块
TOOLS_DIR = "tools"

def load_all_modules_from_directory():
    """加载 tools/ 下所有 .py 模块，不做任何判断"""
    tools_path = Path(TOOLS_DIR)

    if not tools_path.exists():
        raise FileNotFoundError(f"Tools directory '{TOOLS_DIR}' not found.")

    for file in tools_path.iterdir():
        if file.is_file() and file.suffix == ".py" and file.name != "__init__.py":
            module_name = f"{TOOLS_DIR}.{file.stem}"
            # 加载模块
            spec = importlib.util.spec_from_file_location(module_name, file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            print(f"Loaded module: {module_name}")

import argparse

#运行服务器，使用标准输入输出传输
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run MCP server with transport option")
    parser.add_argument(
        "--transport",
        type=str,
        choices=["streamable-http", "sse", "stdio"],
        default="streamable-http",
        help="Transport mode for the server (default: streamable-http)",
    )
    args = parser.parse_args()

    # 加载工具模块
    print("Loading tools...")
    load_all_modules_from_directory()  # ✅ 调用函数加载模块

    # 初始化并运行服务器
    try:
        print(f"Starting server with transport={args.transport}...")
        mcp.run(transport=args.transport)

    except KeyboardInterrupt:  # 捕获 Ctrl+C 中断信号, 优雅退出
        print("Server stopped by user.")

    except Exception as e:
        print(f"Error: {e}")

