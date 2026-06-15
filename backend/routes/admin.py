"""管理路由：POST /admin/upload, GET /admin/stats。"""
import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from backend.rag.retriever import Retriever
from backend.rag.loader import DocumentLoader

router = APIRouter(prefix="/admin", tags=["管理"])

retriever: Retriever | None = None
UPLOAD_DIR: str = ""


def init_admin(ret: Retriever, upload_dir: str):
    global retriever, UPLOAD_DIR
    retriever = ret
    UPLOAD_DIR = upload_dir


class UploadResponse(BaseModel):
    status: str
    chunks_created: int
    filename: str


class StatsResponse(BaseModel):
    total_chunks: int
    collection_name: str
    document_files: list[str]


@router.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """上传水稻知识文档（PDF/MD/TXT），自动切分并向量化入库。"""
    if retriever is None:
        raise HTTPException(500, "服务未初始化")

    ext = os.path.splitext(file.filename or "")[1].lower()
    if ext not in (".pdf", ".md", ".txt"):
        raise HTTPException(400, f"不支持的文件类型: {ext}。支持: .pdf, .md, .txt")

    save_path = os.path.join(UPLOAD_DIR, file.filename or "uploaded_file")
    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    loader = DocumentLoader()
    chunks = loader.load_file(save_path)

    if not chunks:
        raise HTTPException(400, "文档中没有提取到有效文本内容")

    count = retriever.add_documents(chunks)

    return UploadResponse(
        status="ok",
        chunks_created=count,
        filename=file.filename or "unknown",
    )


@router.get("/stats", response_model=StatsResponse)
async def get_stats():
    """获取知识库统计信息。"""
    if retriever is None:
        raise HTTPException(500, "服务未初始化")

    stats = retriever.get_collection_stats()

    docs = []
    if os.path.exists(UPLOAD_DIR):
        docs = [f for f in os.listdir(UPLOAD_DIR) if not f.startswith(".")]

    return StatsResponse(
        total_chunks=stats["total_chunks"],
        collection_name=stats["collection_name"],
        document_files=docs,
    )
