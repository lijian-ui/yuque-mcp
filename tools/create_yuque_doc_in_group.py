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
async def create_yuque_doc_in_group(group_name: str, doc_title: str, doc_body: str) -> list[TextContent]:
    """
    在指定的语雀知识库中的指定分组下创建一个文档。如果该分组不存在，则会先创建该分组，再在其中创建文档。

    参数说明:
        group_name (str): 分组名称。如果该分组不存在，将自动创建。
        doc_title (str): 要创建的文档的标题。
        doc_body (str): 文档的内容，支持 Markdown 格式。

    返回值:
        str: 创建结果信息，包含是否成功、错误信息（如有）、文档或分组的链接或 ID 等。

    示例用法:
        create_yuque_doc_in_group(group_name="项目文档", doc_title="需求说明书", doc_body="# 项目需求\n...")

    注意事项:
        - 需要确保已正确配置语雀 API Token 和知识库相关信息。
        - 若分组或文档已存在，行为取决于具体实现，可选择更新或跳过。
    """
    
    request: Request = get_http_request()
    space_subdomain = request.headers.get("YUQUE_SPACE_SUBDOMAIN") or YUQUE_SPACE_SUBDOMAIN
    api_token = request.headers.get("DEFAULT_API_TOKEN") or DEFAULT_API_TOKEN
    group_login = request.headers.get("DEFAULT_GROUP_LOGIN") or DEFAULT_GROUP_LOGIN
    book_slug = request.headers.get("DEFAULT_BOOK_SLUG") or DEFAULT_BOOK_SLUG

    if not api_token or not group_login or not book_slug:
        return [TextContent(type="text", text="缺少必要的API_TOKEN、GROUP_LOGIN或BOOK_SLUG参数，请检查配置。")]

    if not group_name:
        return [TextContent(type="text", text="缺少分组名称参数 group_name。")]

    if not doc_title:
        return [TextContent(type="text", text="缺少文档标题参数 doc_title。")]

    if not doc_body:
        return [TextContent(type="text", text="缺少文档内容参数 doc_body。")]

    # 获取目录结构
    url_toc = f"https://{space_subdomain}.yuque.com/api/v2/repos/{group_login}/{book_slug}/toc"
    headers = {
        "X-Auth-Token": api_token,
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(url_toc, headers=headers)
        if response.status_code != 200:
            return [TextContent(type="text", text=f"获取目录失败，状态码: {response.status_code}，信息: {response.text}")]
        toc_list = response.json().get("data", [])
    except Exception as e:
        return [TextContent(type="text", text=f"请求异常: 获取目录失败，{str(e)}")]

    # 查找分组uuid
    group_uuid = None
    for node in toc_list:
        if node.get("type") == "TITLE" and node.get("title") == group_name:
            group_uuid = node.get("uuid")
            break

    # 如果分组不存在，创建分组节点
    if not group_uuid:
        url_create_group = url_toc
        payload_group = {
            "action": "appendNode",
            "action_mode": "child",
            "type": "TITLE",
            "title": group_name,
            "visible": 1
        }
        try:
            response = requests.put(url_create_group, json=payload_group, headers=headers)
            if response.status_code != 200:
                return [TextContent(type="text", text=f"创建分组失败，状态码: {response.status_code}，信息: {response.text}")]
            data = response.json().get("data", [])
            if data and isinstance(data, list):
                group_uuid = data[-1].get("uuid")
            elif isinstance(data, dict):
                group_uuid = data.get("uuid")
            else:
                return [TextContent(type="text", text="创建分组失败，未获取到分组UUID。")]
        except Exception as e:
            return [TextContent(type="text", text=f"请求异常: 创建分组失败，{str(e)}")]

    # 创建文档
    url_create_doc = f"https://souche.yuque.com/api/v2/repos/{group_login}/{book_slug}/docs"
    payload_doc = {
        "title": doc_title,
        "body": doc_body,
        "format": "markdown",
        "public": 0
    }
    try:
        response = requests.post(url_create_doc, json=payload_doc, headers=headers)
        if response.status_code != 200:
            return [TextContent(type="text", text=f"文档创建失败，状态码: {response.status_code}，信息: {response.text}")]
        doc_data = response.json().get("data", {})
        doc_id = doc_data.get("id")
        if not doc_id:
            return [TextContent(type="text", text="文档创建失败，未获取到文档ID。")]
    except Exception as e:
        return [TextContent(type="text", text=f"请求异常: 创建文档失败，{str(e)}")]

    # 更新目录，将文档添加到分组
    url_update_toc = url_toc
    payload_update_toc = {
        "action": "appendNode",
        "action_mode": "child",
        "target_uuid": group_uuid,
        "type": "DOC",
        "doc_ids": [doc_id],
        "visible": 1
    }
    try:
        response = requests.put(url_update_toc, json=payload_update_toc, headers=headers)
        if response.status_code != 200:
            return [TextContent(type="text", text=f"目录更新失败，状态码: {response.status_code}，信息: {response.text}")]
    except Exception as e:
        return [TextContent(type="text", text=f"请求异常: 目录更新失败，{str(e)}")]

    return [TextContent(type="text", text=f"文档 '{doc_title}' 创建成功并添加到分组 '{group_name}'。")]
