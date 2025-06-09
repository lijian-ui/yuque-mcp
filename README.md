# 语雀知识库管理 MCP 服务器

## 项目简介
本项目基于 FastMCP 框架，提供一个专门用于管理语雀知识库的 MCP 服务器。  
该服务器支持自动识别并创建知识库分组，创建或更新文档，获取文档详情、文档列表及完整知识库目录，支持分页查询与结构化数据返回。  
所有操作均基于语雀官方 API 实现。

## 环境配置

### 依赖安装
请确保已安装 Python 3.8+，并安装依赖包。  
本项目主要依赖以下 Python 包：
- fastmcp
- starlette
- requests
- python-dotenv

可使用以下命令安装：
```bash
pip install fastmcp starlette requests python-dotenv
```

如果项目根目录有 `requirements.txt` 文件，也可使用：
```bash
pip install -r requirements.txt
```

### 环境变量配置
请在项目根目录创建 `.env` 文件，配置以下环境变量：
- `DEFAULT_API_TOKEN`：语雀 API 访问令牌
- `DEFAULT_GROUP_LOGIN`：团队的 Login（唯一标识）
- `DEFAULT_BOOK_SLUG`：知识库的路径标识（slug）

示例：
```
DEFAULT_API_TOKEN=your_api_token_here
DEFAULT_GROUP_LOGIN=your_group_login_here
DEFAULT_BOOK_SLUG=your_book_slug_here
```

此外，也可以通过客户端请求头传递这些变量，示例配置文件如下：

```json
{
    "mcpServers": {
       "yuque-mcp": {
          "url": "http://192.168.125.89:8000/mcp",
          "headers": {
              "DEFAULT_API_TOKEN": "M4HeyBFsRmyNDflrqSwzh7BSv23434ysLb7ut3YFPX",
              "DEFAULT_GROUP_LOGIN": "oxv2347",
              "DEFAULT_BOOK_SLUG": "v2335y6"
            }
        }
    }
}
```



## 启动服务

运行服务器主程序 `server.py`，支持多种传输模式：

```bash
python server.py --transport streamable-http
```

可选传输模式：
- `streamable-http`（默认）：基于 HTTP 流的传输
- `sse`：基于服务器发送事件（Server-Sent Events）
- `stdio`：基于标准输入输出流

## 工具说明

服务器自动加载 `tools/` 目录下的所有工具模块，主要包括：

- `create_yuque_group(name: str)`  
  创建语雀知识库中的分组（目录）。

- `create_yuque_doc_in_group(...)`  
  在指定分组下创建或更新文档。

- `get_yuque_doc_list(group_login, book_slug, offset, limit)`  
  获取知识库中的文档列表，支持分页。

- `get_yuque_doc_detail(...)`  
  获取指定文档的详细内容。

- `get_yuque_repo_toc(...)`  
  获取知识库的完整目录结构。



## 使用示例


启动服务器并使用默认传输：

```bash
python server.py
```

指定传输模式为 SSE：

```bash
python server.py --transport sse
```

## 贡献指南

欢迎提交 Issue 和 Pull Request，改进功能或修复问题。

## 联系方式

如有疑问，请联系项目维护者。
