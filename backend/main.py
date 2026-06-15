"""FastAPI 主入口：启动服务、注入依赖、挂载路由。"""
import os
import sys

# 确保 backend 包可以被正确导入
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.config import DATABASE_URL
from backend.llm.provider import OllamaProvider
from backend.rag.embedding import OllamaEmbedding
from backend.rag.retriever import Retriever
from backend.db.models import init_db
from backend.routes.chat import init_chat, router as chat_router
from backend.routes.admin import init_admin, router as admin_router

# === 应用创建 ===
app = FastAPI(
    title="水稻种植智能问答系统",
    description="基于 RAG 的水稻种植知识问答系统 API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# === API 路由（必须在静态文件挂载之前注册）===

@app.get("/api/health")
async def health():
    """健康检查。"""
    return {"status": "ok", "message": "水稻 QA 系统运行中"}


# === 依赖初始化 ===
print("正在连接 Ollama...")
embedding = OllamaEmbedding()
llm = OllamaProvider()
retriever = Retriever(embedding=embedding)
print("Ollama 连接成功！")

# 文档上传目录
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "documents")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 注入到路由
init_chat(llm, retriever)
init_admin(retriever, UPLOAD_DIR)

# 初始化数据库
init_db()
print(f"SQLite 数据库初始化完成: {DATABASE_URL}")

# === 挂载路由 ===
app.include_router(chat_router)
app.include_router(admin_router)

# === 静态文件（前端页面）===  —— 必须放在最后，否则会拦截所有 API 请求
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
    print(f"前端页面已挂载: {FRONTEND_DIR}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
