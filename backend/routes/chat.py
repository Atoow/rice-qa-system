"""对话路由：POST /chat —— 核心 RAG 问答接口。"""
import uuid
import asyncio
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from backend.llm.provider import LLMProvider
from backend.llm.prompts import build_prompt
from backend.rag.retriever import Retriever
from backend.db.models import save_conversation, get_conversation_history

router = APIRouter(prefix="/chat", tags=["对话"])


class ChatRequest(BaseModel):
    session_id: str = Field(default_factory=lambda: uuid.uuid4().hex[:12])
    question: str = Field(..., min_length=1, max_length=500)


class Source(BaseModel):
    title: str
    relevance: float


class ChatResponse(BaseModel):
    session_id: str
    answer: str
    sources: list[Source]


llm_provider: LLMProvider | None = None
retriever: Retriever | None = None


def init_chat(llm: LLMProvider, ret: Retriever):
    global llm_provider, retriever
    llm_provider = llm
    retriever = ret


@router.post("", response_model=ChatResponse)
async def chat(req: ChatRequest):
    if llm_provider is None or retriever is None:
        raise HTTPException(500, "服务未初始化")

    # 1. 语义检索
    results = retriever.search(req.question)

    if not results:
        return ChatResponse(
            session_id=req.session_id,
            answer="知识库中暂无相关信息，建议您咨询当地农技站或拨打12316农业服务热线。",
            sources=[],
        )

    chunks = [r["content"] for r in results]
    sources = [Source(title=r["source"], relevance=r["relevance"]) for r in results]

    # 2. 获取对话历史
    history = get_conversation_history(req.session_id)

    # 3. 构建 Prompt
    messages = build_prompt(
        user_question=req.question,
        retrieved_chunks=chunks,
        sources=[s.title for s in sources],
        history=history,
    )

    # 4. 调用 LLM 生成（最长等待 120 秒）
    try:
        answer = await asyncio.wait_for(
            llm_provider.generate(messages),
            timeout=120.0,
        )
    except asyncio.TimeoutError:
        raise HTTPException(504, "模型生成超时（120s），请尝试更简短的问题，或更换更快的模型。")
    except Exception as e:
        raise HTTPException(502, f"模型调用失败: {str(e)}")

    # 5. 保存对话记录
    save_conversation(req.session_id, "user", req.question)
    save_conversation(
        req.session_id, "assistant", answer,
        [s.title for s in sources],
    )

    return ChatResponse(
        session_id=req.session_id,
        answer=answer,
        sources=sources,
    )
