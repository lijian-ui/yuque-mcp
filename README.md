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
- `YUQUE_SPACE_SUBDOMAIN`：语雀空间子域名（用于访问语雀空间的URL前缀，如 https://[SUBDOMAIN].yuque.com）
- `DEFAULT_API_TOKEN`：默认API访问令牌（用于认证调用语雀API的权限）
- `DEFAULT_GROUP_LOGIN`：默认群组（团队）别名（指定需要访问的语雀群组标识）
- `DEFAULT_BOOK_SLUG`：默认知识库别名（语雀文档库的唯一标识符，用于定位具体文档库）

示例：
```
YUQUE_SPACE_SUBDOMAIN=your_space_subdomain_here
DEFAULT_API_TOKEN=your_api_token_here
DEFAULT_GROUP_LOGIN=your_group_login_here
DEFAULT_BOOK_SLUG=your_book_slug_here
```

此外，也可以通过mcp客户端请求头传递这些变量，示例配置文件如下：

```json
{
    "mcpServers": {
       "yuque-mcp": {
          "url": "http://192.168.125.89:8000/mcp",
          "headers": {
              "YUQUE_SPACE_SUBDOMAIN": "www",
              "DEFAULT_API_TOKEN": "M4HeyBFsRmyNDsdfsdfsdf7ut3YFPX",
              "DEFAULT_GROUP_LOGIN": "oxsdf47",
              "DEFAULT_BOOK_SLUG": "vfgsd6"
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

## 语雀文档重要的概念
接口域名为 https://www.yuque.com，但要注意访问空间内资源需要使用该空间的子域名。

网址路径：语雀的网址有一定的格式，比如https://www.yuque.com/yuque/developer/api。
这里面包含了用户或团队的名称、知识库的标识，以及文档的标识。

```
https://www.yuque.com/yuque/developer/api        [文档完整访问路径]
                        |
                        +-- yuque/               [团队或用户的登录名(group_login)]
                                |
                                +-- developer/   [知识库的标识(book_slug)]
                                       |
                                       +-- api   [文档的标识(doc_slug)]

```

## 语雀文档身份认证

语雀所有的开放 API 都需要 Token 验证之后才能访问。

### 个人用户认证 超级会员专享权益
获取 Token 可通过点击语雀的个人头像，并进入 个人设置 页面拿到，如下图：

![image](https://github.com/user-attachments/assets/daf7caca-ac77-4177-9857-fea0934e0edc)

### 企业团队身份认证 旗舰版空间专享权益
空间内的团队，可进入团队设置页面进行获取（仅旗舰版空间可使用），如下图。
![image](https://github.com/user-attachments/assets/4ec55e0e-b0d6-4e69-af83-628578700062)



## 贡献指南

欢迎提交 Issue 和 Pull Request，改进功能或修复问题。

## 联系方式

如有疑问，请联系项目维护者。
