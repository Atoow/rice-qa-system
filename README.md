# 水稻种植智能问答系统

> 🚧 **当前为 MVP（最小可行产品）版本，并非最终版。** 后续计划：知识图谱集成、Docker 容器化部署、流式响应、模型微调。

基于 RAG（检索增强生成）的水稻种植知识问答系统。

**四川农业大学 2026 本科生科研兴趣培养计划项目**

## 技术栈

- 后端: FastAPI + Python
- LLM: Ollama `qwen3.5:4b`（本机 RTX 4060 GPU 推理、完全离线）
- Embedding: `shaw/dmeta-embedding-zh`（中文语义向量化，768 维）
- 向量检索: 自实现 numpy 余弦相似度检索引擎（零外部依赖）
- 文档处理: LangChain Text Splitter + pypdf
- 业务数据库: SQLite
- 前端: 原生 HTML/CSS/JS（零框架依赖）

## 快速启动

```bash
# 1. 安装 Python 依赖
pip install -r backend/requirements.txt --break-system-packages

# 2. 确保 Ollama 服务运行且已拉取模型
ollama serve
ollama pull qwen3.5:4b
ollama pull shaw/dmeta-embedding-zh

# 3. 启动后端
cd rice-qa-system
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# 4. 打开浏览器
#   对话页面:   http://localhost:8000/
#   管理后台:   http://localhost:8000/admin.html
#   API 文档:   http://localhost:8000/docs
#   健康检查:   http://localhost:8000/api/health
```

## 使用流程

1. 打开管理后台 → 上传水稻种植知识文档（PDF / Markdown / TXT）
2. 系统自动切分文本、向量化、存入本地检索引擎
3. 打开对话页面 → 输入水稻种植问题 → 获取 AI 回答（附带知识来源引用）

## 项目结构

```
rice-qa-system/
├── backend/
│   ├── main.py              # FastAPI 入口
│   ├── config.py            # 配置项
│   ├── requirements.txt
│   ├── llm/                 # LLM 抽象层
│   │   ├── provider.py      # OllamaProvider
│   │   └── prompts.py       # Prompt 构建
│   ├── rag/                 # RAG 检索
│   │   ├── embedding.py     # Embedding 向量化
│   │   ├── retriever.py     # 向量检索引擎（numpy 余弦相似度）
│   │   └── loader.py        # 文档加载切分
│   ├── routes/
│   │   ├── chat.py          # POST /chat
│   │   └── admin.py         # POST /admin/upload, GET /admin/stats
│   └── db/
│       └── models.py        # SQLite 对话历史
├── frontend/
│   ├── index.html           # 对话页面
│   └── admin.html           # 管理后台
├── data/
│   └── documents/           # 原始知识文档
└── README.md
```

## 设计文档

详见 [rice-qa-system-design.md](../rice-qa-system-design.md)

## License

MIT
