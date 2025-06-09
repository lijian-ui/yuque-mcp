import os
import requests
from mcp.types import TextContent
from dotenv import load_dotenv
from mcp_instance import mcp
load_dotenv()
from fastmcp.server.dependencies import get_http_request
from starlette.requests import Request

YUQUE_SPACE_SUBDOMAIN = os.getenv("YUQUE_SPACE_SUBDOMAIN", "")
DEFAULT_API_TOKEN = os.getenv("DEFAULT_API_TOKEN", "")
DEFAULT_GROUP_LOGIN = os.getenv("DEFAULT_GROUP_LOGIN", "")
DEFAULT_BOOK_SLUG = os.getenv("DEFAULT_BOOK_SLUG", "")

@mcp.tool()
async def create_yuque_group(name: str) -> list[TextContent]:
    """
    创建一个语雀知识库中的分组（目录）。

    参数说明:
        name (str): 要创建的分组名称。该名称在当前知识库中应具有唯一性。

    返回值:
        Group: 创建成功的分组对象，包含分组的 ID、名称等信息。
               如果创建失败，可能返回 None 或抛出异常（具体取决于实现方式）。

    示例用法:
        create_yuque_group(name="项目文档")

    注意事项:
        - 若同名分组已存在，可能会返回已有分组或抛出冲突异常，具体行为取决于 API 实现。
        - 需要确保当前用户有权限在目标知识库中创建分组。
    """
    request: Request = get_http_request()
    space_subdomain = request.headers.get("YUQUE_SPACE_SUBDOMAIN") or YUQUE_SPACE_SUBDOMAIN
    api_token = request.headers.get("DEFAULT_API_TOKEN") or DEFAULT_API_TOKEN
    group_login = request.headers.get("DEFAULT_GROUP_LOGIN") or DEFAULT_GROUP_LOGIN
    book_slug = request.headers.get("DEFAULT_BOOK_SLUG") or DEFAULT_BOOK_SLUG

    if not api_token or not group_login or not book_slug:
        return [
            TextContent(
                type="text",
                text="缺少必要的API_TOKEN、GROUP_LOGIN或BOOK_SLUG参数，请检查配置。",
            )
        ]

    if not name:
        return [
            TextContent(
                type="text",
                text="缺少分组名称参数 name。",
            )
        ]

   
    url = f"https://{space_subdomain}.yuque.com/api/v2/repos/{group_login}/{book_slug}/toc"
    headers = {
        "X-Auth-Token": api_token,
        "Content-Type": "application/json"
    }
    payload = {
        "action": "appendNode",
        "action_mode": "child",
        "type": "TITLE",
        "title": name,
        "visible": 1
    }

    try:
        response = requests.put(url, json=payload, headers=headers)
        if response.status_code == 200:
            return [
                TextContent(
                    type="text",
                    text=f"分组节点 '{name}' 创建成功。",
                )
            ]
        else:
            return [
                TextContent(
                    type="text",
                    text=f"创建分组失败，状态码: {response.status_code}，信息: {response.text}",
                )
            ]
    except Exception as e:
        return [
            TextContent(
                type="text",
                text=f"请求异常: {str(e)}",
            )
        ]
