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
async def get_yuque_doc_detail(group_login: str = "", book_slug: str = "", doc_id: str = "", page_size: int = 100, page: int = 1) -> list[TextContent]:
    """
    获取语雀知识库中指定文档的详细信息。

    参数说明:
        group_login (str, optional): 团队的 Login（标识符），默认从请求头或环境变量中自动获取。
        book_slug (str, optional): 知识库的路径（slug），默认从请求头或环境变量中自动获取。
        doc_id (str or int): 要获取详情的文档 ID 或文档路径（必填项）。
        page_size (int, optional): 分页参数，每页返回的数据条目数，默认为 100。
        page (int, optional): 分页参数，当前请求的页码，默认为 1。

    返回值:
        dict: 包含文档详细信息的字典，如标题、内容、创建时间、更新时间、作者等信息。
    
    示例用法:
        get_yuque_doc_detail(doc_id="example-doc", group_login="myteam", book_slug="wiki")

    注意事项:
        - 如果未提供 `group_login` 或 `book_slug`，将尝试从上下文中自动获取。
        - `doc_id` 可以为数字 ID 或字符串形式的路径（slug）。
        - 返回内容可能包含 Markdown 格式的正文，具体以语雀 API 返回为准。
    """
    # 获取请求对象
    request: Request = get_http_request()
    space_subdomain = request.headers.get("YUQUE_SPACE_SUBDOMAIN") or YUQUE_SPACE_SUBDOMAIN
    api_token = request.headers.get("DEFAULT_API_TOKEN") or DEFAULT_API_TOKEN
    group_login = group_login or request.headers.get("DEFAULT_GROUP_LOGIN") or DEFAULT_GROUP_LOGIN
    book_slug = book_slug or request.headers.get("DEFAULT_BOOK_SLUG") or DEFAULT_BOOK_SLUG

    if not api_token or not group_login or not book_slug or not doc_id:
        return [TextContent(type="text", text="缺少必要的API_TOKEN、GROUP_LOGIN、BOOK_SLUG或文档ID参数，请检查配置。")]

    url = f"https://{space_subdomain}.yuque.com/api/v2/repos/{group_login}/{book_slug}/docs/{doc_id}"
    headers = {
        "X-Auth-Token": api_token,
        "Content-Type": "application/json"
    }
    params = {
        "page_size": page_size,
        "page": page
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json().get("data", {})
            if not data:
                return [TextContent(type="text", text="未找到文档详情。")]
            # Format document details as text
            detail_text = f"文档详情:\n标题: {data.get('title', '')}\nID: {data.get('id', '')}\n描述: {data.get('description', '')}\n创建时间: {data.get('created_at', '')}\n更新时间: {data.get('updated_at', '')}\n阅读数: {data.get('read_count', 'N/A')}\n点赞数: {data.get('likes_count', 'N/A')}\n评论数: {data.get('comments_count', 'N/A')}\n内容:\n{data.get('body', '')}"
            return [TextContent(type="text", text=detail_text)]
        else:
            return [TextContent(type="text", text=f"获取文档详情失败，状态码: {response.status_code}，信息: {response.text}")]
    except Exception as e:
        return [TextContent(type="text", text=f"请求异常: {str(e)}")]
