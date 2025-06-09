# mcp_instance.py
from fastmcp import FastMCP

mcp = FastMCP(
    name="yuque_mcp",
    instructions = "你是一个语雀知识库管理代理，具备以下能力：\n" \
                "- 自动识别并创建所需分组\n" \
                "- 支持在指定分组下创建或更新文档\n" \
                "- 获取文档详情、文档列表及完整知识库目录\n" \
                "- 支持分页查询与结构化数据返回\n" \
                "所有操作基于语雀 API 完成，请确保上下文参数（如 group_login, book_slug）已正确配置。",
    stateless_http=True,
    json_response=True,
    port=8000,
    host="0.0.0.0"
)
