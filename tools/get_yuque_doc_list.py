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
async def get_yuque_doc_list(group_login: str = "", book_slug: str = "", offset: int = 0, limit: int = 100) -> list[TextContent]:
    """
    获取语雀知识库中的文档列表。

    参数说明:
        group_login (str, optional): 团队的 Login（唯一标识），默认从请求头或环境变量中自动获取。
        book_slug (str, optional): 知识库的路径标识（slug），默认从请求头或环境变量中自动获取。
        offset (int, optional): 分页偏移量，用于指定从第几条数据开始返回，默认为 0。
        limit (int, optional): 每页返回的文档数量，最大支持 100 条，默认为 100。

    返回值:
        list: 包含文档基本信息的列表，每个元素为一个字典，包含文档 ID、标题、更新时间等信息。

    示例用法:
        get_yuque_doc_list(group_login="myteam", book_slug="wiki", offset=0, limit=50)

    注意事项:
        - 如果未提供 `group_login` 或 `book_slug`，将尝试从上下文中自动获取。
        - 若知识库为空或无权限访问，可能返回空列表或错误信息，具体取决于实现方式。
    """
    request: Request = get_http_request()
    space_subdomain = request.headers.get("YUQUE_SPACE_SUBDOMAIN") or YUQUE_SPACE_SUBDOMAIN
    api_token = request.headers.get("DEFAULT_API_TOKEN") or DEFAULT_API_TOKEN
    group_login = request.headers.get("DEFAULT_GROUP_LOGIN") or DEFAULT_GROUP_LOGIN
    book_slug = request.headers.get("DEFAULT_BOOK_SLUG") or DEFAULT_BOOK_SLUG

    if not api_token or not group_login or not book_slug:
        return [TextContent(type="text", text="缺少必要的API_TOKEN、GROUP_LOGIN或BOOK_SLUG参数，请检查配置。")]

    url = f"https://{space_subdomain}.yuque.com/api/v2/repos/{group_login}/{book_slug}/docs"
    headers = {
        "X-Auth-Token": api_token,
        "Content-Type": "application/json"
    }
    params = {
        "offset": offset,
        "limit": limit,
        "optional_properties": "hits,tags,latest_version_id"
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json().get("data", [])
            if not data:
                return [TextContent(type="text", text="文档列表为空。")]
            # Format document list as text
            doc_list_text = "文档列表:\n"
            for doc in data:
                title = doc.get("title", "无标题")
                doc_id = doc.get("id", "")
                doc_list_text += f"- {title} (ID: {doc_id})\n"
            return [TextContent(type="text", text=doc_list_text)]
        else:
            return [TextContent(type="text", text=f"获取文档列表失败，状态码: {response.status_code}，信息: {response.text}")]
    except Exception as e:
        return [TextContent(type="text", text=f"请求异常: {str(e)}")]
