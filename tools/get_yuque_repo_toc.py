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
async def get_yuque_repo_toc() -> list[TextContent]:
    """
    获取语雀知识库的完整目录结构（包括所有分组和文档）。

    参数说明:
        group_login (str, optional): 团队的 Login（唯一标识），默认从请求头或环境变量中自动获取。
        book_slug (str, optional): 知识库的路径标识（slug），默认从请求头或环境变量中自动获取。

    返回值:
        dict or list: 成功时返回知识库的目录结构数据，通常为嵌套结构，包含分组（目录）及其下的文档信息。

    示例用法:
        get_yuque_toc(group_login="myteam", book_slug="wiki")

    注意事项:
        - 如果未提供 `group_login` 或 `book_slug`，将尝试从上下文中自动获取。
        - 返回的数据结构可能包含层级关系，例如：分组 -> 子分组 -> 文档。
        - 适用于需要展示完整知识库结构或进行文档导航的场景。
    """
    # 获取请求对象
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

    url = f"https://{space_subdomain}.yuque.com/api/v2/repos/{group_login}/{book_slug}/toc"
    headers = {
        "X-Auth-Token": api_token,
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            toc_data = response.json()
            return [
                TextContent(
                    type="text",
                    text=f"目录获取成功: {toc_data}",
                )
            ]
        else:
            return [
                TextContent(
                    type="text",
                    text=f"获取目录失败，状态码: {response.status_code}，信息: {response.text}",
                )
            ]
    except Exception as e:
        return [
            TextContent(
                type="text",
                text=f"请求异常: {str(e)}",
            )
        ]
